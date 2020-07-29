# You have L, a list containing some digits (0 to 9). Write a function solution(L) which finds the largest number that
# can be made from some or all of these digits and is divisible by 3. If it is not possible to make such a number,
# return 0 as the solution. L will contain anywhere from 1 to 9 digits.  The same digit may appear multiple times in
# the list, but each element in the list may only be used once.

"""
We know that if a number x has more digits than a number y, then x > y.
So we try to use the largest possible number of digits in the given array.
A number is divisible by 3 if sum of its digit is divisible by 3. So once we filter out the digits whose sum is
divisible by 3, a number formed by any permutation of those digit would be divisible by 3. Out of all those permutations
the largest one would be formed by the permutation where digits are sorted in decreasing order.

Now for the given array, if sum s of its digit is already divisible by 3, then no adjustment is needed.
In this case we return the largest number formed by these digits.
Other cases are sum of number is is either 1 (mod 3) or 2 (mod 3).
If s is 1 (mod 3), then we remove the smallest digit which is 1 (mod 3). This will make the sum of the rest of the
digits divisible by 3.
If there are no digits that are 1 (mod 3), the we remove two of the smallest digits that are 2 (mod 3).
This is due the fact that adding two numbers that are 2 (mod 3), we get a number that is 1 (mod 3).
(2 + 2) (mod 3) = 4 (mod 3) = 1 (mod 3).

We follow the same process if s is 2 (mod 3).
First we try to remove the smallest digit that is 2 (mod 3).
If that's not possible, remove two digits that are 1 (mod 3), due to the fact that (1 + 1) (mod 3) = 2 (mod 3).

Here solution function create a frequency array from the original array and find sum s and then take action according
to the different cases.
The adjust function make the adjustment to the frequency array by removing appropriate digits based on the
logic described above.
form_largest_number takes the adjusted frequency array and give the number obtained from that.
"""


def solution(l):
    freq = [0 for _ in range(10)]
    for i in l:
        freq[i] += 1
    s = sum(l)
    if s % 3 == 0:
        return form_largest_number(freq)
    elif s % 3 == 1:
        return form_largest_number(adjust(freq, 1))
    else:
        return form_largest_number(adjust(freq, 2))


def adjust(freq, m):
    for i in range(10):
        if i % 3 == m:
            if freq[i] > 0:
                freq[i] -= 1
                return freq

    if m == 1:
        m = 2
    else:
        m = 1

    r = 2
    for i in range(10):
        if i % 3 == m:
            if freq[i] >= r:
                freq[i] -= r
                r = 0
            elif freq[i] > 0:
                freq[i] -= 1
                r -= 1
        if r == 0:
            return freq
    return []


def form_largest_number(freq):
    s = ''
    for i in range(9, -1, -1):
        s += freq[i]*str(i)
    if len(s) > 0:
        return int(str(s))
    return 0


print(solution([2, 2, 2, 2, 2]))
