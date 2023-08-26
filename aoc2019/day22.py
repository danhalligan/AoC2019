from aoc2019.helpers import input_lines
import re


# reverse
def dns(deck):
    return deck[::-1]


# cut N
def cut(deck, n):
    return deck[n:] + deck[:n]


# deal with increment n
def dwi(deck, n):
    new = deck[:]
    for i, card in enumerate(deck):
        new[i * n % len(deck)] = card
    return new


def part1(file):
    deck = list(range(10006 + 1))

    for line in input_lines("inputs/day22.txt"):
        if line.startswith("deal into new"):
            deck = dns(deck)
        elif line.startswith("deal with increment"):
            deck = dwi(deck, int(re.findall("-*\d+", line)[0]))
        elif line.startswith("cut"):
            deck = cut(deck, int(re.findall("-*\d+", line)[0]))

    return deck.index(2019)


# It is at this point that I gracefully bow out and cheat.
# https://www.reddit.com/r/adventofcode/comments/ee0rqi/comment/fbnifwk
# https://www.reddit.com/r/adventofcode/comments/ee0rqi/comment/fbnif4d/


# return (position of p, number at position p)
# after shuffling the deck of 'sz' cards 'reps' times (with shuf)
# We use that both are a linear function of p (second inverse of first):
# if p1-p0=x then position of p after 1 rep is p0 + x*p  (mod sz)
# and number at position p is (pos-p0) * (x**-1)  (mod sz)
# rep 2: p0*(1 + x + x**2) + (x**2)(p-p0)
def num_at_pos(sz, reps, shuf, p):
    p0, p1 = 0, 1
    for line in shuf:
        if line.endswith("stack"):
            # reverse: 0 => sz-1
            p0 = ~p0
            p1 = ~p1
        elif line.startswith("cut"):
            n = int(line.split()[-1])
            p0 -= n
            p1 -= n
        else:
            n = int(line.split()[-1])
            p0 *= n % sz
            p1 *= n % sz
    x = p1 - p0
    # Use the identity x^n+...+x^2+x+1 = (x^(n+1)-1)//(x-1)
    x_reps = pow(x, reps, sz)
    #   p0 * (x^(n+1) -1) * ((x-1)**-1)
    dx = p0 * ((x_reps * x - 1) * pow(x - 1, -1, sz)) % sz
    pos_of_p = (dx + x_reps * (p - p0)) % sz
    # invert the permutation
    num_at_p = ((p - dx) * pow(x_reps, -1, sz) + p0) % sz
    return pos_of_p, num_at_p


def part2(file):
    lines = input_lines("inputs/day22.txt")
    # print("Verify part 1:", num_at_pos(10007, 1, lines, 2019)[0])
    return num_at_pos(119315717514047, 101741582076661, lines, 2020)[1]
