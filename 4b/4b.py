from math import sqrt
from Queue import PriorityQueue


def solution(dim, a, b, limit):
    return get_reflection_points(dim, a, b, limit)


def get_reflection_points(dim, a, b, limit):
    dim_x, dim_y = dim
    ref_a = set()
    ref_b = set()
    ref_b_radial = PriorityQueue()
    add_reflection_points(dim, a, b, limit, ref_a, ref_b, ref_b_radial)
    return ref_a, ref_b, ref_b_radial


def add_reflection_points(dim, a, b, limit, ref_a, ref_b, ref_b_radial):
    dim_x, dim_y = dim
    too_far_x = False
    x = 0
    while not too_far_x:
        too_far_y = False
        y = 0
        while not too_far_y:
            box_x, box_y = x * dim_x, y * dim_y
            offset_x_a, offset_y_a = get_offsets(a, x, y, dim)
            offset_x_b, offset_y_b = get_offsets(b, x, y, dim)
            a_r = (box_x + offset_x_a, box_y + offset_y_a)
            b_r = (box_x + offset_x_b, box_y + offset_y_b)
            check_bounds = [check_limit(a, a_r, limit), check_limit(a, b_r, limit)]
            if not any(check_bounds) and y == 0:
                too_far_y = too_far_x = True
            elif not any(check_bounds):
                too_far_y = True
            else:
                if check_bounds[0]:
                    ref_a.add(a_r)
                if check_bounds[1]:
                    ref_b.add(b_r)
                    ref_b_radial.put((get_distance(a, b_r), b_r))
            y += 1
        x += 1


def get_offsets(point, x, y, dim):
    offset_x = point[0] if x % 2 == 0 else dim[0] - point[0]
    offset_y = point[1] if y % 2 == 0 else dim[1] - point[1]
    return offset_x, offset_y


def get_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def check_limit(p1, p2, limit):
    return get_distance(p1, p2) <= limit


ap, bp, br = solution([3, 2], [1, 1], [2, 1], 4)
print(ap)
print(bp)
print(br)
while br.qsize():
    print(br.get())

