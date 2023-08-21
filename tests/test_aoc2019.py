import importlib
import pytest

solutions = [
    {"d": 6, "p": 1, "ans": 42, "file": f"day06p1.txt"},
    {"d": 6, "p": 2, "ans": 4, "file": f"day06p2.txt"},
    {"d": 7, "p": 1, "ans": 43210, "file": f"day07a.txt"},
    {"d": 7, "p": 1, "ans": 54321, "file": f"day07b.txt"},
    {"d": 7, "p": 1, "ans": 65210, "file": f"day07c.txt"},
    {"d": 7, "p": 2, "ans": 139629729, "file": f"day07d.txt"},
    {"d": 7, "p": 2, "ans": 18216, "file": f"day07e.txt"},
]


# Test each day by importing the module and running part1 and part2
@pytest.mark.parametrize("x", solutions)
def test_all(x):
    day = f"{x['d']:02d}"
    module = importlib.import_module(f"aoc2019.day{day}")
    file = x["file"] if x["file"] else f"{day}.txt"
    path = f"tests/inputs/{file}"
    print(path)
    assert getattr(module, f"part{x['p']}")(path) == x["ans"]
