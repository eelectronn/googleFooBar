from Queue import PriorityQueue
from itertools import product


def solution(a):
    h = len(a)
    w = len(a[0])
    st = i, j = (0, 0)
    distance = a_star(a, st, h, w)
    for i in range(h):
        for j in range(w):
            if a[i][j] == 1:
                a[i][j] = 0
                distance = min(distance, a_star(a, st, h, w))
                a[i][j] = 1
    return distance


def a_star(a, st, h, w):
    en = h - 1, w - 1

    opn = PriorityQueue()

    came_from = dict()

    g_score = {node: 500 for node in product(range(h), range(w))}
    g_score[st] = 1

    f_score = {node: 500 for node in product(range(h), range(w))}
    f_score[st] = heuristics(st, h, w)

    opn.put((f_score[st], st))
    while opn.qsize() > 0:
        curr = opn.get()[1]
        if curr == en:
            return g_score[en]
        for neighbour in get_neighbours(curr, h, w):
            i, j = neighbour
            if a[i][j] == 0:
                temp_g_score = g_score[curr] + 1
                if temp_g_score < g_score[neighbour]:
                    came_from[neighbour] = curr
                    g_score[neighbour] = temp_g_score
                    f_score[neighbour] = g_score[neighbour] + heuristics(neighbour, h, w)
                    opn.put((f_score[neighbour], neighbour))
    return 'impossible'


def get_neighbours(node, h, w):
    i, j = node
    neighbour = []
    n = {
        'e': (0, 1),
        'w': (0, -1),
        'n': (-1, 0),
        's': (1, 0)
    }
    for y, x in n.values():
        if is_valid(i + y, j + x, h, w):
            neighbour.append((i + y, j + x))
    return neighbour


def is_valid(i, j, h, w):
    return -1 < i < h and -1 < j < w


def heuristics(st, h, w):
    i, j = st
    return (h - i) ** 2 + (w - j) ** 2
