"""
This is a very interesting problem. The crux of the problem can be described as follows.
The situation can be described through a directed weighted (possibly negative) graph, and the solution to the
problem can be computed by finding a walk in that graph starting at a particular source vertex and end at a particular
sink vertex and visit as many vertices as possible while keeping the weight of the walk within limit.

As there could multiple paths possible between any two vertices, we should find ordered-pair wise shortest distances.
And everytime we needed to traverse between any two vertices, we should use this shortest distance to minimize
the weight.
For this we're using Floyd-Warshall algorithm.

Another interesting aspect is, there could be some cycles with negative weights. So these cycles can be used to decrease
the total weight by sufficient amount to visit all the vertices while remaining within weight limit.
This essentially means that if there are negative cycles, then we can visit all the vertices.
After applying Floyd-Warshall algorithm, if there is a negative cycle containing come vertex v, then it will be computed
that distance from v to v is negative (through the most negative cycle).
So Floyd-Warshall would also detect the negative cycles.

If there aren't any negative cycles, then there could be a limit on how many vertices we can visit.
Here this is done by brute force method of examining all the possible number and sequences of vertices.
"""
from itertools import permutations


def solution(dist, limit):
    """
    Find out the intermediate vertices that can be visited by a walk while staying within the weight limit.
    :param dist: edge weight matrix.
    :param limit: limit applied on weight.
    :return: sorted list of intermediate vertices that can be visited through a walk while being within the weight limit
    """
    n = len(dist)
    # Floyd-Warshall algorithm.
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Check for negative cycles.
    bunny_ids = [i for i in range(n - 2)]
    for i in range(n):
        if dist[i][i] < 0:
            return bunny_ids

    # Check each possible combination and permutation for all intermediate vertices.
    for r in range(n - 2, -1, -1):
        for seq in permutations(bunny_ids, r):
            if bunnies_sequence_is_valid(seq, dist, limit):
                seq = list(seq)
                seq.sort()
                return seq
    return []


def bunnies_sequence_is_valid(seq, dist, limit):
    """
    Check if the provided intermediate vertices sequence results in a walk whose weight is within the limit.
    :param seq: sequence of intermediate vertices to visit.
    :param dist: shortest distance matrix for every ordered-pair of vertices.
    :param limit: limit applied on weight
    :return: True if it's possible to visit all the intermediate vertices in that order through a walk while staying
    within the weight limit. False otherwise.
    """
    last = 0
    for i in seq:
        limit -= dist[last][i + 1]
        last = i + 1
    limit -= dist[last][len(dist) - 1]
    return limit >= 0
