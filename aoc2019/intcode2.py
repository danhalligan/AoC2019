from itertools import count
from collections import defaultdict
from aoc2019.helpers import input_ints
from copy import copy


# takes input (file name) and returns output as a list
class SimpleIntcode:
    def __init__(self, file, inp):
        self.prog = input_ints(file)
        self.exe = Intcode(self.prog).input(inp)

    def run(self):
        return list(self.exe.generate())


class Intcode:
    _ids = count(0)

    def __init__(self, program, inputter=lambda: int(input())):
        program = copy(program)
        self.program = defaultdict(int)
        for v, x in enumerate(program):
            self.program[v] = x
        self.ptr = 0
        self.relbase = 0
        self.id = next(self._ids)
        self.halted = False
        self.inputs = []
        self.inputter = inputter
        self.output = None

    def generate(self):
        while self.ptr < len(self.program) and not self.halted:
            opcode, modes = self.parse_opcode(self.program, self.ptr)
            Operation(opcode, modes).run(self)
            if self.output is not None:
                yield self.output
                self.output = None

    def run(self, outputter=lambda x: print(x)):
        for output in self.generate():
            outputter(output)

    def run_until_input_or_done(self):
        return self.runpause(False, True)

    def run_until_io_or_done(self):
        return self.runpause(True, True)

    # Run get one input then stop
    def runpause(self, stop_on_output=True, stop_on_input=False):
        self.paused = False
        while self.ptr < len(self.program) and not self.halted:
            opcode, modes = self.parse_opcode(self.program, self.ptr)
            Operation(opcode, modes).run(self)
            if opcode == 3:
                self.paused = True
                if stop_on_input:
                    break
            elif opcode == 4:
                if stop_on_output:
                    break
        return self.output

    def input(self, value):
        value = [value] if not isinstance(value, list) else value
        self.inputs += value
        return self

    def get_input(self):
        return self.inputs.pop(0) if self.inputs else self.inputter()

    @classmethod
    def from_file(cls, file, inputs=[], inputter=lambda: int(input())):
        return cls(input_ints(file), inputs, inputter)

    @staticmethod
    def parse_opcode(program, ptr):
        code = program[ptr]
        x = list(str(code).rjust(5, "0"))
        opcode = int("".join(x[-2:]))
        modes = [int(v) for v in x[0:-2][::-1]]
        return opcode, modes


class Operation:
    _nparam = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0}

    # Perform an operation given an opcode and parameters
    def __init__(self, opcode, modes):
        self.opcode, self.modes = opcode, modes
        self.moved_ptr = False

    def nparam(self):
        return self._nparam[self.opcode]

    def run(self, exe):
        fn = getattr(self, f"op{self.opcode}")
        fn(exe, *self.params(exe))
        if not self.moved_ptr:
            exe.ptr += self.nparam() + 1

    def params(self, exe):
        ran = range(exe.ptr + 1, exe.ptr + self.nparam() + 1)
        return [Param(exe, p, m) for p, m in zip(ran, self.modes)]

    def op1(self, _, a, b, c):  # adds
        c.put(a.get() + b.get())

    def op2(self, _, a, b, c):  # multiplies
        c.put(a.get() * b.get())

    def op3(self, exe, a):  # input
        a.put(exe.get_input())

    def op4(self, exe, a):  # output
        exe.output = a.get()

    def op5(self, exe, a, b):  # jump-if-true
        if a.get() != 0:
            exe.ptr = b.get()
            self.moved_ptr = True

    def op6(self, exe, a, b):  # jump-if-false
        if a.get() == 0:
            exe.ptr = b.get()
            self.moved_ptr = True

    def op7(self, _, a, b, c):  # less than
        c.put(1 if a.get() < b.get() else 0)

    def op8(self, _, a, b, c):  # equals
        c.put(1 if a.get() == b.get() else 0)

    def op9(self, exe, a):  # adjusts the relative base
        exe.relbase += a.get()

    def op99(self, exe):  # halt program
        exe.halted = True


class Param:
    # Get or set a value at a given memory position given a mode

    def __init__(self, exe, ptr, mode):
        self.program = exe.program
        self.address = self.program[ptr]
        self.mode = mode
        if self.mode == 2:
            self.address += exe.relbase

    def get(self):
        if self.mode == 1:
            return self.address
        else:
            return self.program[self.address]

    def put(self, value):
        self.program[self.address] = value
