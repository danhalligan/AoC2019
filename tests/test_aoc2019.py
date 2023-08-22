import importlib
import pytest

solutions = [
    {"d": 6, "p": 1, "ans": 42, "file": "day06p1.txt"},
    {"d": 6, "p": 2, "ans": 4, "file": "day06p2.txt"},
    {"d": 7, "p": 1, "ans": 43210, "file": "day07a.txt"},
    {"d": 7, "p": 1, "ans": 54321, "file": "day07b.txt"},
    {"d": 7, "p": 1, "ans": 65210, "file": "day07c.txt"},
    {"d": 7, "p": 2, "ans": 139629729, "file": "day07d.txt"},
    {"d": 7, "p": 2, "ans": 18216, "file": "day07e.txt"},
    {"d": 10, "p": 1, "ans": 8, "file": "day10a.txt"},
    {"d": 10, "p": 1, "ans": 33, "file": "day10b.txt"},
    {"d": 10, "p": 1, "ans": 35, "file": "day10c.txt"},
    {"d": 10, "p": 1, "ans": 41, "file": "day10d.txt"},
    {"d": 10, "p": 1, "ans": 210, "file": "day10e.txt"},
    {"d": 12, "p": 1, "ans": 179, "file": "day12.txt", "args": {"steps": 10}},
    {"d": 12, "p": 1, "ans": 1940, "file": "day12b.txt", "args": {"steps": 100}},
    {"d": 12, "p": 2, "ans": 2772, "file": "day12.txt"},
    {"d": 12, "p": 2, "ans": 4686774924, "file": "day12b.txt"},
]


# Test each day by importing the module and running part1 and part2
@pytest.mark.parametrize("x", solutions)
def test_all(x):
    day = f"{x['d']:02d}"
    module = importlib.import_module(f"aoc2019.day{day}")
    file = x["file"] if x["file"] else f"{day}.txt"
    path = f"tests/inputs/{file}"
    if "args" in x:
        assert getattr(module, f"part{x['p']}")(path, **x["args"]) == x["ans"]
    else:
        assert getattr(module, f"part{x['p']}")(path) == x["ans"]
