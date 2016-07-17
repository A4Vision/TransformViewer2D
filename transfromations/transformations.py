import abc


class Transformation(object):
    def compose(self, transformation):
        return ComposedTransformation([transformation, self])

    @abc.abstractmethod
    def transform_point(self, point):
        """
        :param point:
        :type point: QtCore.QPointF
        :return:
        """
        return point


class IdTransformation(object):
    def transform_point(self, point):
        return point


class ComposedTransformation(object):
    def __init__(self, transformations):
        """
        :param transformations:
        :type transformations: List[Transformation]
        :return:
        """
        self._transformations = list(transformations)

    def transform_point(self, point):
        for t in self._transformations:
            point = t.transform_point(point)
        return point

    def compose(self, transformation):
        return ComposedTransformation([transformation] + self._transformations)
