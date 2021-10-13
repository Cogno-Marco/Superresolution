import os
import random
import sys
import cProfile
import numpy as np
import matplotlib.pyplot as plt

from typing import List
from src.world import World
from matplotlib.ticker import MaxNLocator


# registration algorithm:
# compare each macropixel of a photo with a macropixel of the world at an offset
# compute the product of all macropixels values (p if white, 1-p if black)
# the final value is the probability that the photo was taken at that offset
# the final registration offset is the offset where the product is highest

# to check that the algorithm works we show that:
# 1. probability at the offset where the photo was taken > probability at other offsets
# 2. as k increases we're less likely to guess a wrong offset compared to the one where the photo was actually taken


def calculate_probability(world: World, photo: np.ndarray, offset: int, resolution: int) -> int:
    macros = world.macros(offset, resolution)
    # Where photo is different from 1, I have to multiply for
    # (resolution - pixel) instead of pixel.
    macros[photo != 1] = resolution - macros[photo != 1]
    return int(np.prod(macros.astype(object)))


def guess_offset(world: World, photo: np.ndarray, resolution: int) -> int:
    # calculate the product probability
    # N.B. using float the probability gets squished to 0.0 due to the high amount of macropixels
    # using bigints we can avoid the problem, so instead of calculating the actual probability
    # we only calculate the numerator, since the denominator is always r^k which we can ignore
    # since the argmax doesn't get affected
    probabilities = [calculate_probability(world, photo, i, resolution) for i in range(0, resolution + 1)]
    return np.argmax(probabilities)


def benchmark_guessing_probability(k: int, r: int, trials: int = 100) -> List[int]:
    """
    Tests the probability to guess correctly at each offset given some parameters
    Returns the number of guesses at each offset as a list
    The index of the list is the relative offset tested
    L[0] is the number of times the offset was correctly guessed
    L[1:] is the number of times the offset was wrongly guessed at offset 1 to r (included)
    """
    guesses: List[int] = [0] * (r + 1)  # record wrong guesses ad relative offset distance
    for _ in range(trials):
        f: int = random.randint(0, r)
        world: World = World(2 * k * r, 1, 0.5)
        photo = world.picture(f, r)

        guess = guess_offset(world, photo, r)
        guesses[abs(f - guess)] += 1

        # print(f"{world=}")
        # print(f"{photo=}")
        # print(f"guessed position: {guess} actual offset: {f}")

    return guesses


def main():
    # test for each k the number of times the photo is correctly guessed,
    # we expect to see this value increase as k increases

    # world setup
    r: int = 16
    trials: int = 1000
    min_k = 1
    max_k = 3000
    k_step = 4

    probability_as_k_increases: List[float] = [0] * int(((max_k + 1) - min_k) / k_step)
    k_to_test = range(min_k, max_k + 1, k_step)
    for i, k in enumerate(k_to_test):
        percentage = round(i / len(k_to_test) * 100, 2)
        print(f"Current k: {k}, {percentage}%             ", end="\r")
        guesses = benchmark_guessing_probability(k, r, trials)
        probability_as_k_increases[i] = guesses[0] / trials

    print(f"{probability_as_k_increases=}")

    fig, ax = plt.subplots()
    ax.plot(k_to_test, probability_as_k_increases)

    ax.set(xlabel=f'camera size (k)', ylabel='probability (p)',
           title=f'Probability to guess correctly photos offset as k increases (r={r})')

    ax.grid()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.ylim(bottom=0)
    plt.xlim(left=min_k, right=max_k)
    plt.show()


if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()
    pr.dump_stats("test.prof")
    os.system("snakeviz test.prof")
