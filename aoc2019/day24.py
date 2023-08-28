from collections import defaultdict
from aoc2019.helpers import input_lines


def neighbours(i, j):
    return [(i, j - 1), (i - 1, j), (i + 1, j), (i, j + 1)]


def print_board(b):
    for i in range(5):
        print(*[b[i, j] for j in range(5)], sep="")


def update(board):
    new_board = defaultdict(int)
    for pos in list(board.keys()):
        new_board[pos] = board[pos]
        vals = [board[x] for x in neighbours(*pos)]
        if board[pos] and sum(vals) != 1:
            new_board[pos] = 0
        if not board[pos] and sum(vals) in [1, 2]:
            new_board[pos] = 1
    return new_board


def parse_data(file, pt2=False):
    dat = input_lines(file)
    board = defaultdict(int)
    for i in range(len(dat)):
        line = list(dat[i])
        for j in range(len(line)):
            if pt2:
                if line[j] == "#":
                    board[0, i, j] = 1
            else:
                board[i, j] = 1 if line[j] == "#" else 0
    return board


def biodiversity(board):
    return sum(2**i for i, x in enumerate(board.values()) if x)


def part1(file):
    boards = []
    board = parse_data(file)
    while True:
        boards.append(list(board.values()))
        board = update(board)
        if list(board.values()) in boards:
            break

    return biodiversity(board)


def adjust_coord(space, i, j, ic, jc):
    # In squares 8, 12, 14 and 18 we can have 5 neighbours if we move to a
    # containing space.
    if i == 2 and j == 1 and jc == 1:  # square 8
        return [(space + 1, i, 0) for i in range(5)]
    if i == 1 and j == 2 and ic == 1:  # square 12
        return [(space + 1, 0, j) for j in range(5)]
    if i == 3 and j == 2 and ic == -1:  # square 14
        return [(space + 1, 4, j) for j in range(5)]
    if i == 2 and j == 3 and jc == -1:  # square 14
        return [(space + 1, i, 4) for i in range(5)]

    # When i or j are 0 or 4, we can move to an outer space (1 neighbour)
    if i == 0 and ic == -1:
        return [(space - 1, 1, 2)]
    if j == 0 and jc == -1:
        return [(space - 1, 2, 1)]
    if i == 4 and ic == 1:
        return [(space - 1, 3, 2)]
    if j == 4 and jc == 1:
        return [(space - 1, 2, 3)]

    # Otherwise we stay in the space and just increment i and j as normal
    return [(space, i + ic, j + jc)]


# return neighbours as 3 numbers: the space (up or down 1) and position (i, j)
def recursive_neighbours(space, i, j):
    changes = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    new = [adjust_coord(space, i, j, ic, jc) for ic, jc in changes]
    return [pos for posns in new for pos in posns]


def print_board_recursive(b, space):
    for i in range(5):
        print(*[b[space, i, j] for j in range(5)], sep="")


def update_recursive(board):
    to_consider = list(board.keys())
    to_consider += [p for pos in to_consider for p in recursive_neighbours(*pos)]
    new_board = defaultdict(int)
    for pos in to_consider:
        new_board[pos] = board[pos]
        vals = [board[x] for x in recursive_neighbours(*pos)]
        if board[pos] and sum(vals) != 1:
            new_board[pos] = 0
        if not board[pos] and sum(vals) in [1, 2]:
            new_board[pos] = 1
    return new_board


def part2(file):
    board = parse_data(file, True)
    for _ in range(200):
        board = update_recursive(board)
    return sum(board.values())
