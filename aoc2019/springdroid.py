from aoc2019.intcode2 import Intcode
from aoc2019.helpers import input_ints


class SpringDroid:
    def __init__(self, file):
        self.prog = input_ints(file)
        self.exe = Intcode(self.prog, inputter=self.ascii_input)
        self.pos = (0, 0)

    def input(self, instructions, mode="WALK"):
        for inst in instructions:
            self.write_input(inst)
        self.write_input(mode)
        return self

    def interactive(self):
        for v in self.exe.generate():
            try:
                print(chr(v), end="")
            except:
                return v

    def write_input(self, vals):
        for x in self.as_ascii(vals):
            self.exe.input(x)

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
