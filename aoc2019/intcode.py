from itertools import count


def readint():
    print("Enter input: ", end="")
    return int(input())


class Intcode:
    _ids = count(0)

    def __init__(self, program, inputter=readint, outputter=print):
        self.program = program.copy()
        self.ptr = 0
        self.inputter = inputter
        self.outputter = outputter
        self.id = next(self._ids)

    def parse_opcode(self, code):
        x = list(str(code).rjust(5, "0"))
        op = int("".join(x[-2:]))
        modes = [int(v) for v in x[0:-2][::-1]]
        return op, modes

    def getv(self, mode, v):
        return self.program[v] if mode == 0 else v

    def params(self, n):
        return self.program[self.ptr + 1 : self.ptr + 1 + n]

    def run(self):
        while self.ptr < len(self.program):
            opcode, modes = self.parse_opcode(self.program[self.ptr])
            # print(f"[{self.id}] op:{opcode}, modes:{modes}")
            if opcode == 99:
                self.halted = True
                return
            elif opcode in range(9):
                getattr(self, f"op{opcode}")(modes)
            else:
                raise Exception(f"Error! Unknown op code {opcode}")

    def op1(self, modes):
        a, b, o = self.params(3)
        self.program[o] = self.getv(modes[0], a) + self.getv(modes[1], b)
        self.ptr += 4

    def op2(self, modes):
        a, b, o = self.params(3)
        self.program[o] = self.getv(modes[0], a) * self.getv(modes[1], b)
        self.ptr += 4

    def op3(self, modes):
        a = self.params(1)[0]
        val = self.inputter()
        # print(f"[{self.id}] read value {val}")
        self.program[a] = val
        self.ptr += 2

    def op4(self, modes):
        val = self.params(1)[0]
        # print(f"[{self.id}] writing {self.getv(modes[0], val)}")
        self.outputter(self.getv(modes[0], val))
        self.ptr += 2

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
        a, b, o = self.params(3)
        self.program[o] = 1 if self.getv(modes[0], a) < self.getv(modes[1], b) else 0
        self.ptr += 4

    def op8(self, modes):
        a, b, o = self.params(3)
        self.program[o] = 1 if self.getv(modes[0], a) == self.getv(modes[1], b) else 0
        self.ptr += 4
