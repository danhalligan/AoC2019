import aoc2019.santadroid
from itertools import combinations
import re


# I built the map manually (PNG in repo!)
# Wrote code to collect all items automatically.
# Then code to try combinations of items. Turns out I needed to drop 4.
# Code will be printed to screen...
def part1(file):
    droid = aoc2019.santadroid.SantaDroid(file).collect()
    for obj in combinations(droid.objects(), 4):
        droid.drop_and_try(list(obj))
        if droid.exe.halted:
            break
    return int(re.match(".+typing\s(\d+).+", droid.output, re.DOTALL).groups()[0])
