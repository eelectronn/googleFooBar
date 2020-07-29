"""
There are several path finding algorithms to consider. Due to the maze like structure, we can opt for a-star algorithm.

Beginning from the starting cell, for any cell (i, j) we consider each of its unvisited neighbour n and compute f_score,
where f_score[n] = g_score[n] + h(n, end)
Here g_score is the shortest distance to n from the start, (in our case, g_score[n] = g_score[(i, j)] + 1)
and h(n, end) is heuristic functions that estimate the length of shortest path from n to end.
Terminate when we reach the end and g_score of the end is our answer.

Now there needs to be a few modifications to account for the wall breaking.

To put the approach in simple words, it resembles to following:
Imagine two copy of grid stacked together (one on top of the other).
We start at (0, 0) on the top layer and traverse using the a-star algorithm, we move around on the top grid as long as
we are traversing through open paths (not breaking any wall). However, when we do get to the point where we have
to break a wall, we break the wall and at the same time move to the bottom grid. Once we are in the bottom grid,
we're only allowed to move through the open paths, we're not allowed to break any walls anymore and
we also cannot go back to the top grid.
Moving in this fashion, we have to get to the (0, 0) of either top grid or the bottom grid, and find out which one is
shorter. If (0, 0) of the bottom grid gives the shorter path, then it means we can get to the end point faster after
breaking one wall, as compared to not breaking any wall.

A little more technical description:
Take the original gird, make its copy and stack them, one on top of the other such that the corresponding positions
line up.
Call the index of top grid 0 and the index of the bottom grid 1.
Each cell will now be identified with 3-tuple. First two co-ordinates would be the row and column index respectively,
and the third co-ordinate will be either 0 (top) or 1 (bottom).
Edges:
No edges will be added between nodes that are not cardinally adjacent.
For any nodes a = (i, j, 0 or 1 resp.) and b = (x, y, 0 or 1 resp.) such that (i, j) and (x, y) are cardinally adjacent
in the original grid.
    For both the 0th and 1st grid individually, add an edge between a and b if a = b = 0
    For 1st grid add a directed edge from a to b if (a = 1 and b = 0) and from b to a if (b = 1 and a = 0).
For any node a = (i, j, 0) and b = (x, y, 1) where (i, j) and (x, y) are cardinally adjacent in the original grid.
    We add a directed edge from a to b if a = 0 and b = 1

As we can see for any edge between a node of the top layer and a node of the bottom layer is always in the direction
from the top to the bottom. So when traversing this graph, once we move from the top layer to the bottom layer
thorough one of these edges, we cannot go back to the top layer.
Similarly, there are no edges in bottom layer that leads from 0 to 1, so we cannot break any wall once in
the bottom layer.

We start at the (0, 0, 0) and traverse using the a-star algorithm and find
the shortest path to (h-1, w-1, 0) and (h-1, w-1, 1) and minimum of those path would be the answer.

This can be extended to allow for breaking k walls, by stacking k + 1 grids and adding edges between them as mentioned
above, and finding shortest path between (0, 0, 0) and (h-1, w-1, t) for 0 <= t <= k and the minimum of those would be
the answer.

Note:
Having the graph structure stated above, the only time when are concerned about the edges in the graph is when we are
iterating over the neighbours of any node (as part of the a-star algorithm). Therefore, we don't need to have an
implementation of data structure of such graph structure. Instead we just have a function called get_neighbours that
iterate over all possible cardinally adjacent neighbour of a given node and only return a list of neighbours that
are consistent with the edges description given above. This lets us work with the above structure without implementing
the actual data structure and hence, simplify the program a little bit.
"""
from Queue import PriorityQueue
from itertools import product


def solution(a, k=1):
    """
    Iterate over distances from (0, 0, 0) to (h-1, w-1, i) for 0 <= i <= k and return the minimum of those.
    :param a: original grid.
    :param k: maximum number of walls breaking that is allowed.
    :return: shortest distance to to get to (h-1, w-1) from (0, 0) in grid a after breaking at most k walls.
    """
    h = len(a)
    w = len(a[0])
    st = (0, 0, 0) if a[0][0] == 0 else (0, 0, 1)
    distance = h * w + 1
    for i in range(0, k + 1):
        distance = min(distance, a_star(a, k, st, (h - 1, w - 1, i)))
    return distance


def a_star(a, k, st, en):
    """
    A star algorithm as described above.
    :param a: grid
    :param k: number of walls that could be broken
    :param st: starting point in the grid
    :param en: ending point in the grid
    :return: shortest distance between st and en after breaking at most k walls.
    """
    h, w, ent = en[0] + 1, en[1] + 1, en[2]
    opn = PriorityQueue()
    # came_from = dict()
    g_score = {node: 500 for node in product(range(h), range(w), range(k + 1))}
    g_score[st] = 1
    f_score = {node: 500 for node in product(range(h), range(w), range(k + 1))}
    f_score[st] = heuristics(st, en)
    opn.put((f_score[st], st))
    while opn.qsize() > 0:
        curr = opn.get()[1]
        if curr == en:
            return g_score[en]
        neighbour_hood = get_neighbours(curr, a, k)
        for neighbour in neighbour_hood:
            temp_g_score = g_score[curr] + 1
            if temp_g_score < g_score[neighbour]:
                # came_from[neighbour] = curr
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = g_score[neighbour] + heuristics(neighbour, en)
                opn.put((f_score[neighbour], neighbour))
    return h * w + 1


def get_neighbours(node, a, k):
    """
    For a given node in grid a and maximum possible walls that can be broken into, it returns a list of
    all the neighbours of the given node as per the graph structure mentioned at the beginning of the file.
    :param node: node whose neighbours are to be found.
    :param a: grid
    :param k: number of walls that could be broken
    :return: a list of all the neighbours of the given node as per the graph structure mentioned at the beginning of
    the file.
    """
    i, j, t = node
    h, w = len(a), len(a[0])
    neighbours = []
    n = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    for y, x in n:
        if is_valid(i + y, j + x, h, w):
            if a[i + y][j + x] == 0:
                neighbours.append((i + y, j + x, t))
            else:
                if t != k:
                    neighbours.append((i + y, j + x, t + 1))
    return neighbours


def is_valid(i, j, h, w):
    """
    check if i, j is bounded within grid of dimension h times w.
    :param i: row index
    :param j: col index
    :param h: height of grid
    :param w: width of grid
    :return: True if i, j is bounded within grid of dimension h times w. False otherwise.
    """
    return -1 < i < h and -1 < j < w


def heuristics(st, en):
    """
    Heuristics function that gives Manhattan distance between st and en
    :param st: starting point
    :param en: ending point
    :return: Manhattan distance
    """
    i, j, t = st
    h, w, ent = en
    return abs(h - i) + abs(w - j) + abs(ent - t)
