import aoc2019.santadroid
import importlib
from itertools import combinations


# I built the map manually (PNG in repo!)
# Wrote code to collect all items automatically.
# Then code to try combinations of items. Turns out I needed to drop 4.
# Code will be printed to screen...
def part1(file):
    importlib.reload(aoc2019.santadroid)
    droid = aoc2019.santadroid.SantaDroid(file).collect()
    droid.inv()
    for obj in combinations(droid.objects(), 4):
        droid.drop_and_try(list(obj))
