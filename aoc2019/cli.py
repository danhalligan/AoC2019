import typer
import re
from importlib import import_module
import os
import requests
from pathlib import Path
from typing import List
from datetime import date

app = typer.Typer()


def get_part(day, part):
    module = import_module(f"aoc2019.day{day:02d}")
    return getattr(module, f"part{part}")


@app.command("solve")
def solve(files: List[Path]):
    """Solve a challenges based on filename"""
    for path in files:
        if path.is_file():
            day = int(re.findall(r"\d+", path.name)[0])
            print(f"--- Day {day} ---")
            for part in [1, 2]:
                try:
                    print(f"Part {part}:", get_part(day, part)(path))
                except AttributeError:
                    print(f"No part {part}")
            print()


@app.command("input")
def input(day: int = date.today().day):
    """Download AoC input file (for today by default)"""
    print(f"Downloading https://adventofcode.com/2019/day/{day}/input")
    if "AOC_SESSION" not in os.environ and os.path.exists(".session.txt"):
        os.environ["AOC_SESSION"] = open(".session.txt").read().rstrip()
    res = requests.get(
        f"https://adventofcode.com/2019/day/{day}/input",
        cookies={"session": os.environ.get("AOC_SESSION")},
    )
    file = f"inputs/day{day:02d}.txt"
    with open(file, "w") as f:
        f.write(res.text)
    return file


def main():
    app()
