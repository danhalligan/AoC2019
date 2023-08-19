from aoc2019.helpers import input_ints

def part1(file):
    x = input_ints("inputs/day01.txt")
    return sum(e//3-2 for e in x)


def part2(file):
    x = input_ints("inputs/day01.txt")
    tot = 0
    while sum(x) > 0:
        x = [max(e//3-2, 0) for e in x]
        tot += sum(x)
    return tot