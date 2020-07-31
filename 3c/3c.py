"""
At every state (x,y), we can either move to (x+y,y) or (x,x+y). Starting at (1,1) we get following tree of
possibilities.
                     1,1
         1,2                     2,1
    1,3        3,2          2,3        3,1
1,4   4,3   3,5   5,2   2,5   5,2   3,4   4,1
    .       .       .       .       .       .
    .       .       .       .       .       .
    .       .       .       .       .       .

Continue on this we have to find the depth of occurrence of (m,f) which is our target.
As out target is of order 10^50, algorithms like depth first would be too expensive.
Instead of find shortest path from (1,1) to (m,f), we can instead find path from (m,f) to (1,1)
Notice that for any state (a,b) where b > a, it's parent would be (a,b-a).
We can carry on this process from (m,f) and keep finding parent until we hit (1,1)
We can make this process a little faster in some instances of state.
For example if we have (a, na + b) or (na + b, a) for some integer n > 0 and 0 < b < a. We can subtract a from an + b
for at most n times. In such case it's equivalent to make a jump of n in tree depth towards the root, and hence
some speed up.
Similarly, if we have (1, a) or (a, 1), we can subtract 1 from a for a-1 times before we get to (1,1).
Putting these ideas together, we get the following.
"""


def solution(m, f):
    m, f = int(m), int(f)
    steps = 0
    while m > 0 and f > 0:
        big, sml = max(m, f), min(m, f)
        if sml == 1:
            steps += big - 1
            return str(steps)
        num = big // sml
        big -= num * sml
        steps += num
        m, f = big, sml
    return 'impossible'
