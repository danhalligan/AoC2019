from aoc2019.helpers import input_ints


def parse_opcode(code):
    x = list(str(code).rjust(5, "0"))
    op = int("".join(x[-2:]))
    modes = [int(v) for v in x[0:-2][::-1]]
    return op, modes


def intcode(program, input):
    def getv(mode, v):
        return program[v] if mode == 0 else v

    ptr = 0
    while ptr < len(program):
        # input()
        opcode, modes = parse_opcode(program[ptr])
        # print(ptr, program[ptr], opcode, modes)
        if opcode == 1:
            a, b, o = program[ptr + 1 : ptr + 4]
            # print(getv(modes[0], a), getv(modes[1], b))
            program[o] = getv(modes[0], a) + getv(modes[1], b)
            ptr += 4
        elif opcode == 2:
            a, b, o = program[ptr + 1 : ptr + 4]
            program[o] = getv(modes[0], a) * getv(modes[1], b)
            ptr += 4
        elif opcode == 3:
            a = program[ptr + 1]
            program[a] = input
            ptr += 2
        elif opcode == 4:
            o = program[ptr + 1]
            yield getv(modes[0], o)
            ptr += 2
        elif opcode == 5:
            a, b = program[ptr + 1 : ptr + 3]
            if getv(modes[0], a) != 0:
                ptr = getv(modes[1], b)
            else:
                ptr += 3
        elif opcode == 6:
            a, b = program[ptr + 1 : ptr + 3]
            if getv(modes[0], a) == 0:
                ptr = getv(modes[1], b)
            else:
                ptr += 3
        elif opcode == 7:
            a, b, o = program[ptr + 1 : ptr + 4]
            program[o] = 1 if getv(modes[0], a) < getv(modes[1], b) else 0
            ptr += 4
        elif opcode == 8:
            a, b, o = program[ptr + 1 : ptr + 4]
            program[o] = 1 if getv(modes[0], a) == getv(modes[1], b) else 0
            ptr += 4
        elif opcode == 99:
            break
        else:
            raise Exception("Error!")


def part1(file):
    prog = input_ints(file)
    return list(intcode(prog, 1))[-1]


def part2(file):
    prog = input_ints(file)
    return list(intcode(prog, 5))[0]
