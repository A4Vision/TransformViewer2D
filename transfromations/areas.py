import abc
from utils.my_qt import *


def size(point):
    return (point.x() ** 2 + point.y() ** 2) ** 0.5


def distance(point1, point2):
    return size(point2 - point1)


class LegalPath(object):
    @abc.abstractmethod
    def get_path(self, rect):
        return QtGui.QPainterPath()

    @abc.abstractmethod
    def get_brush(self):
        return QtGui.QBrush()

    @abc.abstractmethod
    def project_point(self, point):
        """
        :param point:
        :type point:QtCore.QPointF
        :return:
        """
        return point


class CirclePath(LegalPath):
    def __init__(self, center, radius):
        assert radius > 0
        self._center = QtCore.QPointF(center)
        self._radius = radius

    def get_path(self, rect):
        path = QtGui.QPainterPath()
        path.addEllipse(self._center.x() - self._radius, self._center.y() - self._radius,
                        self._center.x() + self._radius * 2, self._center.y() + self._radius * 2)
        return path

    def get_brush(self):
        return QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

    def project_point(self, point):
        """

        :param point:
        :type point: QtGui.QPointF
        :return:
        """
        moved = QtCore.QPointF(point) - self._center
        if size(moved) == 0:
            on_circle = QtCore.QPointF(0, self._radius)
        else:
            on_circle = moved / size(moved) * self._radius
        assert abs(size(on_circle) - self._radius) < 0.0001
        res = self._center + on_circle
        assert abs(distance(self._center, res) - self._radius) < 0.0001
        return res




c = CirclePath(QtCore.QPoint(50, 50), (50 ** 2 * 2) ** 0.5)
x = c.project_point(QtCore.QPointF(40, 50))


class AllLegalPath(LegalPath):
    def get_path(self, rect):
        path = QtGui.QPainterPath()
        path.addRect(rect)
        return path

    def project_point(self, point):
        return point

    def get_brush(self):
        return QtGui.QBrush(QtGui.QColor(0, 255, 0, 40))


