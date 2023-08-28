from aoc2019.helpers import input_ints
from aoc2019.intcode2 import *
from functools import reduce
from itertools import permutations
from queue import Queue
import threading


def amplifier(prog, input):
    out = Queue()
    Intcode(prog, listin(input)).run(qout(out))
    return out.get_nowait()


def amplify(prog, phases):
    return reduce(lambda a, b: amplifier(prog, [b, a]), phases, 0)


def part1(file):
    prog = input_ints(file)
    return max(amplify(prog, perm) for perm in permutations([0, 1, 2, 3, 4]))


def amplify2(prog, phases):
    qs = [Queue() for _ in phases]
    for b, p in zip(qs, phases):
        b.put(p)
    qs[0].put(0)
    amps = [Intcode(prog, qin(qs[i])) for i in range(5)]
    threads = []
    for i in range(5):
        thread = threading.Thread(target=amps[i].run, args=[qout(qs[(i + 1) % 5])])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return qs[0].get_nowait()


def part2(file):
    prog = input_ints(file)
    return max(amplify2(prog, perm) for perm in permutations(range(5, 10)))
