from typing import Literal


def sign(x: int) -> Literal[-1, 1]:
    if x >= 0:
        return 1
    else:
        return -1


def gcd(x: int, y: int) -> int:
    if y == 0:
        return x
    return gcd(y, x % y)
