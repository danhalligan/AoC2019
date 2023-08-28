from aoc2019.intcode2 import Intcode
from aoc2019.helpers import input_ints


class SantaDroid:
    def __init__(self, file):
        self.prog = input_ints(file)
        self.exe = Intcode(self.prog, inputter=self.ascii_input)
        self.pos = (0, 0)
        self.output = ""

    def collect(self):
        cmds = [
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
        for cmd in cmds:
            self.command(cmd)
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
        for x in obj:
            self.drop(x)
        self.command("north")
        for x in obj:
            self.take(x)

    def drop(self, obj):
        self.command("drop " + obj)

    def take(self, obj):
        self.command("take " + obj)

    def run(self):
        while self.exe.inputs and not self.exe.halted:
            for out in self.exe.rungame():
                self.output += chr(out)

    def command(self, cmd):
        self.write_input(cmd)
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
