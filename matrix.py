from copy import deepcopy
from numbers import Number
from typing import Optional, List


class Matrix:
    def __init__(self, data: Optional[List[List[Number]]]) -> None:
        self.data = data
        self.height = len(self.data)
        if self.data:
            self.width = len(self.data[0])
        else:
            self.width = 1

    @classmethod
    def zero(cls, n: int, m: int):
        data = [[0 for _ in range(m)] for _ in range(n)]
        return cls(data)

    @classmethod
    def identity(cls, n: int):
        data = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return cls(data)

    def copy(self):
        return deepcopy(self)

    def swap_rows(self, i: int, j: int):
        self.data[i], self.data[j] = self.data[j], self.data[i]
        return self

    def add_row(self, i: int, j: int, lamb: Number = 1):
        if lamb == 0:
            return self

        for col in range(self.width):
            self.data[i][col] += self.data[j][col] * lamb
        return self

    def multiply_row(self, i: int, lamb: Number):
        assert lamb != 0

        if lamb == 1:
            return self

        for col in range(self.width):
            self.data[i][col] *= lamb
        return self

    def gcd_rows(self, i: int, j: int, col: int):
        if i == j:
            return self
        if self.data[i][col] < 0:
            self.multiply_row(i, -1)
        if self.data[j][col] < 0:
            self.multiply_row(j, -1)
        while self.data[j][col] != 0:
            lamb = -(self.data[i][col] // self.data[j][col])
            self.add_row(i, j, lamb)
            self.swap_rows(i, j)
        return self

    def make_triangle(self):
        current = 0
        for col in range(self.width):
            for row in range(current + 1, self.height):
                self.gcd_rows(current, row, col)
            if self.data[current][col] == 0:
                continue
            current += 1
        return self

    def make_perfect(self):
        self.make_triangle()
        for i in range(self.height):
            for col in range(self.width):
                if self.data[i][col] == 0:
                    continue
                self.multiply_row(i, 1 / self.data[i][col])
                for j in range(self.height):
                    if i == j:
                        continue
                    self.add_row(j, i, -self.data[j][col])
                break
        return self

    def __matmul__(self, other):
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

    def _repr_latex_(self):
        rows = [' & '.join(map(str, self.data[row]))
                for row in range(self.height)]
        rows = [f'{row} \\\\\n' for row in rows]
        return (
            f'\\begin{{bmatrix}}\n'
            f'{"".join(rows)}\n'
            f'\\end{{bmatrix}}'
        )
