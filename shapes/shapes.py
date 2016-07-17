from utils.my_qt import *
from utils.utils import average
ABC = ''.join(chr(ord('A') + i) for i in xrange(26))


class PointItem(QtGui.QGraphicsItem):
    def __init__(self, x, y, color, radius, owner, text, parent=None, scene=None):
        super(PointItem, self).__init__(parent, scene)
        self._point = QtCore.QPointF(x, y)
        self._radius = radius
        self.color = color
        self._owner = owner
        adjust = 0.5
        self._bounding_rect = QtCore.QRectF(-self._radius - adjust, -self._radius * 3 - adjust,
                                            self._radius * 3 + adjust, self._radius * 5 + adjust)
        self._text = text
        self.setPos(self._point)

    def move_to(self, point):
        self._point = point
        self.setPos(point)

    def extra_items(self):
        return []

    def get_owner(self):
        return self._owner

    def get_point(self):
        return self._point

    def get_text(self):
        return self._text

    def my_transform(self, transformation):
        self.move_to(transformation.transform_point(self._point))
        self.update()

    def boundingRect(self):
        return self._bounding_rect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-self._radius, -self._radius, self._radius * 2, self._radius * 2)
        return path

    def paint(self, painter, option, widget):
        """

        :param painter:
         :type painter: QtGui.QPainter
        :param option:
        :param widget:
        :return:
        """
        # Body.
        font = QtGui.QFont()
        font.setBold(True)
        font.setPixelSize(self._radius * 2)
        painter.setFont(font)
        painter.drawText(-QtCore.QPoint(0, self._radius), self._text)
        painter.setBrush(QtGui.QColor("purple"))
        shape = self.shape()
        painter.drawPath(shape)


class PolygonItem(QtGui.QGraphicsItem):
    def __init__(self, points, color, parent=None, scene=None):
        super(PolygonItem, self).__init__(parent, scene)
        self.color = color
        self._points_items = [PointItem(p.x(), p.y(), self.color, 8, self, letter) for p, letter in zip(points, ABC)]
        for p in self._points_items:
            p.setCursor(QtCore.Qt.OpenHandCursor)
        self._polygon = self._get_polygon()

    def my_transform(self, transformation):
        self.hide()
        for p in self._points_items:
            p.my_transform(transformation)
        self._polygon = self._get_polygon()
        self.show()
        self.update()

    def extra_items(self):
        return self._points_items

    def boundingRect(self):
        return self._polygon.boundingRect()

    def shape(self):
        path = QtGui.QPainterPath()
        path.addPolygon(self._polygon)
        return path

    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setBrush(self.color)
        painter.setBrush(QtGui.QColor(0, 0, 0, 0))
        painter.setPen(pen)
        painter.drawPath(self.shape())

    def _get_polygon(self):
        return QtGui.QPolygonF([p.get_point() for p in self._points_items] + [self._points_items[0].get_point()])

    def mean(self):
        return average([self._polygon.at(i) for i in xrange(self._polygon.size() - 1)])


class RectangleItem(PolygonItem):
    def __init__(self, rect, color):
        """
        :param rect:
        :type rect: QtCore.QRectF
        :param color:
        :return:
        """
        super(RectangleItem, self).__init__([rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()],
                                            color)




