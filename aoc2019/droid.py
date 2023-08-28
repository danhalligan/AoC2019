from aoc2019.intcode import Intcode, qout
from aoc2019.helpers import input_ints
from queue import Queue
import threading


class Droid:
    def __init__(self, file):
        self.prog = input_ints(file)
        self.inp = Queue()
        self.out = Queue()
        self.exe = Intcode(
            self.prog,
            lambda: self.inp.get(),
        )
        self.area = {}
        self.pos = (0, 0)
        self.area[self.pos] = 1
        self.path = []
        self.stop = False

    def start(self):
        self.thread = threading.Thread(target=self.exe.run, args=[qout(self.out)])
        self.thread.start()
        return self

    def kill(self):
        self.exe.halted = True
        self.inp.put(99)
        return self

    # Attempt to move the droid by issuing command to intcode executable
    def move(self, command):
        if command not in [1, 2, 3, 4]:
            raise Exception("command not valid")
        self.inp.put(command)
        res = self.out.get()
        if res == 0:
            self.area[self.newpos(self.pos, command)] = 0
        elif res in [1, 2]:
            self.path += [command]
            self.pos = self.newpos(self.pos, command)
            self.area[self.pos] = res
            # if res == 2:
            #     print(f"Found oxygen: {command} {self.pos} {len(self.path)}")
        return res

    def unmove(self):
        last = self.path.pop()
        res = self.move(self.reverse(last))
        self.path.pop()
        return res

    # Return moves from given position that are unknown or not walls
    def possible_moves(self, pos=None):
        if pos == None:
            pos = self.pos
        return [
            m
            for m in range(1, 5)
            if self.newpos(pos, m) not in self.area
            or self.area[self.newpos(pos, m)] != 0
        ]

    def print_value(self, i, j):
        if self.pos == (i, j):
            return "D"
        elif (i, j) in self.area:
            return {0: "#", 1: ".", 2: "O"}[self.area[i, j]]
        else:
            return " "

    def print_area(self):
        ks = [k for k, v in self.area.items() if v is not None]
        ir = self.span(x[0] for x in ks + [self.pos])
        jr = self.span(x[1] for x in ks + [self.pos])
        for j in jr:
            txt = [self.print_value(i, j) for i in ir]
            print("".join(txt))

    # Probe each possible direction from current position
    # (reversing if the droid moves)
    # and return valid moves -- definitely not walls and not steps back
    def foward_moves(self):
        for v in self.possible_moves():
            res = self.move(v)
            if res in [1, 2]:
                self.unmove()
        poss = self.possible_moves()
        if self.path:
            poss.remove(self.reverse(self.path[-1]))  # remove backward step
        return poss

    def explore(self):
        poss = self.foward_moves()
        if len(poss):
            for v in poss:
                self.move(v)
                self.explore()
                self.unmove()
        return self

    @staticmethod
    def span(x):
        x = list(x)
        return range(min(x), max(x) + 1)

    @staticmethod
    def newpos(p, d):
        if d == 1:
            return (p[0], p[1] - 1)
        elif d == 2:
            return (p[0], p[1] + 1)
        elif d == 3:
            return (p[0] - 1, p[1])
        elif d == 4:
            return (p[0] + 1, p[1])

    @staticmethod
    def reverse(move):
        return {1: 2, 2: 1, 3: 4, 4: 3}[move]
