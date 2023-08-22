from aoc2019.helpers import input_lines
import re
from math import lcm


def parse_input(file):
    lines = input_lines(file)
    return [
        {"c": [int(x) for x in re.findall("-*\d+", line)], "v": (0, 0, 0)}
        for line in lines
    ]


def print_moons(moons):
    for moon in moons:
        print(
            f"pos=<x={moon['c'][0]:2}, y={moon['c'][1]:2}, z={moon['c'][2]:2}>, ",
            end="",
        )
        print(f"vel=<x={moon['v'][0]:2}, y={moon['v'][1]:2}, z={moon['v'][2]:2}>")


def pull(a, b):
    return 1 if a < b else -1 if a > b else 0


def movement(curr, pairs, i):
    return sum(pull(curr["c"][i], m["c"][i]) for m in pairs)


def velocity(curr, pairs):
    return tuple(curr["v"][i] + movement(curr, pairs, i) for i in range(3))


def move(x):
    return tuple(x["c"][i] + x["v"][i] for i in range(3))


def moon_energy(x):
    return sum(abs(x["c"][i]) for i in range(3)) * sum(abs(x["v"][i]) for i in range(3))


def part1(file, steps=1000):
    moons = parse_input(file)

    for _ in range(steps):
        for curr in moons:
            pairs = [pair for pair in moons if curr != pair]
            curr["v"] = velocity(curr, pairs)
        for curr in moons:
            curr["c"] = move(curr)

    return sum(moon_energy(x) for x in moons)


def find_cycle(moons, i):
    sc = tuple(x["c"][i] for x in moons)
    sv = tuple(x["v"][i] for x in moons)
    for count in range(500000):
        for curr in moons:
            pairs = [pair for pair in moons if curr != pair]
            curr["v"] = velocity(curr, pairs)
        for curr in moons:
            curr["c"] = move(curr)
        xc = tuple(x["c"][i] for x in moons)
        xv = tuple(x["v"][i] for x in moons)
        if xc == sc and xv == sv:
            return count + 1


# the x, y and z coordinates are independent
# if each cycle, then they will coincide at the lowest common denominator
def part2(file):
    moons = parse_input(file)
    cycles = [find_cycle(moons, i) for i in range(3)]
    return lcm(*cycles)
