from itertools import product


h = 3
w = 5
g_score = {node: 500 for node in product(range(h), range(w))}
print g_score
