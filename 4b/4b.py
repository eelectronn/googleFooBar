from math import sqrt
from Queue import PriorityQueue
from fractions import gcd


def solution(dim, a, b, limit):
    a = (a[0], a[1])
    b = (b[0], b[1])
    ref_a, ref_b, ref_b_radial = get_reflection_points(dim, a, b, limit)
    lines = get_lines(a, ref_a, ref_b)
    attacks = find_attacks(*lines)
    return attacks


def find_attacks(lines_a, lines_b):
    attacks = 0
    for line in lines_b:
        if line in lines_a:
            if lines_a[line][0] > lines_b[line][0]:
                attacks += 1
        else:
            attacks += 1
    return attacks


def get_lines(a, ref_a, ref_b):
    lines_a = dict()
    lines_b = dict()
    for a_r in ref_a:
        if a_r != a:
            dist = get_distance(a, a_r)
            line = find_line(a, a_r)
            if line in lines_a:
                if dist < lines_a[line][0]:
                    lines_a[line] = (dist, a_r)
            else:
                lines_a[line] = (dist, a_r)
    for b_r in ref_b:
        dist = get_distance(a, b_r)
        line = find_line(a, b_r)
        if line in lines_b:
            if dist < lines_b[line][0]:
                lines_b[line] = (dist, b_r)
        else:
            lines_b[line] = (dist, b_r)
    return lines_a, lines_b


def find_lines(a, ref_a, ref_b, ref_b_radial):
    seen = set()
    possible = set()
    while ref_b_radial.qsize():
        d, b = ref_b_radial.get()
        line = find_line(a, b)
        if line not in seen:
            if not incidence_with_reflection_of_a(a, b, line, ref_a):
                possible.add(line)
            seen.add(line)
    return possible


def incidence_with_reflection_of_a(a, b, line, ref_a):
    for ra in ref_a:
        not_original_a = ra != a
        x_within_bound = a[0] <= ra[0] <= b[0] or b[0] <= ra[0] <= a[0]
        y_within_bound = a[1] <= ra[1] <= b[1] or b[1] <= ra[1] <= a[1]
        if not_original_a and x_within_bound and y_within_bound:
            if fall_on_line(line, ra):
                return True
    return False


def fall_on_line(line, pt):
    return line[0] * pt[0] + line[1] * pt[1] + line[2] == 0


def find_line(p1, p2):
    a = p2[1] - p1[1]
    b = p1[0] - p2[0]
    c = p1[1] * (p2[0] - p1[0]) - p1[0] * (p2[1] - p1[1])
    g = gcd(abs(a), gcd(abs(b), abs(c)))
    a, b, c = a // g, b //g, c // g
    return a, b, c


def get_reflection_points(dim, a, b, limit):
    ref_a = set()
    ref_b = set()
    ref_b_radial = PriorityQueue()
    quad_params = [
        [0, 0, 1, 1],
        [-1, 0, -1, 1],
        [-1, -1, -1, -1],
        [0, -1, 1, -1]
    ]
    for p in quad_params:
        add_reflection_points(dim, a, b, limit, ref_a, ref_b, ref_b_radial, *p)
    return ref_a, ref_b, ref_b_radial


def add_reflection_points(dim, a, b, limit, ref_a, ref_b, ref_b_radial, x_start, y_start, x_inc, y_inc):
    dim_x, dim_y = dim
    too_far_x = False
    x = x_start
    while not too_far_x:
        too_far_y = False
        y = y_start
        while not too_far_y:
            box_x, box_y = x * dim_x, y * dim_y
            offset_x_a, offset_y_a = get_offsets(a, x, y, dim)
            offset_x_b, offset_y_b = get_offsets(b, x, y, dim)
            a_r = (box_x + offset_x_a, box_y + offset_y_a)
            b_r = (box_x + offset_x_b, box_y + offset_y_b)
            check_bounds = [check_limit(a, a_r, limit), check_limit(a, b_r, limit)]
            if not any(check_bounds) and y == y_start:
                too_far_y = too_far_x = True
            elif not any(check_bounds):
                too_far_y = True
            else:
                if check_bounds[0]:
                    ref_a.add(a_r)
                if check_bounds[1]:
                    ref_b.add(b_r)
                    ref_b_radial.put((get_distance(a, b_r), b_r))
            y += y_inc
        x += x_inc


def get_offsets(point, x, y, dim):
    offset_x = point[0] if x % 2 == 0 else dim[0] - point[0]
    offset_y = point[1] if y % 2 == 0 else dim[1] - point[1]
    return offset_x, offset_y


def get_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def check_limit(p1, p2, limit):
    return get_distance(p1, p2) <= limit


at = solution([42, 59], [34, 44], [6, 34], 5000)
print(at)

