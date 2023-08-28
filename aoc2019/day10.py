from aoc2019.helpers import input_lines
from numpy import sign
from math import gcd, sqrt, degrees, atan2
from heapq import heappush, heappop


def parse_asteroids(file):
    return [
        (x, y)
        for y, line in enumerate(input_lines(file))
        for x, v in enumerate(line)
        if v != "."
    ]


def sightline(a, b):
    # to calculate the sight line, we'll consider steps.
    # we need to consider max(difference in x, difference in y) steps
    xs = sign(b[0] - a[0])
    ys = sign(b[1] - a[1])
    steps = gcd(abs(a[0] - b[0]), abs(a[1] - b[1]))
    xd = int((b[0] - a[0]) / steps)
    yd = int((b[1] - a[1]) / steps)
    return [(a[0] + xd * step, a[1] + yd * step) for step in range(1, steps)]


def visable(a, b, asteroids):
    return all(v not in asteroids for v in sightline(a, b))


def detectable(x, asteroids):
    return sum(visable(x, b, asteroids) for b in asteroids if x != b)


def best_location(asteroids):
    n = [detectable(a, asteroids) for a in asteroids]
    return asteroids[n.index(max(n))]


def angle(a, b):
    angle = degrees(atan2(b[1] - a[1], b[0] - a[0]))
    return (90 + angle) % 360


def dist(a, b):
    return sqrt((b[1] - a[1]) ** 2 + (b[0] - a[0]) ** 2)


def part1(file):
    asteroids = parse_asteroids(file)
    return max(detectable(a, asteroids) for a in asteroids)


def part2(file):
    asteroids = parse_asteroids(file)
    loc = best_location(asteroids)

    q = []
    for x in asteroids:
        if x != loc:
            heappush(q, ((angle(loc, x), dist(loc, x)), x))

    count = 0
    ang = None
    while asteroids:
        (xa, xd), x = heappop(q)
        if ang == xa:
            asteroids += [x]
            heappush(q, ((xa + 360, xd), loc))
        else:
            ang = xa
            count += 1
            if count == 200:
                return x[0] * 100 + x[1]
