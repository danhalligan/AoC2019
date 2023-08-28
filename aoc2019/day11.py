from aoc2019.intcode import *
from collections import defaultdict
from aoc2019.helpers import input_ints
from queue import Queue
import threading
from advent_of_code_ocr import convert_6


def paint(prog, start_color):
    inp = Queue()
    out = Queue()
    robot = Intcode(prog, lambda: inp.get())
    thread = threading.Thread(target=robot.run, args=[qout(out)])
    thread.start()

    d, i, j = 0, 0, 0
    panels = defaultdict(int)
    inp.put(start_color)

    while thread.is_alive():
        panels[(i, j)] = out.get()
        turn = out.get()
        # print(i, j, panels[(i, j)], turn)
        d = (d - 1 if turn == 0 else (d + 1)) % 4
        j += {0: 1, 1: 0, 2: -1, 3: 0}[d]
        i += {0: 0, 1: 1, 2: 0, 3: -1}[d]
        inp.put(panels[(i, j)])

    return panels


def part1(file):
    prog = input_ints(file)
    panels = paint(prog, 0)
    return len(panels)


def span(x):
    x = list(x)
    return range(min(x), max(x) + 1)


def part2(file):
    prog = input_ints(file)
    panels = paint(prog, 1)
    ir = span(x[0] for x in panels.keys() if panels[x])
    jr = span(x[1] for x in panels.keys() if panels[x])
    txt = ["".join("#" if panels[i, j] else "." for i in ir) for j in jr]
    txt.reverse()
    txt = "\n".join(txt)
    return convert_6(txt)
