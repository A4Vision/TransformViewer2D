import abc
import functools

from shapes.shapes import RectangleItem, PointItem, PolygonItem
from transfromations.transformations_builders import TranslationBuilder, RigidBuilder, SimilarityBuilder, AffineBuilder
from utils.my_qt import *
from dock import Ui_DockWidget as Dock
import sys


L_SPOTS = [QtCore.Qt.LeftDockWidgetArea, QtCore.Qt.RightDockWidgetArea, QtCore.Qt.BottomDockWidgetArea,
           QtCore.Qt.TopDockWidgetArea]


def update_layout(form, new_area):
    layout = form.buttons_layout
    # if new_area in (QtCore.Qt.LeftDockWidgetArea, QtCore.Qt.RightDockWidgetArea):
    #     print 'left right'
    # else:
    #     print 'top buttom'
    if (new_area in (QtCore.Qt.LeftDockWidgetArea, QtCore.Qt.RightDockWidgetArea)) == \
            (isinstance(layout, QtGui.QHBoxLayout)):
        # print 'changing layout'
        if isinstance(layout, QtGui.QHBoxLayout):
            new_layout = QtGui.QVBoxLayout()
        else:
            new_layout = QtGui.QHBoxLayout()
        w = layout.parent()
        while layout.count() > 0:
            c = layout.itemAt(0).widget()
            layout.removeWidget(c)
            new_layout.addWidget(c)
        w.removeItem(layout)
        w.addLayout(new_layout)
        form.buttons_layout = new_layout


class PolygonFinder(object):
    def __init__(self, scene):
        """

        :param scene:
        :type scene: QtGui.QGraphicsScene
        :return:
        """
        self._scene = scene

    def has_point_at(self, pos):
        item = self._scene.itemAt(pos)
        return item is not None and isinstance(item, PointItem) and isinstance(item.get_owner(), PolygonItem)

    def point_at(self, pos):
        return self._scene.itemAt(pos)


class TempItemDrawer(object):
    def __init__(self, scene):
        """

        :param scene:
        :type scene: QtGui.QGraphicsScene
        :return:
        """
        self._scene = scene
        self._temp_items = set()

    def draw_temp_item(self, item):
        self._scene.addItem(item)
        self._temp_items.add(item)

    def erase_temp_item(self, item):
        self._scene.removeItem(item)
        self._temp_items.remove(item)

    def clear(self):
        for item in self._temp_items:
            self._scene.removeItem(item)
        self._temp_items.clear()


class HandlesMouseGUI(object):
    MODE_DISABLED = 'DISABLED'

    def __init__(self):
        self._mode = self.MODE_DISABLED

    def enabled(self):
        return self._mode != self.MODE_DISABLED

    @abc.abstractmethod
    def mouseReleased(self, pos, scene_pos):
        pass

    @abc.abstractmethod
    def mousePressed(self, pos, scene_pos):
        pass

    @abc.abstractmethod
    def mouseMoved(self, pos, scene_pos):
        pass


