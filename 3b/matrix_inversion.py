from fractions import Fraction
from random import randint


def matrix_inverse(matrix):
    size = len(matrix)
    inverse = [[Fraction(1) if i == j else Fraction(0) for j in range(size)] for i in range(size)]
    for i in range(size):
        diag = matrix[i][i]
        for j in range(size):
            matrix[i][j] = matrix[i][j] / diag
            inverse[i][j] = inverse[i][j] / diag
        for j in range(size):
            if i != j:
                multiplier = matrix[j][i]
                for k in range(size):
                    matrix[j][k] -= multiplier*matrix[i][k]
                    inverse[j][k] -= multiplier*inverse[i][k]
    return inverse


mat = [[randint(1, 5) for _ in range(10)] for _ in range(10)]
print matrix_inverse(mat)
