from aoc2019.intcode2 import *
from aoc2019.helpers import input_ints
from collections import defaultdict
from aoc2019.vacuum import *


def parse_scaffolds(file):
    prog = input_ints(file)
    i, j = 0, 0
    scaffolds = defaultdict(lambda: ".")
    for v in Intcode(prog).generate():
        if v == 10:
            j += 1
            i = 0
        else:
            scaffolds[i, j] = chr(v)
            i += 1
    return scaffolds


def span(x):
    x = list(x)
    return range(min(x), max(x) + 1)


def view(scaffolds):
    xr = span(x[0] for x in scaffolds.keys())
    yr = span(x[1] for x in scaffolds.keys())
    for j in yr:
        print("".join(scaffolds[i, j] for i in xr))


def cross(i, j):
    return [(i, j), (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]


def part1(file):
    scaffolds = parse_scaffolds(file)
    xr = list(span(x[0] for x in scaffolds.keys()))[1:-1]
    yr = list(span(x[1] for x in scaffolds.keys()))[1:-1]
    crosses = []
    for j in yr:
        for i in xr:
            if all(scaffolds[x, y] == "#" for x, y in cross(i, j)):
                crosses += [(i, j)]
    return sum(a * b for a, b in crosses)


def forward(face, pos):
    # move forward in current direction one position
    return {
        "^": (pos[0], pos[1] - 1),
        ">": (pos[0] + 1, pos[1]),
        "v": (pos[0], pos[1] + 1),
        "<": (pos[0] - 1, pos[1]),
    }[face]


def turn(face, direction):
    if direction == "R":
        return {"^": ">", ">": "v", "v": "<", "<": "^"}[face]
    else:
        return {"^": "<", "<": "v", "v": ">", ">": "^"}[face]


def find_path(area):
    pos = [k for k, v in area.items() if v == "^"][0]
    face = "^"
    steps = 0, 0
    path = []
    while True:
        if area[forward(face, pos)] == "#":
            steps = 0
            while area[forward(face, pos)] == "#":
                steps += 1
                pos = forward(face, pos)
            path += [steps]
        else:
            turned = False
            for d in ["L", "R"]:
                if area[forward(turn(face, d), pos)] == "#":
                    face = turn(face, d)
                    path += [d]
                    turned = True
            if not turned:
                return path


def replace_section(path, section, code):
    new = []
    i = 0
    while i < len(path):
        chunk = tuple(path[i : i + len(section)])
        if chunk == section:
            new += code
            i += len(section)
        else:
            new += [path[i]]
            i += 1
    return new


# Given the path, its relatively easy to find sections manually.
# We can only have 3, which means we're looking for 3 repeats
# - repeats can't have more than 20 instructions (11 elements max)
# - one repeats must start at start, one must end at end.
def part2(file):
    area = parse_scaffolds(file)
    path = tuple(find_path(area))

    sections = [
        ("R", 6, "L", 10, "R", 8, "R", 8),
        ("R", 12, "L", 10, "R", 6, "L", 10),
        ("R", 12, "L", 8, "L", 10),
    ]
    path = replace_section(path, sections[0], "A")
    path = replace_section(path, sections[1], "B")
    path = replace_section(path, sections[2], "C")

    vac = Vacuum(file)
    vac.input(
        main=",".join(path),
        a=",".join(str(x) for x in sections[0]),
        b=",".join(str(x) for x in sections[1]),
        c=",".join(str(x) for x in sections[2]),
        video=False,
    )
    return vac.run()
