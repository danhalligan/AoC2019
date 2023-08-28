from aoc2019.intcode import *
from collections import defaultdict
from aoc2019.helpers import input_ints
from queue import Queue
from time import sleep


def get_all(queue):
    out = []
    # sleep(0.1)
    while not queue.empty():
        out.append(queue.get_nowait())
    return out


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def spaceship(a, b):
    # like spaceship operator from ruby
    return 1 if a < b else -1 if a > b else 0


def span(x):
    x = list(x)
    return range(min(x), max(x) + 1)


def qout(q):
    return lambda x: q.put_nowait(x)


class Arcade:
    def __init__(self, file):
        self.prog = input_ints(file)
        self.prog[0] = "2"
        self.inp = Queue()
        self.score = 0
        self.arcade = Intcode(self.prog, lambda: self.inp.get())
        self.screen = defaultdict(int)

    def play(self, view=False):
        gen = self.arcade.generate()
        self.paddle = 99
        ball_pos = (-1, -1)
        while not self.arcade.halted:
            for x, y, v in zip(gen, gen, gen):
                if x == -1 and y == 0:  # score
                    self.score = v
                else:
                    if v == 3:
                        self.paddle = x
                    elif v == 4:
                        ball_pos = (x, y)
                        self.inp.put(-spaceship(ball_pos[0], self.paddle))
                    elif ball_pos == (x, y) and view:
                        self.view()
                        sleep(0.1)
                    self.screen[x, y] = v
            self.screen[x, y] = v
        return self
        # print(f"END! Score: {self.score}")

    def view(self):
        LINE_UP = "\033[1A"
        LINE_CLEAR = "\x1b[2K"
        tile = {
            0: " ",  # empty
            1: "\u2588",  # wall
            2: "\u2610",  # block
            3: "\u2594",  # paddle
            4: "o",  # ball
        }
        xr = span(x[0] for x in self.screen.keys())
        yr = span(x[1] for x in self.screen.keys())
        for _ in range(28):
            print(LINE_UP, end=LINE_CLEAR)
        for j in yr:
            print("".join(tile[self.screen[i, j]] for i in xr))
        print(f"{self.score}\n")
