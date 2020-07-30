from fractions import Fraction
from random import randint


def matrix_multiplication(a, b):
    row = len(a)
    col = len(b[0])
    mid = len(a[0])
    c = [[0 for _ in range(col)] for _ in range(row)]
    for i in range(row):
        for j in range(col):
            for k in range(mid):
                c[i][j] += Fraction(a[i][k] * b[k][j])
    return c


x = [[randint(1, 5) for _ in range(10)] for _ in range(10)]
y = [[randint(1, 5) for _ in range(10)] for _ in range(10)]
print matrix_multiplication(x, y)
