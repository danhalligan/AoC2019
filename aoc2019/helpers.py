# Functions to help read inputs
import re
from heapq import heappush, heappop


def getint(x):
    """Grab a single int from a string"""
    return int(re.search("-*\\d+", x).group())


def ints(x):
    """Coerce a list into a list of ints"""
    return [int(y) for y in x]


def input_str(file):
    """Returns input file as a str"""
    return open(file, "r").read().rstrip()


def input_lines(file):
    """Returns lines from input file"""
    return open(file).read().splitlines()


def input_ints(file):
    """Returns list of ints from input file (split by new line or comma)"""
    txt = input_str(file)
    return ints(re.split(r"[\n,]", txt))


def input_blocks(file, sep="\n\n"):
    """Returns lines of input split by empty lines from input file"""
    blocks = open(file).read().split(sep)
    return [block.split() for block in blocks]


# Breadth First Search
# If end is provided, we don't consider paths any longer than path to end.
def bfs(start, neighbours, end=None):
    visited = {start: 0}
    queue = []
    queue.append(start)
    while queue:
        pos = queue.pop(0)
        for neighbour in neighbours(pos):
            if neighbour not in visited:
                if end is None or visited[pos] + 1 < visited.get(end, float("inf")):
                    visited[neighbour] = visited[pos] + 1
                    queue.append(neighbour)
    return visited


# Dijkstra's algorithm
# If end is provided, we don't consider paths any longer than path to end.
def dij(start, neighbours, end=None):
    scores = {start: 0}
    queue = [(0, start)]
    best = float("inf")
    while len(queue):
        score, pos = heappop(queue)
        for nb in neighbours(pos):
            new_score = score + 1
            if new_score > best:
                break
            if new_score < scores.get(nb, float("inf")):
                if end is None or new_score < scores.get(end, float("inf")):
                    scores[nb] = new_score
                    heappush(queue, (new_score, nb))
    return scores
