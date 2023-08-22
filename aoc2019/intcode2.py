from itertools import count
from collections import defaultdict
from queue import Queue
import inspect


def qin(q):
    return lambda: q.get(True, 2)


def qout(q):
    return lambda x: q.put_nowait(x)


def readint():
    print("Enter input: ", end="")
    return int(input())


def listin(data):
    inp = Queue()
    [inp.put(v) for v in data]
    return qin(inp)


def basic_intcode(prog, input):
    out = Queue()
    Intcode(prog, listin(input), qout(out)).run()
    return out.get_nowait()


class Position:
    # Get or set a value at a given memory position given a mode

    def __init__(self, mem, relbase, position, mode):
        self.mem = mem
        self.rb = relbase
        self.p = position
        self.m = mode

    def get(self):
        if self.m == 0:
            return self.mem[self.p]
        elif self.m == 1:
            return self.p
        elif self.m == 2:
            return self.mem[self.rb + self.p]
        else:
            raise Exception(f"Error! Unknown get mode {self.m}")

    def put(self, value):
        if self.m == 0:
            self.mem[self.p] = value
        elif self.m == 2:
            self.mem[self.rb + self.p] = value
        else:
            raise Exception(f"Error! Unknown set mode {self.m}")


class Operation:
    # Perform an operation given an opcode and parameters
    def __init__(self, opcode, relbase, inputter=readint, outputter=print):
        self.operation = getattr(self, f"op{opcode}")
        self.relbase = relbase
        self.inputter = inputter
        self.outputter = outputter

    def nparam(self):
        return len(inspect.getargspec(self.operation)[0]) - 1

    def run(self, params):
        return self.operation(*params)

    def op1(self, a, b, c):
        c.put(a.get() + b.get())

    def op2(self, a, b, c):
        c.put(a.get() * b.get())

    def op3(self, a):
        a.put(self.inputter())

    def op4(self, a):
        self.outputter(a.get())

    def op5(self, a, b):
        if a.get() != 0:
            return b.get()

    def op6(self, a, b):
        if a.get() == 0:
            return b.get()

    def op7(self, a, b, c):
        c.put(1 if a.get() < b.get() else 0)

    def op8(self, a, b, c):
        c.put(1 if a.get() == b.get() else 0)

    def op9(self, a):
        self.relbase += a.get()


class Intcode:
    _ids = count(0)

    def __init__(self, program, inputter=readint, outputter=print):
        self.program = defaultdict(int)
        for v, x in enumerate(program):
            self.program[v] = x
        self.ptr = 0
        self.inputter = inputter
        self.outputter = outputter
        self.id = next(self._ids)
        self.relbase = 0

    def parse_opcode(self, code):
        x = list(str(code).rjust(5, "0"))
        op = int("".join(x[-2:]))
        modes = [int(v) for v in x[0:-2][::-1]]
        return op, modes

    def run(self):
        while self.ptr < len(self.program):
            opcode, modes = self.parse_opcode(self.program[self.ptr])
            # print(f"[{self.id}] op:{opcode}, modes:{modes} relbase:{self.relbase}")
            if opcode == 99:
                self.halted = True
                return
            op = Operation(opcode, self.relbase, self.inputter, self.outputter)
            prange = range(self.ptr + 1, self.ptr + op.nparam() + 1)
            pos = [
                Position(self.program, self.relbase, self.program[p], m)
                for p, m in zip(prange, modes)
            ]
            ptr = op.run(pos)
            self.ptr = ptr if ptr else self.ptr + op.nparam() + 1
            self.relbase = op.relbase
