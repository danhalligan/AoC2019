from aoc2019.intcode2 import Intcode
from aoc2019.helpers import input_ints


class Vacuum:
    def __init__(self, file):
        self.prog = input_ints(file)
        self.prog[0] = 2
        self.exe = Intcode(self.prog, inputter=self.ascii_input)
        self.pos = (0, 0)

    def input(self, main, a, b, c, video=True):
        self.write_input(main)
        self.write_input(a)
        self.write_input(b)
        self.write_input(c)
        self.write_input("y") if video else self.write_input("n")

    def write_input(self, vals):
        for x in self.as_ascii(vals):
            self.exe.input(x)

    def interactive(self):
        count = 0
        for v in self.exe.generate():
            try:
                print(chr(v), end="")
            except:
                return v
            if v == 10:
                count += 1
            if count == 42:
                print("\r\033[50A")
                count = 0

    def run(self):
        out = list(self.exe.generate())
        return out[-1]

    def as_ascii(self, x):
        return list(map(ord, list(x))) + [10]

    def ascii_input(self):
        # Add inputs to this instance as ascii codes, then return first
        if self.exe.inputs:
            return self.exe.inputs.pop(0)
        self.exe.inputs = self.as_ascii(input())
        return self.exe.inputs.pop(0)
