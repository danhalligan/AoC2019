from aoc2019.helpers import input_ints


def part1(file):
    return sum(e // 3 - 2 for e in input_ints(file))


def part2(file):
    x = input_ints(file)
    tot = 0
    while sum(x) > 0:
        x = [max(e // 3 - 2, 0) for e in x]
        tot += sum(x)
    return tot
