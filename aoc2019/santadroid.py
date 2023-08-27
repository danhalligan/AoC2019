from aoc2019.intcode2 import Intcode
from aoc2019.helpers import input_ints


class SantaDroid:
    def __init__(self, file):
        self.prog = input_ints(file)
        self.exe = Intcode(self.prog, inputter=self.ascii_input)
        self.pos = (0, 0)
        self.output = []

    def input(self, instructions):
        for inst in instructions:
            self.write_input(inst)
        return self

    def collect(self):
        inst = [
            "west",
            "take ornament",
            "west",
            "take astrolabe",
            "north",
            "take fuel cell",
            "south",
            "south",
            "take hologram",
            "north",
            "east",
            "south",
            "east",
            "take weather machine",
            "west",
            "north",
            "east",
            "east",
            "north",
            "take monolith",
            "south",
            "take mug",
            "south",
            "west",
            "north",
            "west",
            "take bowl of rice",
            "north",
            "west",
        ]
        self.input(inst)
        self.run(False)
        return self

    def objects(self):
        return [
            "bowl of rice",
            "monolith",
            "mug",
            "weather machine",
            "fuel cell",
            "astrolabe",
            "ornament",
            "hologram",
        ]

    def drop_and_try(self, obj):
        cmds = ["drop " + x for x in obj]
        self.input(cmds)
        self.run(False)
        cmds = ["north"]
        self.input(cmds)
        self.run(True)
        cmds += ["take " + x for x in obj]
        self.input(cmds)
        self.run(False)

    def run(self, print_output=True):
        while self.exe.inputs:
            for out in self.exe.rungame():
                if print_output:
                    print(chr(out), end="")

    def interactive(self):
        for v in self.exe.generate():
            print(chr(v), end="")

    # def interactive(self):
    #     while self.exe.inputs:
    #         out = self.exe.run_until_io_or_done()
    #         if out is not None:
    #             self.output += [out]

    def print_output(self):
        for v in self.output:
            print(chr(v), end="")

    def command(self, cmd):
        self.input([cmd])
        self.run()

    def inv(self):
        self.input(["inv"])
        self.run()

    def write_input(self, vals):
        for x in self.as_ascii(vals):
            self.exe.input(x)

    def as_ascii(self, x):
        return list(map(ord, list(x))) + [10]

    def ascii_input(self):
        # Add inputs to this instance as ascii codes, then return first
        if self.exe.inputs:
            return self.exe.inputs.pop(0)
        self.exe.inputs = self.as_ascii(input())
        return self.exe.inputs.pop(0)
