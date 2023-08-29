from aoc2019.helpers import input_lines, span
from heapq import heappop, heappush
import string


def parse_map(file):
    grid = [list(line) for line in input_lines(file)]
    area = {}
    items = []
    robots = []
    for j in range(len(grid)):
        for i in range(len(grid[j])):
            if grid[j][i] in string.ascii_letters:
                items += [(grid[j][i], (i, j))]
                area[i, j] = "."
            elif grid[j][i] == "@":
                robots += [(i, j)]
                area[i, j] = "."
            else:
                area[i, j] = grid[j][i]
    return area, (tuple(robots), tuple(items))


def view(area, state):
    robots, items = state
    items = {b: a for a, b in items}
    xr = span(x[0] for x in area.keys())
    yr = span(x[1] for x in area.keys())
    for j in yr:
        for i in xr:
            if (i, j) in robots:
                print("@", end="")
            elif (i, j) in items:
                val = items[i, j]
                print(val, end="")
            else:
                print(area[i, j], end="")
        print()


def move(p, d):
    return {
        "^": (p[0], p[1] - 1),
        ">": (p[0] + 1, p[1]),
        "v": (p[0], p[1] + 1),
        "<": (p[0] - 1, p[1]),
    }[d]


def valid_moves(area, pos, robots):
    return [
        move(pos, d)
        for d in ["^", ">", "v", "<"]
        if area[move(pos, d)] != "#" and move(pos, d) not in robots
    ]


# find shortest paths to targets using Dijkstra's algorithm
def get_scores(area, start, items, robots=[]):
    item_locations = [b for _, b in items]
    scores = {start: 0}
    queue = [(0, start)]
    while len(queue):
        score, pos = heappop(queue)
        for npos in valid_moves(area, pos, robots):
            new = score + 1
            if new < scores.get(npos, 10000000):
                scores[npos] = new
                if npos not in item_locations:
                    heappush(queue, (new, npos))
    kr = {b: a for a, b in items if a in string.ascii_lowercase}
    return [{"key": kr[k], "score": v, "pos": k} for k, v in scores.items() if k in kr]


def find_value(area, value):
    if value in area.values():
        return [k for k, v in area.items() if v == value][0]


def unlock(items, key):
    return tuple([item for item in items if item[0] != key and item[0].lower() != key])


def part1(file):
    area, state = parse_map(file)
    start = state
    scores = {start: 0}
    queue = [(0, start)]
    best = 10000000
    while len(queue):
        score, state = heappop(queue)
        robots, items = state
        for mv in get_scores(area, robots[0], items):
            new_score = score + mv["score"]
            remaining = unlock(items, mv["key"])
            if remaining:
                new_state = (tuple([mv["pos"]]), remaining)
                if new_score < scores.get(new_state, 10000000) and new_score < best:
                    scores[new_state] = new_score
                    heappush(queue, (new_score, new_state))
            else:
                if new_score < best:
                    best = new_score
    return best


def fix_area(area, pos):
    area[pos[0] - 1, pos[1]] = "#"
    area[pos[0] + 1, pos[1]] = "#"
    area[pos[0], pos[1] - 1] = "#"
    area[pos[0], pos[1] + 1] = "#"
    area[pos[0], pos[1]] = "#"
    return area


def add_robots(state):
    robots, items = state
    p = robots[0]
    robots = (
        (p[0] - 1, p[1] - 1),
        (p[0] + 1, p[1] - 1),
        (p[0] - 1, p[1] + 1),
        (p[0] + 1, p[1] + 1),
    )
    return (robots, items)


def all_moves(area, robots, items):
    moves = []
    for i in range(4):
        robot = robots[i]
        others = [x for j, x in enumerate(robots) if i != j]
        for move in get_scores(area, robot, items, others):
            move["robot"] = i
            moves += [move]
    return moves


def move_robots(robots, mv):
    return tuple(
        [robot if i != mv["robot"] else mv["pos"] for i, robot in enumerate(robots)]
    )


def part2(file):
    area, state = parse_map(file)
    area = fix_area(area, state[0][0])
    state = add_robots(state)

    start = state
    scores = {start: 0}
    queue = [(0, start)]
    best = 10000000
    while len(queue):
        score, state = heappop(queue)
        robots, items = state
        for mv in all_moves(area, robots, items):
            new_score = score + mv["score"]
            remaining = unlock(items, mv["key"])
            if remaining:
                new_state = (move_robots(robots, mv), remaining)
                if new_score < scores.get(new_state, 10000000) and new_score < best:
                    scores[new_state] = new_score
                    heappush(queue, (new_score, new_state))
            else:
                if new_score < best:
                    # print(new_score)
                    best = new_score
    return best
