"""
This is a very interesting problem. Following is the approach that I've implemented.
For easier notation we will call protagonist 'A' and guard 'B'.
So A and B are both in a rectangular area.
Imagine this rectangular area on an xy plane, such that the bottom left corner of this area coincides with (0, 0)
Now, we find the reflection points as follows.
   ^
   |
   |
   |     |     |     |     |
   |_____|_____|_____|_____|__
   |     |     |     |     |
   |   b | b   |   b | b   |
   |     |     |     |     |
   | a   |   a | a   |   a |
   |_____|_____|_____|_____|__
   |     |     |     |     |
   | a   |   a | a   |   a |
   |     |     |     |     |
   |   b | b   |   b | b   |
   |_____|_____|_____|_____|__
   |     |     |     |     |
   |   B | b   |   b'| b   |
   |     |     |     |     |
   | A   |   a | a   |   a |
<__|_____|_____|_____|_____|______>
   |
The block at the bottom left corner is our original area with A and B. The block on its immediate right is formed by
taking the mirror reflection of our original block across the common side of both the blocks.
The block that is on immediate top of the original block is also formed in the similar way from the original block.
The block on the immediate top-right of the original block can be formed by taking the mirror reflection of
one of the block that is to the immediate right or immediate top of the original block.
Both would give same result due to the commutative nature of mirror reflections.

So using this method we can form infinitely many blocks, and consequently infinitely many reflection of A and B.
The above "image" is only for first quadrant but it can be extended in similar way across all the four quadrants.

Now consider a line l from A to b'. This line is passing through 3 blocks, and 2 sides that separates those 3 blocks,
before reaching b'.

This means that in our original situation, if we fire the beam in the direction of this line l, it will hit the guard
after two reflections off the wall. We can see how that might happens. When beam originates from A and hit the wall, it
reflect off the wall and start travelling toward other wall.

But here what we are doing is, instead of taking the reflection of the beam, we are taking the reflection of our
original block across the wall that we hit with the beam, and putting it right next to our original block.
Doing this allows us to let the beam continue to travel in straight line, but enter the reflected block instead.
For the purpose of this problem, this type of setup is easier to work with instead of taking the reflection of the beam.

Once again, before reaching b' the beam has one more side to pass through. We do the same thing again, instead of taking
a reflection of the beam, we take the reflection of the current block and put it right next to the current block, and
let the beam continue to travel in the straight line. And then, in the third block beam will hit b'.

This is analogous to beam reflecting off of one wall, and then reflection off of another wall and then hitting
the guard.

Also the distance between the A and b' in the above xy plane would be same as the distance that the beam would have to
travel in the original block before hitting the guard, after considering all the reflections off the walls.

So to get to the final answer to the problem, we just have to count all the distinct lines that starts at A and end at
any of the b, such that there aren't any other reflection (of A or B) on that line that lies between A and b, and the
distance between A and b must be within the the given distance limit for beam.

To do this, we first find out the coordinates of all the possible reflection points of A and B that are within
given distance from A.
Then we find all the unique lines that can be formed between A and any reflection point b (and a).
Then for all reflection points on those lines we find out that is it any reflection point b that is closer to A or is
it any reflection point a that is closer to A. We only count those lines where reflection point b is closer to A,
and that gives us our answer. If the reflection point a is closer, then the beam fired in that direction would hit
A after necessary number of reflections, so that direction is not good for firing beam.
"""
from math import sqrt
from fractions import gcd


def solution(dim, a, b, limit):
    """
    Compute the final solution to the problem by calling appropriate functions.
    :param dim: dimension of th rectangular area.
    :param a: Original position of A.
    :param b: Original position of B.
    :param limit: limit on the distance that the beam can travel.
    :return: The total distinct directions where the beam can be fired to hit B.
    """
    a = (a[0], a[1])
    b = (b[0], b[1])
    ref_a, ref_b = get_reflection_points(dim, a, b, limit)
    lines = get_lines(a, ref_a, ref_b)
    attacks = find_attacks(*lines)
    return attacks


def get_reflection_points(dim, a, b, limit):
    """
    Find all the reflection point of A and B among all the blocks that are created by the technique mentioned above,
    such that the distance between A and any reflection point is within the limit.
    :param dim: dimension of th rectangular area.
    :param a: Original position of A.
    :param b: Original position of B.
    :param limit: limit on the distance that the beam can travel.
    :return: sets of all the reflection points of A and B.
    """
    ref_a = set()
    ref_b = set()
    quad_params = [
        # First quadrant
        [0, 0, 1, 1],
        # Second quadrant
        [-1, 0, -1, 1],
        # Third quadrant
        [-1, -1, -1, -1],
        # Fourth quadrant
        [0, -1, 1, -1]
    ]
    for p in quad_params:
        reflection_points_for_quadrant(dim, a, b, limit, ref_a, ref_b, *p)
    return ref_a, ref_b


