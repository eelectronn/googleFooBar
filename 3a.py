from Queue import PriorityQueue


def solution(a):
    h = len(a)
    w = len(a[0])
    state = [[[500, 500] for _ in range(w)] for _ in range(h)]
    state[0][0][0] = state[0][0][1] = 1
    opn = PriorityQueue()
    cls = set()
    i, j = 0, 0
    wall_broken = 0
    distance = 1
    opn.put((heuristic(i, j, h, w), 1, wall_broken, i, j))
    while opn.qsize() > 0:
        score, distance, wall_broken, i, j = opn.get()
        neighbours = get_neighbours(i, j, h, w)
        for y, x in neighbours:
            if (y, x) not in cls:
                if a[y][x] == 0:
                    n_score = distance + heuristic(y, x, h, w)
                    if n_score < state[y][x][wall_broken]:
                        state[y][x][wall_broken] = n_score
                        opn.put((n_score, distance + 1, wall_broken, y, x))
                elif a[y][x] == 1 and wall_broken == 0:
                    n_score = distance + heuristic(y, x, h, w)
                    if n_score < state[y][x][1]:
                        state[y][x][1] = n_score
                        opn.put((n_score, distance + 1, 1, y, x))
        cls.add((i, j))
    print(state[h - 1][w - 1])
    return min(state[h - 1][w - 1][0], state[h - 1][w - 1][1])


def heuristic(i, j, h, w):
    return h - i + w - j - 1


def get_neighbours(i, j, h, w):
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


# maze = [
#     [0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 0],
#     [0, 0, 0, 1, 0],
#     [1, 1, 1, 0, 0],
#     [1, 1, 1, 0, 1],
#     [1, 1, 1, 0, 0]
# ]

maze = [
    [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
]

print(solution(maze))
