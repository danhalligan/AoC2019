import importlib
import pytest
import os

solutions = [
    {"d": 1, "p": 1, "ans": 3382284},
    {"d": 1, "p": 2, "ans": 5070541},
    {"d": 2, "p": 1, "ans": 3654868},
    {"d": 2, "p": 2, "ans": 7014},
    {"d": 3, "p": 1, "ans": 1285},
    {"d": 3, "p": 2, "ans": 14228},
    {"d": 4, "p": 1, "ans": 1063},
    {"d": 4, "p": 2, "ans": 686},
    {"d": 5, "p": 1, "ans": 16489636},
    {"d": 5, "p": 2, "ans": 9386583},
    {"d": 6, "p": 1, "ans": 333679},
    {"d": 6, "p": 2, "ans": 370},
    {"d": 7, "p": 1, "ans": 199988},
    {"d": 7, "p": 2, "ans": 17519904},
    {"d": 8, "p": 1, "ans": 2318},
    {"d": 8, "p": 2, "ans": "AHFCB"},
    {"d": 9, "p": 1, "ans": 2682107844},
    {"d": 9, "p": 2, "ans": 34738},
    {"d": 10, "p": 1, "ans": 256},
    {"d": 10, "p": 2, "ans": 1707},
    {"d": 11, "p": 1, "ans": 2160},
    {"d": 11, "p": 2, "ans": "LRZECGFE"},
    {"d": 12, "p": 1, "ans": 12644},
    {"d": 12, "p": 2, "ans": 290314621566528},
    {"d": 13, "p": 1, "ans": 369},
    {"d": 13, "p": 2, "ans": 19210},
    {"d": 14, "p": 1, "ans": 469536},
    {"d": 14, "p": 2, "ans": 3343477},
    {"d": 15, "p": 1, "ans": 228},
    {"d": 15, "p": 2, "ans": 348},
    {"d": 16, "p": 1, "ans": 73127523},
    {"d": 16, "p": 2, "ans": 80284420},
    {"d": 17, "p": 1, "ans": 8408},
    {"d": 17, "p": 2, "ans": 1168948},
    {"d": 18, "p": 1, "ans": 4250},
    {"d": 18, "p": 2, "ans": 1640},
    {"d": 19, "p": 1, "ans": 150},
    {"d": 19, "p": 2, "ans": 12201460},
    {"d": 20, "p": 1, "ans": 664},
    {"d": 20, "p": 2, "ans": 7334},
    {"d": 21, "p": 1, "ans": 19357534},
    {"d": 21, "p": 2, "ans": 1142814363},
    {"d": 22, "p": 1, "ans": 1879},
    {"d": 22, "p": 2, "ans": 73729306030290},
    {"d": 23, "p": 1, "ans": 18604},
    {"d": 23, "p": 2, "ans": 11880},
    {"d": 24, "p": 1, "ans": 17863711},
    {"d": 24, "p": 2, "ans": 1937},
    {"d": 25, "p": 1, "ans": 1073874948},
]

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


def id_func(param):
    return f"Day {param['d']}, part {param['p']}"


# Test each day by importing the module and running part1 and part2
@pytest.mark.parametrize("x", solutions, ids=id_func)
@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Requires real inputs")
def test_all(x):
    day = f"{x['d']:02d}"
    module = importlib.import_module(f"aoc2019.day{day}")
    path = f"inputs/day{day}.txt"
    assert getattr(module, f"part{x['p']}")(path) == x["ans"]
