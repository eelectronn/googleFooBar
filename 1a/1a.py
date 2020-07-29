def solution(data, n):
    freq = dict()
    for s in data:
        if s in freq:
            freq[s] += 1
        else:
            freq[s] = 1
    modified_data = []
    for s in data:
        if freq[s] <= n:
            modified_data.append(str(s))
    return ','.join(modified_data)
