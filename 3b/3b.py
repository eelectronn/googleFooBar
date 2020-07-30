"""
For this problem I had to read some theory online about the absorbing Markov chains.
Absorbing Markov chain consists of set of states, and for every pair of states 1 and 2, there is an assigned
probability to change to state 2 from state 1. There has to be at least one state t such that probability to go
from state t to any other state s is 0. Such a state is called a terminal state. State that are not terminal state are
called non-terminal state. If we start from any non-terminal state s, it should always be possible to reach a at least
one of the terminal state in finite number of steps.

The given problem fits exactly in the absorbing Markov chain model as described above.

The information about the state change can be captured in a square matrix P where rows and columns are labelled with
state in the same order and any entry i,j in matrix is equal to the probability of changing from state i to state j in
one step.
In P^n, then i,j entry in P^n is equal to the probability of changing from state i to state j in n steps.
As n approaches infinity, P^n approach some matrix A.
To answer the question, we need to find this matrix A and see the probability of ending up in each of the terminal state
from state 0 after sufficiently large number of steps.

There is some theory to compute such a limiting matrix A without actually multiplying P infinitely many times.
We take P and reorder the state in row and column, to make sure that all the terminal states are at the bottom in the
rows and to the right in the columns. Again the order of states label should be same on rows and columns from top to
bottom and left to right respectively.

Lets say there are t terminal states and l non-terminal state. After arranging the matrix as
mentioned above, we form two sub-matrix out of P. We set Q = the l x l matrix in the top left corner of P.
We set R = the l x t matrix in the top right corner of P.
Now we compute a matrix N = (I - Q)^(-1).
Following that, we compute M = NxR
Now M is a part of the matrix A, but we don't need to get the entire matrix A, as just having M is sufficient for the
solution of our problem. In matrix M, the 0th row precisely contains the probabilities of starting at state 0 and
reaching to each of the terminal state in that order upon sufficiently large number of steps.
That is exactly what we need for our answer.

I've looked up this method at the following site:
https://brilliant.org/wiki/absorbing-markov-chains/
Furthermore, I've looked up the justification for the correctness of the above method at the following site:
http://math.colgate.edu/~wweckesser/math312Spring05/handouts/MarkovChains.pdf
"""
from fractions import Fraction, gcd


def solution(a):
    """
    Takes in the input matrix and call the appropriate sequence of function to solve the problem.
    :param a: input matrix
    """
    if len(a) == 1:
        return [1, 1]
    a, q_dim = rearrange(a)
    q, r = get_q_and_r(a, q_dim)
    n = matrix_inverse(subtract_from_identity(q))
    m = matrix_multiplication(n, r)
    return get_final_answer(m[0])


def get_final_answer(m):
    """
    Convert the array or probability to final answer with numerator and denominator separated as required.
    :param m: Array of probability
    :return: Array of probability with numerator and denominator separated.
    """
    lcm = 1
    for num in m:
        lcm = lcm * num.denominator // gcd(lcm, num.denominator)
    ans = []
    for num in m:
        ans.append(num.numerator * lcm // num.denominator)
    ans.append(lcm)
    return ans


def matrix_multiplication(a, b):
    """
    Multiply matrix a and b
    :param a: matrix a
    :param b: matrix b
    :return: multiplication of a and b
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
    """
    Invert the matrix.
    :param matrix: matrix to be inverted.
    :return: the inverse of the matrix.
    """
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


def subtract_from_identity(q):
    """
    Subtract matrix q from identity
    :param q: Matrix q
    :return: I - q
    """
    size = len(q)
    for i in range(size):
        for j in range(size):
            q[i][j] = 1 - q[i][j] if i == j else -q[i][j]
    return q


def rearrange(a):
    """
    Rearrange the original input matrix to order the states such that all the terminal state occur after all the
    non-terminal state, in a way that the order of occurrence of terminal states and non-terminal state are maintained
    after separation.
    :param a: original input matrix
    :return: rearranged matrix
    """
    size = len(a)
    rearranged = [[0 for _ in range(size)] for _ in range(size)]
    non_terminal = []
    terminal = []
    for i in range(size):
        if sum(a[i]) - a[i][i] == 0:
            terminal.append(i)
        else:
            non_terminal.append(i)
    order = non_terminal + terminal
    for i in range(size):
        for j in range(size):
            rearranged[i][j] = a[order[i]][order[j]]
    return rearranged, len(non_terminal)


def get_q_and_r(a, q_dim):
    """
    Take the rearranges matrix and extract matrix q and r and convert all the frequency to probability in form of
    fraction.
    :param a: rearranged matrix
    :param q_dim: dimension of q matrix
    :return: matrix q and r.
    """
    q, r = [], []
    for i in range(q_dim):
        d = sum(a[i])
        q.append(list(map(lambda x: Fraction(x, d), a[i][:q_dim])))
        r.append(list(map(lambda x: Fraction(x, d), a[i][q_dim:])))
    return q, r
