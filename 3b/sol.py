from fractions import Fraction, gcd


def solution(a):
    a = rearrange(a)
    for i in range(len(a)):
        outgoing = sum(a[i]) - a[i][i]
        d = sum(a[i])
        if outgoing != 0:
            a[i] = list(map(lambda x: Fraction(x, d), a[i]))
    q_dim = 0
    while sum(a[q_dim]) - a[q_dim][q_dim]:
        q_dim += 1
    q, r = [], []
    for i in range(q_dim):
        q.append(list(map(Fraction, a[i][:q_dim])))
        r.append(list(map(Fraction, a[i][q_dim:])))
    for i in range(q_dim):
        for j in range(q_dim):
            if i == j:
                q[i][j] = 1 - q[i][j]
            else:
                q[i][j] = - q[i][j]
    n = matrix_inverse(q)
    m = matrix_multiplication(n, r)
    m = m[0]
    lcm = 1
    for num in m:
        lcm = lcm * num.denominator // gcd(lcm, num.denominator)
    answer = []
    for num in m:
        answer.append(num.numerator * lcm // num.denominator)
    answer.append(lcm)
    return answer


def matrix_multiplication(a, b):
    """

    """
    row = len(a)
    col = len(b[0])
    mid = len(a[0])
    c = [[0 for _ in range(col)] for _ in range(row)]
    for i in range(row):
        for j in range(col):
            for k in range(mid):
                c[i][j] += a[i][k] * b[k][j]
    return c


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


def rearrange(s):
    for i in range(len(s) - 1, 0, -1):
        if sum(s[i]) - s[i][i] != 0:
            for j in range(i - 1, 0, -1):
                if sum(s[j]) - s[j][j] == 0:
                    temp = s[i]
                    s[i] = s[j]
                    s[j] = temp
                    for row in s:
                        temp = row[i]
                        row[i] = row[j]
                        row[j] = temp
    return s


st = [
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

st = [
    [0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [4, 3, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]
print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]))
print(solution(st))
print(rearrange(st))
