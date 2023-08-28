from aoc2019.intcode2 import *


def part1(file):
    return SimpleIntcode(file, 1).run()[-1]


def part2(file):
    return SimpleIntcode(file, 2).run()[-1]
