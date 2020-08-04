"""
For this problem I had to read some theory on Beatty sequences and series, that are defined as follows.
sum over floor(i*r) for 1 <= i, where r is a positive irrational number.
I came across some results that showed that for any Beatty sequence there exist another Beatty sequence that partition
the set of natural numbers.
Therefore, in our case where r = sqrt(2) there is another paired Beatty sequence for a different positive irrational
number s.
There is another result to relate r and s given as follows:
1/r + 1/s = 1
This lets us compute s = 2 + sqrt(2)

Say we want to sum over first n terms of beatty sequence defined by principle irrational number as r.
Let m = floor((r-1)*n)
sum over 1 <= i <= n of floor(i*r) = (n + m)(n + m + 1)/2 - (sum over 1 <= j <= m of floor(j*s))
Further applying the results to the summation part on right hand side, to get back to r as our principle
irrational number we get following.
sum over 1 <= i <= n of floor(i*r) = nm + n(n+1)/2 - m(m+1)/2 - sum over 1 <= j <= m of floor(j*r)
The above recursive formula is being used in compute function to get the answer.
"""
sqrt_2 = long('''4142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727\
350138462309122970249248360558507372126441214970999358314132226659275055927557999505011527820''')
ten_p = long('''10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000''')


def solution(n):
    return str(compute(int(n)))


def compute(n):
    if n == 0:
        return long(0)
    m = long((sqrt_2 * n) / ten_p)
    return long(n*m) + long(n*(n+1)/2) - long(m*(m+1)/2) - compute(m)
