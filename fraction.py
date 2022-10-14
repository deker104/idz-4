from __future__ import annotations
from typing import Optional, Union

from utils import gcd, sign


Number = Union[int, 'Fraction']


class Fraction:
    def __init__(self: Fraction, numerator: Number, denomenator: Optional[Number]) -> None:
        self.numerator: int
        self.denomenator: int

        assert (denomenator != 0)

        if denomenator is None:
            if isinstance(numerator, int):
                self.numerator = numerator
                self.denomenator = 1
            elif isinstance(numerator, Fraction):
                self.numerator = numerator.numerator
                self.denomenator = numerator.denomenator
        elif isinstance(numerator, int) and isinstance(denomenator, int):
            if numerator == 0:
                self.numerator = 0
                self.denomenator = 1
            sgn = sign(numerator) * sign(denomenator)
            d = gcd(abs(numerator), abs(denomenator))
            self.numerator = sgn * abs(numerator) // d
            self.denomenator = abs(denomenator) // d
        else:
            result: Fraction = numerator / denomenator  # type: ignore
            self.numerator = result.numerator
            self.denomenator = result.denomenator

    def __truediv__(self: Fraction, other: Number) -> Fraction:
        if isinstance(other, int):
            return Fraction(self.numerator, self.denomenator * other)
        else:
            return Fraction(self.numerator * other.denomenator, self.denomenator * other.numerator)

    def __rtruediv__(self: Fraction, other: Number) -> Fraction:
        if isinstance(other, int):
            return Fraction(other * self.denomenator, self.numerator)
        else:
            return Fraction(other.numerator * self.denomenator, other.denomenator * self.numerator)

    def __mul__(self: Fraction, other: Number) -> Fraction:
        if isinstance(other, int):
            return Fraction(self.numerator * other, self.denomenator)
        else:
            return Fraction(self.numerator * other.numerator, self.denomenator * other.denomenator)

    def __rmul__(self: Fraction, other: Number) -> Fraction:
        return self * other

    def __add__(self: Fraction, other: Number) -> Fraction:
        if isinstance(other, int):
            return Fraction(self.numerator + other * self.denomenator, self.denomenator)
        else:
            return Fraction(
                self.numerator * other.denomenator + self.denomenator * other.numerator,
                self.denomenator * other.denomenator
            )

    def __radd__(self: Fraction, other: Number) -> Fraction:
        return self + other

    def __sub__(self: Fraction, other: Number) -> Fraction:
        return self + -other

    def __rsub__(self: Fraction, other: Number) -> Fraction:
        return -self + other

    def __neg__(self: Fraction) -> Fraction:
        return Fraction(-self.numerator, self.denomenator)

    def __lt__(self: Fraction, other: Number) -> bool:
        if isinstance(other, int):
            return self.numerator < other * self.denomenator
        else:
            return self.numerator * other.denomenator < other.numerator * self.denomenator

    def __eq__(self: Fraction, other: Number) -> bool:
        if isinstance(other, int):
            return self.numerator == other * self.denomenator
        else:
            return self.numerator * other.denomenator == other.numerator * self.denomenator

    def __repr__(self: Fraction) -> str:
        sgn = '' if self.numerator >= 0 else '-'
        if self.denomenator == 1:
            return f'{sgn}{abs(self.numerator)}'
        else:
            return f'{sgn}\\frac{{{abs(self.numerator)}}}{{{self.denomenator}}}'
