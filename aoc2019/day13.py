from aoc2019.intcode import *
from aoc2019.arcade import Arcade
from collections import defaultdict
from aoc2019.helpers import input_ints


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def part1(file):
    prog = input_ints(file)
    arcade = Intcode(prog).generate()
    screen = defaultdict(int)
    for x, y, v in chunks(list(arcade), 3):
        screen[x, y] = v
    return len([x for x in screen.values() if x == 2])


def part2(file):
    x = Arcade(file).play()
    return x.score
