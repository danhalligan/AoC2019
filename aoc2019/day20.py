import numpy as np
from aoc2019.helpers import input_lines, bfs
from string import ascii_uppercase
from itertools import permutations
from termcolor import colored


def htriple(data, code):
    # coordinates of 3 horizontal consecutive letters
    a = data[:, :-2] == code[0]
    b = data[:, 1:-1] == code[1]
    c = data[:, 2:] == code[2]
    out = np.where(np.logical_and(np.logical_and(a, b), c))
    if np.any(out):
        return out[0], out[1]


def vtriple(data, code):
    # coordinates of 3 vertical consecutive letters
    a = data[:-2, :] == code[0]
    b = data[1:-1, :] == code[1]
    c = data[2:, :] == code[2]
    out = np.where(np.logical_and(np.logical_and(a, b), c))
    if np.any(out):
        return out[0], out[1]


def unpack(pos):
    return [[pos[j][i] for j in range(len(pos))] for i in range(len(pos[0]))]


def find_code(data, pair):
    found = []
    if pos := vtriple(data, pair + ["."]):
        found += [(p[0] + 2, p[1]) for p in unpack(pos)]
    if pos := vtriple(data, ["."] + pair):
        found += [(p[0], p[1]) for p in unpack(pos)]
    if pos := htriple(data, pair + ["."]):
        found += [(p[0], p[1] + 2) for p in unpack(pos)]
    if pos := htriple(data, ["."] + pair):
        found += [(p[0], p[1]) for p in unpack(pos)]
    return found


def find_portals(data):
    portals = {}
    codes = list(permutations(ascii_uppercase, 2))
    for code in codes:
        code = list(code)
        # print(code)
        found = find_code(data, code)
        if len(found) == 2:
            # print(code, found[0], found[1])
            portals[found[0]] = found[1]
            portals[found[1]] = found[0]
    return portals


def move(p, d):
    return {
        "^": (p[0] - 1, p[1]),
        ">": (p[0], p[1] + 1),
        "v": (p[0] + 1, p[1]),
        "<": (p[0], p[1] - 1),
    }[d]


def valid_moves(data, portals, pos):
    moves = []
    for d in ["^", ">", "v", "<"]:
        new = move(pos, d)
        if data[new] != "#":
            if data[new] in ascii_uppercase:
                if pos in portals:
                    moves += [portals[pos]]
            else:
                moves += [new]
    return moves


def print_donut(data, path=[]):
    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            if (row, col) in path:
                print(colored("+", "red"), end="")
            else:
                print(data[row, col], end="")
        print()


def part1(file):
    data = np.array([list(line) for line in input_lines(file)])
    portals = find_portals(data)
    start = find_code(data, ["A", "A"])[0]
    end = find_code(data, ["Z", "Z"])[0]
    return bfs(start, lambda x: valid_moves(data, portals, x))[end]


# position is on outer edge of donut (not in the actual labels)
def is_outer(data, pos):
    return (
        pos[0] == 2
        or pos[1] == 2
        or pos[0] == data.shape[0] - 3
        or pos[1] == data.shape[1] - 3
    )


def valid_moves_layers(data, portals, state):
    pos, layer = state
    moves = []
    for d in ["^", ">", "v", "<"]:
        new = move(pos, d)
        if data[new] != "#":
            if data[new] in ascii_uppercase:
                if is_outer(data, pos) and layer == 0:
                    continue
                elif is_outer(data, pos):
                    new_layer = layer - 1
                else:
                    new_layer = layer + 1
                if pos in portals:
                    moves += [(portals[pos], new_layer)]
            else:
                moves += [(new, layer)]
    return moves


def part2(file):
    data = np.array([list(line) for line in input_lines(file)])
    # print_donut(data)
    portals = find_portals(data)
    start = (find_code(data, ["A", "A"])[0], 0)
    end = (find_code(data, ["Z", "Z"])[0], 0)
    return bfs(start, lambda x: valid_moves_layers(data, portals, x), end)[end]
