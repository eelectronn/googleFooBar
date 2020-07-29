def solution(x, y):
    """
    The consecutive ids horizontally or vertically have difference in arithmetic progression with difference of 1.
    In other words difference of difference is 1.
    The sequence at base start with 1 and the differences starts with 2, going across that line to say xth number
    would be a = 1 + 2 + ... + x. This is done by x(x+1)/2.
    Now to rise up from there to say yth number, the sequence of difference between ids looks like x, x+1 ...
    We are already at the base row, so we only need to add y-1 terms to get to y. So we get the following.
    x + (x+1) + ... (x+y-2)
    Note that we are adding all the natural numbers from x to x+y-2, which is y-1 count of terms.
    This sum is given by the expression (y-1)y/2 + (x-1)(y-1).
    It's adding numbers 1 through y-1 separately and then adding x-1 to each of y-1 terms, which gives us the sum of
    x + (x+1) + ... (x+y-2).
    To get our final answer, we add that to a.
    f = a + x + (x+1) + ... (x+y-2)
    f = x(x+1)/2 + (y-1)y/2 + (x-1)(y-1)

    :param x: distance from vertical wall.
    :param y: distance from base.
    :return: id of prisoner.
    """
    return str(x * (x + 1) // 2 + y * (y - 1) // 2 + (x - 1) * (y - 1))