def reflection_points_for_quadrant(dim, a, b, limit, ref_a, ref_b, x_start, y_start, x_inc, y_inc):
    """
    Find all the reflection point of A and B among all the blocks in the quadrant that is described by the
    given parameters, such that the distance between A and any reflection point is within the limit.
    :param dim: dimension of th rectangular area.
    :param a: Original position of A.
    :param b: Original position of B.
    :param limit: limit on the distance that the beam can travel.
    :param ref_a: set to store the reflection points of A
    :param ref_b: set to store the reflection points of B
    :param x_start: Starting block index in x direction of a given quadrant.
    :param y_start: Starting block index in y direction of a given quadrant.
    :param x_inc: Increment to take for searching more blocks in x direction.
    :param y_inc: Increment to take for searching more blocks in y direction.
    :return: A set of all the reflection points of A and B in the quadrant that is described by the given parameters.
    """
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
            y += y_inc
        x += x_inc


def get_offsets(p, x, y, dim):
    """
    Given any point p in the original block and the bottom left point of any reflection block, it computes the
    offset of the reflection point of p with respect to the bottom left corner of its block.
    :param p: point whose reflection point's offset is to be found.
    :param x: x coordinate of the bottom left corner of the reflected block.
    :param y: y coordinate of the bottom left corner of the reflected block.
    :param dim: dimension of the block
    :return: offset of the reflection point of p with respect to the bottom left corner of its block.
    """
    offset_x = p[0] if x % 2 == 0 else dim[0] - p[0]
    offset_y = p[1] if y % 2 == 0 else dim[1] - p[1]
    return offset_x, offset_y


def get_distance(p1, p2):
    """
    Compute distance between the given two points.
    :param p1: point 1
    :param p2: point 2
    :return: distance between p1 and p2
    """
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def check_limit(p1, p2, limit):
    """
    Check if distance between two point is within given limit
    :param p1: point 1
    :param p2: point 2
    :param limit: limit on the distance between two points
    :return: True if distance between p1 and p2 is less than or equal to the limit. False otherwise.
    """
    return get_distance(p1, p2) <= limit


def find_attacks(lines_a, lines_b):
    """
    Find the the number of distinct directions where the beam can be fired to hit B.
    :param lines_a: All the lines from A to any reflection of A with the shortest distance among all the distances
    between A and any reflection of A that falls on that line.
    :param lines_b: All the lines from A to any reflection of B with the shortest distance among all the distances
    between A and any reflection of B that falls on that line.
    :return: distinct number of directions where A can fire the beam to hit B.
    """
    attacks = 0
    for line in lines_b:
        if line in lines_a:
            if lines_a[line] > lines_b[line]:
                attacks += 1
        else:
            attacks += 1
    return attacks


def get_lines(a, ref_a, ref_b):
    """
    Compute all the lines that can be formed between A and all the reflection of A (and B), along with the shortest
    distance among all the the distances between A and any reflection of A (and B) that falls on that line.
    :param a: Coordinates of point A
    :param ref_a: set of all the points that are reflection of A.
    :param ref_b: set of all the points that are reflection of B.
    :return: Dictionary of all the lines between A and all the reflection of A (and B), along with the shortest
    distance among all the the distances between A and any reflection of A (and B) that falls on that line.
    """
    lines_a = dict()
    lines_b = dict()
    for a_r in ref_a:
        if a_r != a:
            dist = get_distance(a, a_r)
            line = find_line(a, a_r)
            if line in lines_a:
                if dist < lines_a[line]:
                    lines_a[line] = dist
            else:
                lines_a[line] = dist
    for b_r in ref_b:
        dist = get_distance(a, b_r)
        line = find_line(a, b_r)
        if line in lines_b:
            if dist < lines_b[line]:
                lines_b[line] = dist
        else:
            lines_b[line] = dist
    return lines_a, lines_b


def find_line(p1, p2):
    """
    For the given two points, find the line between them.
    :param p1: point 1
    :param p2: point 2
    :return: A 3-tuple with value (a, b, c) such that ax + by + c = 0 is the line formed by provided points.
    """
    a = p2[1] - p1[1]
    b = p1[0] - p2[0]
    c = p1[1] * (p2[0] - p1[0]) - p1[0] * (p2[1] - p1[1])
    g = gcd(abs(a), gcd(abs(b), abs(c)))
    a, b, c = a // g, b // g, c // g
    return a, b, c
