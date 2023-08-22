from aoc2019.helpers import input_lines
from itertools import cycle, repeat, chain
from itertools import accumulate, chain, cycle, islice, repeat


def rep(x, n):
    return [val for val in x for _ in range(n)]


def phase(signal, pattern):
    new = []
    for i in range(len(signal)):
        expanded = rep(pattern, i + 1)
        expanded = (expanded * (len(signal) // len(pattern) + 1))[1 : len(signal) + 1]
        new += [int(str(sum(a * b for a, b in zip(signal, expanded)))[-1])]
    return new


def fft(signal, pattern, n=100):
    signal = [int(x) for x in list(signal)]
    for _ in range(n):
        signal = phase(signal, pattern)
    return "".join([str(x) for x in signal])


def part1(file):
    signal = input_lines(file)[0]
    pattern = [0, 1, 0, -1]
    return fft(signal, pattern)[:8]


# https://www.reddit.com/r/adventofcode/comments/ebf5cy/2019_day_16_part_2_understanding_how_to_come_up
# The pattern is 0, 1, 0, -1 which gets repeated n times (but skipping the first value)
# When we calculate the *last* element of our 10_000 int signal, n is 10_0000 
# and the repeated pattern therefore just ends up being 0,0,0,....1.
# Thus the last number after a "phase" will be just signal[-1] (everything else
# is multiplied by 0 and doesn't contribute to the sum).
# For the second last number, our pattern is 0,0,0,0....1,1.
# Thus we need to take add the last two numbers (and mod 10 to take just the
# units).
# This will work for offsets > 10_000 / 2, after which we have to consider
# other aspects of the pattern...
def part2(file):
    signal = input_lines(file)[0]
    offset = int(signal[:7])
    signal = [int(x) for x in list(signal)]
    signal = (signal * 10_000)[offset:]
    signal.reverse()
    for _ in range(100):
        signal = [x % 10 for x in accumulate(signal)]
    signal.reverse()
    return "".join(str(x) for x in signal[:8])
