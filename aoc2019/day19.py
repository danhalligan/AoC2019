from aoc2019.intcode2 import *
from aoc2019.helpers import input_ints
from math import floor


def inbeam_gen(prog):
    return lambda x, y: list(Intcode(prog, [x, y]).generate())[0]


def part1(file):
    prog = input_ints(file)
    inbeam = inbeam_gen(prog)
    tot = 0
    for j in range(50):
        for i in range(50):
            tot += inbeam(i, j)
    return tot


def find_ratios(y, inbeam):
    start, end = 0, 0
    for i in range(10000):
        pull = inbeam(i, y)
        if pull == 1 and start == 0:
            start = i
        if pull == 0 and start != 0:
            end = i
            return start / y, end / y


# We can estimate the angle, predict answer and refine.
# We'll the beam x/y ratios from a y value of 200
# r1 = s/y, r2 = e/y = r2
# The y value that fits a 100 sized box is approximately
# (100*s/200 + 100) / (e/200 + r1)
def part2(file):
    prog = input_ints(file)
    inbeam = inbeam_gen(prog)

    r1, r2 = find_ratios(200, inbeam)
    y = floor((99 * r1 + 99) / (r2 - r1)) - 20
    x = floor(r1 * y) - 20

    # iterate to correct solution
    while True:
        if inbeam(x, y + 99):
            if inbeam(x + 99, y):
                return x * 10_000 + y
            y += 1
        else:
            x += 1
