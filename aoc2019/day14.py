from collections import defaultdict
from aoc2019.helpers import input_lines
from math import floor


class Node:
    def __init__(self, inp):
        self.amount, self.chemical = inp.split(" ")
        self.amount = int(self.amount)
        self.input = []

    def __repr__(self):
        return f"Node({self.amount} {self.chemical})"


def parse(file):
    h = {}
    h["ORE"] = 0
    for line in input_lines(file):
        inp, out = line.split(" => ")
        out = Node(out)
        out.input = [Node(x) for x in inp.split(", ")]
        h[out.chemical] = out
    return h


def ore_required(h, nfuel):
    required = defaultdict(int)
    required["FUEL"] = nfuel
    produced = defaultdict(int)
    ore = 0
    while len(required):
        # puts required
        item = list(required.keys())[0]
        if required[item] <= produced[item]:
            produced[item] -= required[item]
            required.pop(item)
            next
        n_required = required[item] - produced[item]
        required.pop(item)
        produced.pop(item)
        n_produced = h[item].amount
        ratio = n_required / n_produced
        n_reactions = int(ratio if ratio == floor(ratio) else floor(ratio) + 1)
        produced[item] += (n_reactions * n_produced) - n_required
        for chem in h[item].input:
            if chem.chemical == "ORE":
                ore += chem.amount * n_reactions
            else:
                required[chem.chemical] += chem.amount * n_reactions
    return ore


def part1(file):
    inp = parse(file)
    return ore_required(inp, 1)


def part2(file):
    inp = parse(file)
    high = 1e7
    low = 1e6
    while low < high - 1:
        mid = int((low + high) / 2)
        ore = ore_required(inp, mid)
        low, high = [mid, high] if ore < 1e12 else [low, mid]
    return low
