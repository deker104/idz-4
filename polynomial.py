from __future__ import annotations
from typing import List, Sequence, Union

from fraction import Fraction, Number
from matrix import Matrix


class Polynomial:
    def __init__(self: Polynomial, matrices: Sequence[Matrix], symbol: str = 'x'):
        assert len(matrices) > 0

        self.symbol = symbol
        self.matrices = [matrix for matrix in matrices]
        self.relax()

    def relax(self: Polynomial) -> Polynomial:
        while len(self.matrices) > 1 and self.matrices[-1].is_zero():
            self.matrices.pop()
        self.degree = len(self.matrices) - 1
        return self

    def copy(self: Polynomial) -> Polynomial:
        return Polynomial([matrix.copy() for matrix in self.matrices], self.symbol)

    def __mul__(self: Polynomial, other: Union[Polynomial, Number]) -> Polynomial:
        if isinstance(other, int) or isinstance(other, Fraction):
            result = self.copy()
            for matrix in result.matrices:
                matrix *= other
            return result.relax()
        else:
            size = self.matrices[0].height
            degree = self.degree + other.degree
            matrices = [Matrix.zero(size, size) for _ in range(degree + 1)]
            for i in range(self.degree + 1):
                for j in range(other.degree + 1):
                    matrices[i + j] += self.matrices[i] @ self.matrices[j]
            return Polynomial(matrices, self.symbol)

    def __rmul__(self: Polynomial, other: Union[Polynomial, Number]) -> Polynomial:
        return self * other

    def __add__(self: Polynomial, other: Polynomial) -> Polynomial:
        lhs, rhs = self, other
        if rhs.degree > lhs.degree:
            lhs, rhs = rhs, lhs
        result = lhs.copy()
        for i in range(rhs.degree + 1):
            result.matrices[i] += rhs.matrices[i]
        return result

    def __sub__(self: Polynomial, other: Polynomial) -> Polynomial:
        lhs, rhs = self, other
        if rhs.degree > lhs.degree:
            lhs, rhs = rhs, lhs
        result = lhs.copy()
        for i in range(rhs.degree + 1):
            result.matrices[i] -= other.matrices[i]
        return result

    def _repr_latex_(self: Polynomial) -> str:
        rows = []
        for i in range(self.degree + 1):
            if self.matrices[i].is_zero():
                continue
            term = ''
            term += self.matrices[i]._repr_latex_()
            if i == 0:
                pass
            elif i == 1:
                term += self.symbol
            else:
                term += f'{self.symbol}^{i}'
            rows.append(term)
        if not rows:
            return '$0$'
        return f'$${" + ".join(rows)}$$'
