from aoc2019.helpers import input_lines, bfs
from collections import defaultdict


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


def part2(file):
    mp = input_lines(file)
    graph = defaultdict(list)
    for m in mp:
        planet, orbiter = m.split(")")
        graph[planet] += [orbiter]
        graph[orbiter] += [planet]
    return bfs("YOU", lambda x: graph[x])["SAN"] - 2
