from aoc2019.intcode import *


def part1(file):
    return SimpleIntcode(file, 1).run()[-1]


def part2(file):
    return SimpleIntcode(file, 5).run()[-1]
