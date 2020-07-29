from Queue import PriorityQueue
from itertools import product
from math import sqrt, ceil


def solution(a):
    h = len(a)
    w = len(a[0])
    st = i, j = (0, 0)
    return a_star(a, st, h, w)


def a_star(a, st, h, w):
    en = h - 1, w - 1

    opn = PriorityQueue()
    cls = set()

    came_from = dict()

    g_score = {node: [500, 500] for node in product(range(h), range(w))}
    g_score[st] = [1, 1]

    f_score = {node: 500 for node in product(range(h), range(w))}
    f_score[st] = 1 + heuristics(st, h, w)

    opn.put((f_score[st], 0, st))
    while opn.qsize() > 0:
        f, wall_broken, curr = opn.get()
        cls.add(curr)
        if curr == en:
            return min(g_score[en][0], g_score[en][1])
        for neighbour in get_neighbours(curr, h, w):
            if neighbour not in cls:
                i, j = neighbour
                if a[i][j] == 0:
                    temp_g_score = g_score[curr][wall_broken] + 1
                    if temp_g_score < g_score[neighbour][wall_broken]:
                        came_from[neighbour] = curr
                        g_score[neighbour][wall_broken] = temp_g_score
                        f_score[neighbour] = g_score[neighbour][wall_broken] + heuristics(neighbour, h, w)
                        opn.put((f_score[neighbour], wall_broken, neighbour))
                elif a[i][j] == 1 and wall_broken == 0:
                    temp_g_score = g_score[curr][wall_broken] + 1
                    if temp_g_score < g_score[neighbour][1]:
                        came_from[neighbour] = curr
                        g_score[neighbour][1] = temp_g_score
                        f_score[neighbour] = g_score[neighbour][1] + heuristics(neighbour, h, w)
                        opn.put((f_score[neighbour], 1, neighbour))
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


def heuristics(node, h, w):
    i, j = node
    return ceil(sqrt((h - i) ** 2 + (w - j) ** 2))


s = solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]])

# s = solution([
#     [0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 0],
#     [0, 0, 0, 1, 0],
#     [1, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0]
# ])

# node = (3, 3)
# print(node)
# distance = 1
# while node != (0, 0):
#     distance += 1
#     print(s[node])
#     node = s[node]
# print(distance)

print(s)