class TransformerGUI(HandlesMouseGUI):
    MODE_DRAGGING = 'DRAG'
    MODE_WAIT_TO_SELECT = 'WAIT'

    def __init__(self, polygon_finder, temp_items_drawer, transformation_builder_getter, scene_rect):
        """
        :param polygon_finder:
        :type polygon_finder: PolygonFinder
        :param temp_items_drawer:
        :type temp_items_drawer: TempItemDrawer
        :return:
        """
        super(TransformerGUI, self).__init__()
        self._polygon_finder = polygon_finder
        self._temp_items_drawer = temp_items_drawer
        self._transformation_builder_getter = transformation_builder_getter
        self._scene_rect = scene_rect

        self._init_drag()

    def mouseReleased(self, pos, scene_pos):
        if self._mode == self.MODE_DRAGGING:
            legal = self._current_transformation_builder.legal_path(self._current_src_point.get_point())
            projected = legal.project_point(scene_pos)
            assert not self._current_transformation_builder.is_done()
            new_builder = self._current_transformation_builder.move_point(self._current_src_point.get_point(), projected)
            if new_builder.is_done():
                self._mode = self.MODE_DISABLED
                transformation = new_builder.get_transformation()
                self._current_transformed_polygon.my_transform(transformation)
                self._init_drag()
            else:
                self._mode = self.MODE_WAIT_TO_SELECT
                self._current_transformation_builder = new_builder
                self._current_dragged_item = None
                self._current_src_point = None

    def mousePressed(self, pos, scene_pos):
        if self._polygon_finder.has_point_at(scene_pos):
            point = self._polygon_finder.point_at(scene_pos)
            polygon = point.get_owner()
            assert isinstance(point, PointItem)
            if self._mode == self.MODE_DISABLED:
                self._current_transformation_builder = self._transformation_builder_getter()
                self._current_transformed_polygon = polygon
                self._start_dragging(point, polygon, scene_pos)
            elif self._mode == self.MODE_WAIT_TO_SELECT and polygon == self._current_transformed_polygon and \
                point.get_point() not in self._current_transformation_builder.sources():
                assert self._current_transformation_builder is not None
                assert not self._current_transformation_builder.is_done()
                self._start_dragging(point, polygon, scene_pos)

    def mouseMoved(self, pos, scene_pos):
        if self._mode == self.MODE_DRAGGING:
            self._update_dragging(scene_pos)

    def reset(self):
        self._init_drag()

    def _start_dragging(self, src_point_item, polygon, dst_point):
        """
        :param src_point_item:
        :type src_point_item: PointItem
        :param polygon:
        :param dst_point:
        :type dst_point: QtGui.QPointF
        :return:
        """
        self._current_src_point = src_point_item
        self._current_dragged_item = PointItem(dst_point.x(), dst_point.y(),
                                               QtGui.QColor(255, 0, 0), 4, None, src_point_item.get_text())
        self._temp_items_drawer.draw_temp_item(self._current_dragged_item)
        self._mode = self.MODE_DRAGGING
        self._update_dragging(dst_point)

    def _update_dragging(self, point):
        legal = self._current_transformation_builder.legal_path(self._current_src_point.get_point())
        projected = legal.project_point(point)
        self._current_dragged_item.move_to(projected)
        self._current_dragged_item.update()

    def _init_drag(self):
        self._current_transformation_builder = None
        self._current_src_point = None
        self._current_dragged_item = None
        self._current_transformed_polygon = None
        self._temp_items_drawer.clear()

    def scene_rect_changed(self, new_rect):
        self._scene_rect = new_rect


class RectanglesDAST(object):
    def __init__(self, scene):
        """
        :param scene:
        :type scene: QtGui.QGraphicsScene
        :return:
        """
        self._scene = scene
        self._items = []
        self._temp_items = []

    def finder(self):
        return PolygonFinder(self._scene)

    def creator(self):
        return RectanglesCreator(self)

    def temp_items_drawer(self):
        return TempItemDrawer(self._scene)

    def transform_all(self, transformation):
        pass

    def get_scene(self):
        return self._scene

    def add_item(self, item, is_temp):
        self._scene.addItem(item)
        for extra_item in item.extra_items():
            self._scene.addItem(extra_item)



class RectanglesCreator(object):
    def __init__(self, rectangles_dast):
        self._rectangles_dast = rectangles_dast

    def add_rectangle(self, rect):
        item = RectangleItem(rect, QtGui.QColor("blue"))
        self._rectangles_dast.add_item(item, False)



class RectanglesCreatorGUI(HandlesMouseGUI):
    MODE_DRAWING = 'DRAWING'
    MODE_WAIT_TO_DRAW = 'WAIT'

    def __init__(self, rectangles_creator, rubber_band_parent):
        """

        :param rectangles_creator:
        :type rectangles_creator: RectanglesCreator
        :param rubber_band_parent:
        :return:
        """
        super(RectanglesCreatorGUI, self).__init__()
        self._rectangles_creator = rectangles_creator
        self._rubber_band = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle, rubber_band_parent)
        self._rubber_band.hide()
        self._origin = QtCore.QPoint(0, 0)
        self._origin_scene = QtCore.QPoint(0, 0)
        self._target_scene = QtCore.QPoint(0, 0)

    def mouseReleased(self, pos, scene_pos):
        if self._mode == self.MODE_DRAWING:
            self._add_current_rectangle()
            self._mode = self.MODE_WAIT_TO_DRAW

    def mousePressed(self, pos, scene_pos):
        if self._mode == self.MODE_WAIT_TO_DRAW:
            self._mode = self.MODE_DRAWING
            self._origin = pos
            self._origin_scene = scene_pos
            print 'origin', pos

    def mouseMoved(self, pos, scene_pos):
        if self._mode == self.MODE_DRAWING:
            self._rubber_band.setGeometry(QtCore.QRect(self._origin, pos).normalized())
            self._target_scene = scene_pos
            self._rubber_band.show()

    def update_modifiers(self, modifiers):
        shift = bool(modifiers & QtCore.Qt.SHIFT)
        if self._mode == self.MODE_DISABLED and shift:
            self._mode = self.MODE_WAIT_TO_DRAW
        elif self._mode == self.MODE_DRAWING and not shift:
            self._add_current_rectangle()
            self._mode = self.MODE_DISABLED
        elif self._mode == self.MODE_WAIT_TO_DRAW and not shift:
            self._mode = self.MODE_DISABLED

    def _add_current_rectangle(self):
        assert self._mode == self.MODE_DRAWING
        self._rubber_band.hide()
        self._rectangles_creator.add_rectangle(QtCore.QRectF(self._origin_scene, self._target_scene))


