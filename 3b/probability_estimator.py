from random import randint


a = [
  [0, 1, 0, 0, 0, 1],   # s0, the initial state, goes to s1 and s5 with equal probability
  [4, 0, 0, 3, 2, 0],   # s1 can become s0, s3, or s4, but with different probabilities
  [0, 0, 0, 0, 0, 0],   # s2 is terminal, and unreachable (never observed in practice)
  [0, 0, 0, 0, 0, 0],   # s3 is terminal
  [0, 0, 0, 0, 0, 0],   # s4 is terminal
  [0, 0, 0, 0, 0, 0],   # s5 is terminal
]
graph = []
for state in a:
    n = []
    for i in range(len(state)):
        for _ in range(state[i]):
            n.append(i)
    graph.append(n)

print(graph)

prob = [0 for _ in range(len(a))]
for _ in range(1000000):
    curr = 0
    while len(graph[curr]):
        curr = graph[curr][randint(0, len(graph[curr]) - 1)]
    prob[curr] += 1

print prob
print sum(prob)
