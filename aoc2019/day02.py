from aoc2019.helpers import input_ints


def intcode(p):
    ptr = 0
    while ptr < len(p):
        opcode = p[ptr]
        if opcode == 1:
            a, b, o = p[ptr + 1 : ptr + 4]
            p[o] = p[a] + p[b]
        elif opcode == 2:
            a, b, o = p[ptr + 1 : ptr + 4]
            p[o] = p[a] * p[b]
        elif opcode == 99:
            break
        else:
            raise Exception(f"Opcode {opcode} not recognised")
        ptr += 4
    return p


def part1(file):
    x = input_ints(file)
    x[1] = 12
    x[2] = 2
    return intcode(x)[0]


def part2(file):
    x = input_ints(file)
    for noun in range(100):
        for verb in range(100):
            test = x.copy()
            test[1] = noun
            test[2] = verb
            if intcode(test)[0] == 19690720:
                return 100 * noun + verb
