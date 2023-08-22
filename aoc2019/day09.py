from aoc2019.helpers import input_ints
from aoc2019.intcode import *


def part1(file):
    return basic_intcode(input_ints(file), [1])


def part2(file):
    return basic_intcode(input_ints(file), [2])