class MyGraphicsView(QtGui.QGraphicsView):
    def __init__(self, dast, transformation_builder_getter, parent=None):
        """
        :param dast:
        :type dast: RectanglesDAST
        :param parent:
        :return:
        """
        super(MyGraphicsView, self).__init__(parent)
        self.setScene(dast.get_scene())
        self._transformerGUI = TransformerGUI(dast.finder(), dast.temp_items_drawer(), transformation_builder_getter,
                                              dast.get_scene().sceneRect())
        dast.get_scene().sceneRectChanged.connect(self._transformerGUI.scene_rect_changed)
        self._rectangles_creatorGUI = RectanglesCreatorGUI(dast.creator(), self)

    def keyPressEvent(self, QKeyEvent):
        self._update_modifiers(QKeyEvent)

    def keyReleaseEvent(self, QKeyEvent):
        self._update_modifiers(QKeyEvent)

    def mousePressEvent(self, QMouseEvent):
        self._handle_mouse_event('press', QMouseEvent)
        super(MyGraphicsView, self).mousePressEvent(QMouseEvent)

    def mouseReleaseEvent(self, QMouseEvent):
        self._handle_mouse_event('release', QMouseEvent)
        super(MyGraphicsView, self).mouseReleaseEvent(QMouseEvent)

    def mouseMoveEvent(self, QMouseEvent):
        self._handle_mouse_event('move', QMouseEvent)
        super(MyGraphicsView, self).mouseMoveEvent(QMouseEvent)

    def _handle_mouse_event(self, event_name, QMouseEvent):
        self._update_modifiers(QMouseEvent)
        if self._rectangles_creatorGUI.enabled():
            gui = self._rectangles_creatorGUI
        else:
            gui = self._transformerGUI
        pos = QMouseEvent.pos()
        scene_pos = self.mapToScene(pos).toPoint()
        if event_name == 'press':
            gui.mousePressed(pos, scene_pos)
        elif event_name == 'move':
            gui.mouseMoved(pos, scene_pos)
        elif event_name == 'release':
            gui.mouseReleased(pos, scene_pos)

    def _update_modifiers(self, event):
        if not self._transformerGUI.enabled():
            self._rectangles_creatorGUI.update_modifiers(event.modifiers())


class MainWin(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self._dock = d = QtGui.QDockWidget("header", self)
        d.setAllowedAreas(reduce(lambda x, y: x | y, L_SPOTS, 0))
        self._transformation_form = form = Dock()
        form.setupUi(d)
        self.addDockWidget(L_SPOTS[0], d)
        d.dockLocationChanged.connect(functools.partial(update_layout, form))

        scene = QtGui.QGraphicsScene()
        scene.setSceneRect(0, 0, 800, 600)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.BspTreeIndex)
        dast = RectanglesDAST(scene)

        view = MyGraphicsView(dast, self.transformation_builder)
        view.setRenderHint(QtGui.QPainter.Antialiasing)
        view.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        view.setDragMode(QtGui.QGraphicsView.NoDrag)

        self.setWindowTitle("Transformations")
        self.setCentralWidget(view)

    def transformation_builder(self):
        # TODO: after implementing the transformations and the builders, update this switch.
        if self._transformation_form.similarity.isChecked():
            return SimilarityBuilder()
        elif self._transformation_form.bilinear_interpolant.isChecked():
            return TranslationBuilder()
        elif self._transformation_form.affine.isChecked():
            return AffineBuilder()
        elif self._transformation_form.projective.isChecked():
            return TranslationBuilder()
        elif self._transformation_form.rigid.isChecked():
            return RigidBuilder()
        elif self._transformation_form.rotation.isChecked():
            return TranslationBuilder()
        elif self._transformation_form.translation.isChecked():
            return TranslationBuilder()
        else:
            return TranslationBuilder()


def main():
    app = QtGui.QApplication(sys.argv)
    w = MainWin()
    w.show()
    app.exec_()


if __name__ == '__main__':
    main()
