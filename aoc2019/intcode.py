from itertools import count
from collections import defaultdict
from queue import Queue


def qin(q, wait=2):
    return lambda: q.get(True, wait)


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


class Intcode:
    _ids = count(0)

    def __init__(self, program, inputter=None, outputter=None, ascii_mode=False):
        self.program = defaultdict(int)
        for v, x in enumerate(program):
            self.program[v] = x
        self.ptr = 0
        self.id = next(self._ids)
        self.relative_base = 0
        self.halted = False
        self.ascii_mode = ascii_mode
        if outputter is None:
            if ascii_mode:
                outputter = lambda x: print(x, end="")
            else:
                outputter = print
        self.outputter = outputter
        if inputter is None:
            if ascii_mode:
                inputter = input
            else:
                inputter = readint
        self.inputter = inputter

    def parse_opcode(self, code):
        x = list(str(code).rjust(5, "0"))
        op = int("".join(x[-2:]))
        modes = [int(v) for v in x[0:-2][::-1]]
        return op, modes

    def getv(self, mode, pos):
        if mode == 0:
            return self.program[pos]
        elif mode == 1:
            return pos
        elif mode == 2:
            return self.program[self.relative_base + pos]
        else:
            raise Exception(f"Error! Unknown get mode {mode}")

    def setv(self, mode, pos, val):
        if mode == 0:
            self.program[pos] = val
        elif mode == 2:
            self.program[self.relative_base + pos] = val
        else:
            raise Exception(f"Error! Unknown set mode {mode}")

    def params(self, n):
        return [self.program[i] for i in range(self.ptr + 1, self.ptr + 1 + n)]

    def run(self, kill_signal=None):
        self.kill_signal = kill_signal
        while self.ptr < len(self.program):
            opcode, modes = self.parse_opcode(self.program[self.ptr])
            # print(f"[{self.id}] op:{opcode}, modes:{modes}")
            if opcode == 99 or self.halted:
                self.halted = True
                return
            elif opcode in range(10):
                getattr(self, f"op{opcode}")(modes)
            else:
                raise Exception(f"Error! Unknown op code {opcode}")

    def gen(self, kill_signal=None):
        self.outputter = lambda x: None
        self.kill_signal = kill_signal
        while self.ptr < len(self.program):
            opcode, modes = self.parse_opcode(self.program[self.ptr])
            # print(f"[{self.id}] op:{opcode}, modes:{modes}")
            if opcode == 99:
                self.halted = True
                return
            elif opcode in range(10):
                out = getattr(self, f"op{opcode}")(modes)
                if out is not None:
                    yield out
            else:
                raise Exception(f"Error! Unknown op code {opcode}")

    def op1(self, modes):
        a, b, c = self.params(3)
        self.setv(modes[2], c, self.getv(modes[0], a) + self.getv(modes[1], b))
        self.ptr += 4

    def op2(self, modes):
        a, b, c = self.params(3)
        self.setv(modes[2], c, self.getv(modes[0], a) * self.getv(modes[1], b))
        self.ptr += 4

    def op3(self, modes):
        a = self.params(1)[0]
        val = self.inputter()
        if self.ascii_mode:
            val = ord(val)
        if self.kill_signal is not None and val == self.kill_signal:
            self.halted = True
            return
        # print(f"[{self.id}] read value {val}")
        self.setv(modes[0], a, val)
        self.ptr += 2

    def op4(self, modes):
        val = self.params(1)[0]
        out = self.getv(modes[0], val)
        # print(f"[{self.id}] writing {self.getv(modes[0], val)}")
        if self.ascii_mode:
            out = chr(out)
        self.outputter(out)
        self.ptr += 2
        return out

    def op5(self, modes):
        a, b = self.params(2)
        if self.getv(modes[0], a) != 0:
            self.ptr = self.getv(modes[1], b)
        else:
            self.ptr += 3

    def op6(self, modes):
        a, b = self.params(2)
        if self.getv(modes[0], a) == 0:
            self.ptr = self.getv(modes[1], b)
        else:
            self.ptr += 3

    def op7(self, modes):
        a, b, c = self.params(3)
        val = 1 if self.getv(modes[0], a) < self.getv(modes[1], b) else 0
        self.setv(modes[2], c, val)
        self.ptr += 4

    def op8(self, modes):
        a, b, c = self.params(3)
        val = 1 if self.getv(modes[0], a) == self.getv(modes[1], b) else 0
        self.setv(modes[2], c, val)
        self.ptr += 4

    def op9(self, modes):
        a = self.params(1)[0]
        self.relative_base += self.getv(modes[0], a)
        self.ptr += 2
