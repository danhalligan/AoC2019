from aoc2019.intcode import *
from aoc2019.helpers import input_ints
from collections import defaultdict

prog = input_ints("inputs/day17.txt")
i, j = 0, 0
scaffolds = defaultdict(lambda: '.')
for v in Intcode(prog).gen():
    if v == 35:
        scaffolds[i, j] = "#"
        i += 1
    elif v == 46:
        scaffolds[i, j] = "."
        i += 1
    elif v == 10:
        j += 1
        i = 0


def span(x):
    x = list(x)
    return range(min(x), max(x) + 1)


def view(scaffolds):
    xr = span(x[0] for x in scaffolds.keys())
    yr = span(x[1] for x in scaffolds.keys())
    for j in yr:
        print("".join(scaffolds[i, j] for i in xr))

view(scaffolds)
