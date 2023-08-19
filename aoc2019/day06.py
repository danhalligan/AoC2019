from aoc2019.helpers import input_lines
from collections import defaultdict
from heapq import *


def total_orbits(tree, x, depth):
    if len(tree[x]):
        return sum(total_orbits(tree, y, depth + 1) for y in tree[x]) + depth
    else:
        return depth


def part1(file):
    mp = input_lines(file)
    orbits = defaultdict(list)
    for m in mp:
        planet, orbiter = m.split(")")
        orbits[planet] += [orbiter]
    return total_orbits(orbits, "COM", 0)


def dij(graph, start):
    scores = {start: 0}
    queue = [(0, start)]
    best = 100000
    while len(queue):
        score, pos = heappop(queue)
        for nb in graph[pos]:
            new = score + 1
            if new > best:
                break
            if new < scores.get(nb, 100000):
                scores[nb] = new
                heappush(queue, (new, nb))
    return scores


def part2(file):
    mp = input_lines(file)
    graph = defaultdict(list)
    for m in mp:
        planet, orbiter = m.split(")")
        graph[planet] += [orbiter]
        graph[orbiter] += [planet]

    return dij(graph, "YOU")["SAN"] - 2
