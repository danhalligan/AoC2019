from aoc2019.helpers import input_lines


def path(moves):
    path = [0]
    pos = 0
    inc = {"R": +1, "U": +1j, "L": -1, "D": -1j}
    for m in moves:
        for _ in range(int(m[1:])):
            pos += inc[m[0]]
            path += [pos]
    return path


def md(x):
    return int(abs(x.real) + abs(x.imag))


def paths(file):
    lines = input_lines(file)
    p1 = path(lines[0].split(","))
    p2 = path(lines[1].split(","))
    inter = set(p1).intersection(p2).difference([0])
    return p1, p2, inter


def part1(file):
    _, _, inter = paths(file)
    return min(md(x) for x in list(inter))


def part2(file):
    p1, p2, inter = paths(file)
    return min(p1.index(x) + p2.index(x) for x in list(inter))
