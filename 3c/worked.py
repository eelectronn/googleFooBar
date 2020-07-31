def solution(m, f):
    m = int(m)
    f = int(f)
    count = 0
    while m != 1 or f != 1:
        big = max(m, f)
        sml = min(m, f)
        if sml == 1:
            count += big - 1
            return str(count)
        if big % sml == 0:
            return 'impossible'
        num = big // sml
        big -= num * sml
        count += num
        m = big
        f = sml
    if m == 1 or f == 1:
        return str(count)
    else:
        return 'impossible'
