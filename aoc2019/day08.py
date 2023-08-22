from aoc2019.helpers import input_str
import numpy as np
from functools import reduce
from advent_of_code_ocr import convert_6


def chunk(x, s):
    return [x[i : i + s] for i in range(0, len(x), s)]


def parse_layers(file):
    x = [int(v) for v in list(input_str(file))]
    return np.array([chunk(y, 25) for y in chunk(x, 25 * 6)])


def part1(file):
    layers = parse_layers(file)
    minl = np.argmin(np.sum(layers, axis=(1, 2)))
    return np.sum(layers[minl] == 1) * np.sum(layers[minl] == 2)


def part2(file):
    layers = parse_layers(file)
    image = reduce(lambda x, y: np.where(x == 2, y, x), layers)
    image = "\n".join(["".join(x) for x in np.where(image == 1, "#", ".")])
    return convert_6(image)
