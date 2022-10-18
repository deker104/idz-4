from __future__ import annotations
from typing import Sequence, List

from matrix import Matrix


class Polynom:
    def __init__(self: Polynom, matrices: Sequence[Matrix]):
        assert len(matrices) > 0

        self.matrices = [matrix for matrix in matrices]
        self.relax()

    def relax(self: Polynom) -> Polynom:
        while len(self.matrices) > 1 and self.matrices[-1].is_zero():
            self.matrices.pop()
        self.degree = len(self.matrices) - 1
        return self

    def copy(self: Polynom) -> Polynom:
        return Polynom([matrix.copy() for matrix in self.matrices])

    def __mul__(self: Polynom, other: Polynom) -> Polynom:
        size = self.matrices[0].height
        degree = self.degree + other.degree
        result = [Matrix.zero(size, size) for _ in range(degree + 1)]
        for i in range(self.degree + 1):
            for j in range(other.degree + 1):
                result[i + j] += self.matrices[i] @ self.matrices[j]
        return Polynom(result)

    def __add__(self: Polynom, other: Polynom) -> Polynom:
        lhs, rhs = self, other
        if rhs.degree > lhs.degree:
            lhs, rhs = rhs, lhs
        result = lhs.copy()
        for i in range(rhs.degree + 1):
            result.matrices[i] += other.matrices[i]
        return result

    def __sub__(self: Polynom, other: Polynom) -> Polynom:
        lhs, rhs = self, other
        if rhs.degree > lhs.degree:
            lhs, rhs = rhs, lhs
        result = lhs.copy()
        for i in range(rhs.degree + 1):
            result.matrices[i] -= other.matrices[i]
        return result

    def _repr_latex_(self: Polynom) -> str:
        result = ' + '.join(
            f'x^{i} {self.matrices[i]._repr_latex_()}' for i in range(self.degree + 1))
        return f'$${result}$$'
