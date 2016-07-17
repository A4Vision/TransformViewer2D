import math

from utils.my_qt import *
import numpy

from transfromations.transformations import Transformation


class ProjectiveTransformation(Transformation):
    def __init__(self, matrix):
        self._matrix = matrix

    def transform_point(self, point):
        v = (self._matrix * self.to_matrix(point))
        return QtCore.QPointF(v[0, 0] / v[2, 0], v[1, 0] / v[2, 0])

    @staticmethod
    def to_matrix(point):
        """

        :param point:
        :type point: numpy.matrix
        :return:
        """
        return numpy.matrix([[point.x()], [point.y()], [1.0]])

    def compose(self, transformation):
        if isinstance(transformation, ProjectiveTransformation):
            # NOTE: could do here more gentle composing, but rather do it in the
            #       inheritors
            return ProjectiveTransformation(self._matrix * transformation._matrix)
        else:
            return super(ProjectiveTransformation, self).compose(transformation)


class TranslationTransformation(ProjectiveTransformation):
    """
    Simple move transformation.
    """

    def __init__(self, x, y):
        super(TranslationTransformation, self).__init__(numpy.matrix([[1, 0, x],
                                                                      [0, 1, y],
                                                                      [0, 0, 1.0]]))


class RigidTransformation(ProjectiveTransformation):
    def __init__(self, theta, t):
        super(RigidTransformation, self).__init__(
            numpy.matrix([
                [math.cos(theta), -math.sin(theta), t.x()],
                [math.sin(theta), math.cos(theta), t.y()],
                [0, 0, 1.0]]))


class SimilarityTransformation(ProjectiveTransformation):
    def __init__(self, a, b, tx, ty):
        super(SimilarityTransformation, self).__init__(
            numpy.matrix([
                [a, -b, tx],
                [b, a, ty],
                [0, 0, 1.0]]))


class AffineTransformation(ProjectiveTransformation):
    def __init__(self, a00, a01, a02, a10, a11, a12):
        super(AffineTransformation, self).__init__(
            numpy.matrix([
                [a00, a01, a02],
                [a10, a11, a12],
                [0, 0, 1.0]]))


