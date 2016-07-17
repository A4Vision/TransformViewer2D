from collections import namedtuple

import math
import numpy

from transfromations.linear_transformations import TranslationTransformation, RigidTransformation, \
    SimilarityTransformation, AffineTransformation
from utils.my_qt import *
import abc

from transfromations.areas import AllLegalPath, LegalPath, CirclePath, size, distance
from transfromations.transformations import Transformation


class TransformationBuilder(object):
    @abc.abstractmethod
    def move_point(self, src, dst):
        """
        :param src:
        :type src: QtCore.QPointF
        :param dst:
        :type dst: QtCore.QPointF
        :return:
        """
        pass

    @abc.abstractmethod
    def legal_path(self, src):
        """
        :param src:
        :type src: QtCore.QPointF
        :return:
        :rtype LegalPath
        """
        return LegalPath()

    @abc.abstractmethod
    def is_done(self):
        return False

    @abc.abstractmethod
    def get_transformation(self):
       return Transformation()

    @abc.abstractmethod
    def sources(self):
        return []


SrcDst = namedtuple('SrcDst', ['src', 'dst'])


class MultiSrcDstBuilder(TransformationBuilder):
    def __init__(self, n_pairs):
        self._src_dst_pairs = []
        self._n_pairs = n_pairs

    def is_done(self):
        return len(self._src_dst_pairs) == self._n_pairs

    def move_point(self, src, dst):
        assert not self.is_done()
        builder = self.__class__()
        projected_dst = self.legal_path(src).project_point(dst)
        builder._src_dst_pairs = self._src_dst_pairs + [SrcDst(src=src, dst=projected_dst)]
        return builder

    def sources(self):
        return [sd.src for sd in self._src_dst_pairs]


class TranslationBuilder(MultiSrcDstBuilder):
    def __init__(self):
        super(TranslationBuilder, self).__init__(1)

    def legal_path(self, src):
        return AllLegalPath()

    def get_transformation(self):
        assert self.is_done()
        shift = self._src_dst_pairs[0].dst - self._src_dst_pairs[0].src
        return TranslationTransformation(shift.x(), shift.y())


class RigidBuilder(MultiSrcDstBuilder):
    def __init__(self):
        super(RigidBuilder, self).__init__(2)

    def legal_path(self, src):
        if len(self._src_dst_pairs) == 0:
            return AllLegalPath()
        else:
            assert len(self._src_dst_pairs) == 1
            first = self._src_dst_pairs[0]
            return CirclePath(first.dst, distance(first.src, src))

    def get_transformation(self):
        assert self.is_done()
        sd1, sd2 = self._src_dst_pairs
        t1 = sd1.dst - sd1.src
        theta = angle(sd1.src, sd2.src) - angle(sd1.dst, sd2.dst)
        R_theta = numpy.matrix([
            [math.cos(theta), -math.sin(theta), 0],
            [math.sin(theta), math.cos(theta), 0],
            [0, 0, 1.0]])
        c = t1 - sd1.dst
        t = R_theta * numpy.matrix([[c.x()], [c.y()], [0]]) + numpy.matrix([[sd1.dst.x()], [sd1.dst.y()], [0]])
        t_point = QtCore.QPoint(t[0, 0], t[1, 0])
        return RigidTransformation(theta, t_point)


class EquationSystem(object):
    def __init__(self, n_rows, n_columns):
        self._eqs = []
        self._b = []
        self._n_columns = n_columns
        self._n_rows = n_rows

    def index(self, i, j):
        return i * self._n_columns + j

    def add_equation(self, index_coef_pairs, b_value):
        self._b.append(b_value)
        self._eqs.append(self._create_eq(index_coef_pairs))

    def _create_eq(self, index_coef):
        res = [0] * self._n_columns * self._n_rows
        for index, coef in index_coef:
            res[index] = coef
        return res

    def get_solution(self):
        assert len(self._eqs) == self._n_columns * self._n_rows
        m = numpy.matrix(self._eqs)
        b = numpy.matrix(self._b).T
        matrix = numpy.linalg.solve(m, b)
        return matrix.T.tolist()[0]


class SimilarityBuilder(MultiSrcDstBuilder):
    def __init__(self):
        super(SimilarityBuilder, self).__init__(2)

    def get_transformation(self):
        assert self.is_done()
        system = EquationSystem(3, 3)
        for sd in self._src_dst_pairs:
            for i, value in enumerate([sd.dst.x(), sd.dst.y()]):
                index_coef = [(system.index(i, 0), sd.src.x()), (system.index(i, 1), sd.src.y()),
                              (system.index(i, 2), 1)]
                system.add_equation(index_coef, value)
        system.add_equation([(system.index(0, 0), 1), (system.index(1, 1), -1)], 0)
        system.add_equation([(system.index(0, 1), 1), (system.index(1, 0), 1)], 0)
        system.add_equation([(system.index(2, 0), 1)], 0)
        system.add_equation([(system.index(2, 1), 1)], 0)
        system.add_equation([(system.index(2, 2), 1)], 1)

        solution = system.get_solution()
        a = solution[system.index(0, 0)]
        b = solution[system.index(1, 0)]
        tx = solution[system.index(0, 2)]
        ty = solution[system.index(1, 2)]
        # m = numpy.solution(numpy.zeros((3, 3)))
        # for i in xrange(3):
        #     for j in xrange(3):
        #         m[i, j] = solution[self._index(i, j)]
        return SimilarityTransformation(a, b, tx, ty)

    def legal_path(self, src):
        return AllLegalPath()


class AffineBuilder(MultiSrcDstBuilder):
    def __init__(self):
        super(AffineBuilder, self).__init__(3)

    def get_transformation(self):
        assert self.is_done()
        system = EquationSystem(3, 3)
        for sd in self._src_dst_pairs:
            for i, value in enumerate([sd.dst.x(), sd.dst.y()]):
                index_coef = [(system.index(i, 0), sd.src.x()), (system.index(i, 1), sd.src.y()),
                              (system.index(i, 2), 1)]
                system.add_equation(index_coef, value)
        system.add_equation([(system.index(2, 0), 1)], 0)
        system.add_equation([(system.index(2, 1), 1)], 0)
        system.add_equation([(system.index(2, 2), 1)], 1)

        solution = system.get_solution()
        a00 = solution[system.index(0, 0)]
        a01 = solution[system.index(0, 1)]
        a02 = solution[system.index(0, 2)]
        a10 = solution[system.index(1, 0)]
        a11 = solution[system.index(1, 1)]
        a12 = solution[system.index(1, 2)]
        return AffineTransformation(a00, a01, a02, a10, a11, a12)

    def legal_path(self, src):
        return AllLegalPath()


def angle(p1, p2):
    if p1.y() == p2.y():
        res = math.pi / 2.
    else:
        res = math.acos((p2.y() - p1.y()) / distance(p1, p2))
    if p1.x() > p2.x():
        res = 2 * math.pi - res
    return res


