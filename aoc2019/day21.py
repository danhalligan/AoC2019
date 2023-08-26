import aoc2019.springdroid
import importlib


def part1(file):
    sd = aoc2019.springdroid.SpringDroid("inputs/day21.txt")
    # We always jump 4 places
    # !C means C is a hole
    # Jump if (!C & D) | (!A)
    return sd.input(
        [
            "NOT C J",  # C is a hole - we can jump and land on D if solid
            "AND D J",  # D is solid!
            "NOT A T",  # there's a hole immediately next
            "OR T J",  # OR with second statement
        ],
        mode="WALK",
    ).run()


# Must jump:
#    ABCDEFGHI
# 1. _********    hole next, so must always jump
# 2. **_*__***    we can land on the island
# 3. *__*_****    we can land on the island
# 4. _*_**__**    we can land on the island
# 5. ___******
# 6. *_**_****

# Must not jump:
# 7. **_*__**
# 8. ****__*__*
# 9. ***_         we won't land safe


def part2(file):
    sd = aoc2019.springdroid.SpringDroid("inputs/day21.txt")
    # D && (!A | !B | (!C & (!F | H))
    return sd.input(
        [
            # Rule 1
            "NOT A J",
            # includes rules 2-5, excludes 7
            "NOT C T",
            "AND H T",
            "OR T J",
            # includes 6, excludes 8
            "NOT B T",
            "AND A T",
            "AND C T",
            "OR T J",
            # jump only if we can land safely
            "AND D J",
        ],
        mode="RUN",
    ).run()
