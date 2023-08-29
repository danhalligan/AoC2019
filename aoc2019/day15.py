from aoc2019.droid import Droid
from aoc2019.helpers import bfs


def part1(file):
    droid = Droid(file).start().explore().kill()
    oxygen = [k for k, v in droid.area.items() if v == 2][0]
    return bfs((0, 0), lambda x: droid.neighbours(x))[oxygen]


def part2(file):
    droid = Droid(file).start().explore().kill()
    oxygen = [k for k, v in droid.area.items() if v == 2][0]
    return max(bfs(oxygen, lambda x: droid.neighbours(x)).values())
