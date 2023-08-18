import importlib
import pytest

solutions = [
    (1, [24000, 45000], [{}, {}]),
]


# Test each day by importing the module and running part1 and part2
@pytest.mark.parametrize("day,expected,extra", solutions)
def test_all(day, expected, extra):
    module = importlib.import_module(f"aoc2019.day{day:02d}")
    file = "tests/inputs/day" + f"{day:02d}" + ".txt"
    assert getattr(module, "part1")(file, **extra[0]) == expected[0]
    assert getattr(module, "part2")(file, **extra[1]) == expected[1]
