from aoc2019.intcode import *
from aoc2019.arcade import Arcade
from collections import defaultdict
from aoc2019.helpers import input_ints
from queue import Queue


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def part1(file):
    prog = input_ints(file)
    inp = Queue()
    out = Queue()
    arcade = Intcode(prog, lambda: inp.get(), qout(out))
    gen = arcade.gen()
    screen = defaultdict(int)
    for x, y, v in chunks(list(gen), 3):
        screen[x, y] = v
    return len([x for x in screen.values() if x == 2])


def part2(file):
    x = Arcade(file)
    x.play()
    return x.score
