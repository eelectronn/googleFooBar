def solution(a):
    visited = [[False for _ in range(len(a[0]))] for _ in range(len(a))]
    n = {
        'e': (0, 1),
        'w': (0, -1),
        'n': (-1, 0),
        's': (1, 0)
    }
    memo = dict()
    d = solve(a, 0, 0, visited, False, n, memo)
    return d


def solve(a, i, j, visited, wall_broken, n, memo):
    if i == len(a) - 1 and j == len(a[0]) - 1:
        return 1
    if (i, j, wall_broken) in memo:
        return memo[(i, j, wall_broken)]
    neighbours = get_neighbours(i, j, n, a)
    distance = 400
    for y, x in neighbours:
        if not visited[y][x]:
            if a[y][x] == 0 or (a[y][x] == 1 and not wall_broken):
                visited[y][x] = True
                if a[y][x] == 1:
                    wall_broken = True
                distance = min(solve(a, y, x, visited, wall_broken, n, memo), distance)
                if a[y][x] == 1:
                    wall_broken = False
                visited[y][x] = False
    memo[(i, j, wall_broken)] = distance + 1
    return distance + 1


def get_neighbours(i, j, n, a):
    neighbour = []
    for y, x in n.values():
        if is_valid(i + y, j + x, len(a), len(a[0])):
            neighbour.append((i + y, j + x))
    return neighbour


def is_valid(i, j, w, h):
    return -1 < i < h and -1 < j < w


print(solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]))
