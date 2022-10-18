from __future__ import annotations
from typing import Optional, Sequence, Type, List

from fraction import Fraction, Number


class Matrix:
    def __init__(self: Matrix, data: Optional[Sequence[Sequence[Number]]]) -> None:
        self.data: List[List[Number]]
        self.height: int
        self.width: int

        if data is None:
            self.data = []
            self.height = 0
            self.width = 0
            return
        self.height = len(data)
        if data:
            self.width = len(data[0])
        else:
            self.width = 0
        self.data = [[data[row][col]
                      for col in range(self.width)] for row in range(self.height)]

    @classmethod
    def zero(cls: Type[Matrix], n: int, m: int) -> Matrix:
        data = [[0 for _ in range(m)] for _ in range(n)]
        return cls(data)

    @classmethod
    def identity(cls: Type[Matrix], n: int) -> Matrix:
        data = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return cls(data)

    def copy(self: Matrix) -> Matrix:
        return type(self)(self.data.copy())

    def swap_rows(self: Matrix, i: int, j: int) -> Matrix:
        self.data[i], self.data[j] = self.data[j], self.data[i]
        return self

    def add_row(self: Matrix, i: int, j: int, lamb: Number = 1) -> Matrix:
        if lamb == 0:
            return self

        for col in range(self.width):
            self.data[i][col] += self.data[j][col] * lamb
        return self

    def multiply_row(self: Matrix, i: int, lamb: Number) -> Matrix:
        assert lamb != 0

        if lamb == 1:
            return self

        for col in range(self.width):
            self.data[i][col] *= lamb
        return self

    def gcd_rows(self: Matrix, i: int, j: int, col: int) -> Matrix:
        if i == j:
            return self
        if self.data[i][col] < 0:
            self.multiply_row(i, -1)
        if self.data[j][col] < 0:
            self.multiply_row(j, -1)
        while self.data[j][col] != 0:
            lamb = -(Fraction(self.data[i][col], self.data[j][col]))
            self.add_row(i, j, lamb)
            self.swap_rows(i, j)
        return self

    def make_triangle(self: Matrix) -> Matrix:
        current = 0
        for col in range(self.width):
            for row in range(current + 1, self.height):
                self.gcd_rows(current, row, col)
            if self.data[current][col] == 0:
                continue
            current += 1
            if current == self.height:
                break
        return self

    def make_perfect(self: Matrix) -> Matrix:
        self.make_triangle()
        for i in range(self.height):
            for col in range(self.width):
                if self.data[i][col] == 0:
                    continue
                self.multiply_row(i, Fraction(1, self.data[i][col]))
                for j in range(self.height):
                    if i == j:
                        continue
                    self.add_row(j, i, -self.data[j][col])
                break
        return self

    def is_zero(self: Matrix) -> bool:
        return all(self.data[row][col] == 0 for row in range(self.height) for col in range(self.width))

    def is_identity(self: Matrix) -> Optional[Number]:
        const: Optional[Number] = None
        for row in range(self.height):
            for col in range(self.width):
                if row == col:
                    if const is None or self.data[row][col] == const:
                        const = self.data[row][col]
                    else:
                        return None
                else:
                    if self.data[row][col] != 0:
                        return None
        return const

    def __imul__(self: Matrix, other: Number) -> Matrix:
        for row in range(self.height):
            for col in range(self.width):
                self.data[row][col] *= other
        return self

    def __mul__(self: Matrix, other: Number) -> Matrix:
        result = self.copy()
        result *= other
        return result

    def __rmul__(self: Matrix, other: Number) -> Matrix:
        return self * other

    def __matmul__(self: Matrix, other: Matrix) -> Matrix:
        assert self.width == other.height

        n, k = self.height, self.width
        m = other.width
        result = Matrix.zero(n, m)
        for mid in range(k):
            for row in range(n):
                for col in range(m):
                    result.data[row][col] += (self.data[row][mid] *
                                              other.data[mid][col])
        return result

    def __iadd__(self: Matrix, other: Matrix) -> Matrix:
        assert self.height == other.height
        assert self.width == other.width

        for row in range(self.height):
            for col in range(self.width):
                self.data[row][col] += other.data[row][col]
        return self

    def __add__(self: Matrix, other: Matrix) -> Matrix:
        result = self.copy()
        result += other
        return result

    def __isub__(self: Matrix, other: Matrix) -> Matrix:
        assert self.height == other.height
        assert self.width == other.width

        for row in range(self.height):
            for col in range(self.width):
                self.data[row][col] -= other.data[row][col]
        return self

    def __sub__(self: Matrix, other: Matrix) -> Matrix:
        result = self.copy()
        result -= other
        return result

    def _repr_latex_(self: Matrix) -> str:
        rows = [' & '.join(map(str, self.data[row]))
                for row in range(self.height)]
        rows = [f'{row} \\\\\n' for row in rows]
        return (
            f'\\begin{{bmatrix}}\n'
            f'{"".join(rows)}\n'
            f'\\end{{bmatrix}}'
        )
