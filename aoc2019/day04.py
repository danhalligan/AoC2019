from aoc2019.helpers import input_str


def parse(file):
    return [int(x) for x in input_str(file).split("-")]


def valid(x):
    x = [int(v) for v in list(str(x))]
    return sorted(x) == x and any(x[i] == x[i + 1] for i in range(len(x) - 1))


def part1(file):
    a, b = parse(file)
    return sum(valid(x) for x in range(a, b + 1))


def has_double(x):
    # since numbers are strictly increasing to be valid, we can just check if
    # there are two of any digit
    return any(x.count(i) == 2 for i in range(10))


def valid2(x):
    x = [int(v) for v in list(str(x))]
    return sorted(x) == x and has_double(x)


def part2(file):
    a, b = parse(file)
    return sum(valid2(x) for x in range(a, b + 1))
