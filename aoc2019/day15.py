from aoc2019.droid import Droid
from heapq import heappush, heappop


def dij(droid, start):
    scores = {start: 0}
    queue = [(0, start)]
    best = 100000
    while len(queue):
        score, pos = heappop(queue)
        for nb in [droid.newpos(pos, m) for m in droid.possible_moves(pos)]:
            new = score + 1
            if new > best:
                break
            if new < scores.get(nb, 100000):
                scores[nb] = new
                heappush(queue, (new, nb))
    return scores


def part1(file):
    droid = Droid(file)
    droid.start()
    droid.explore()
    droid.kill()
    oxygen = [k for k, v in droid.area.items() if v == 2][0]
    return dij(droid, (0, 0))[oxygen]


def part2(file):
    droid = Droid(file)
    droid.start()
    droid.explore()
    droid.kill()
    oxygen = [k for k, v in droid.area.items() if v == 2][0]
    return max(dij(droid, oxygen).values())
