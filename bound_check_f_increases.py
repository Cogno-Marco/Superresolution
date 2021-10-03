from general.world_1d import World_1d
from general.photo_1d import Photo_1d
import matplotlib.pyplot as plt
from typing import List
import random

# registration algorithm:
# compare each macropixel of a photo with a macropixel of the world at an offset
# compute the product of all macropixels values (p if white, 1-p if black)
# the final value is the probability that the photo was taken at that offset
# the final registration offset is the offset where the product is highest

# to check that the algorithm works we show that:
# 1. probability at the offset where the photo was taken > probability at other offsets
# 2. as k increases we're less likely to guess a wrong offset compared to the one where the photo was actually taken


def calculate_probability(offset: int) -> int:
    # TODO: probability is *really* small, better work with ints than with floats
    probability: int = 1
    for n, mu in zip(world.get_world_whites_count(offset, r), photo.get_macros()):
        probability *= (n) if mu == 1 else (r - n)
    return probability
    
def guess_offset() -> int:
    # calculate the product probability
    # N.B. using float the probability gets squished to 0.0 due to the high amount of macropixels
    # using bigints we can avoid the problem, so instead of calculating the actual probability
    # we only calculate the numerator, since the denominator is always r^k which we can ignore
    # since the argmax doesn't get affected
    probabilities : List[int] = []
    for i in range(0, r + 1):
        probabilities.append(calculate_probability(i))

    print(probabilities)

    return probabilities.index(max(probabilities))

# world setup
k: int = 10
r: int = 2
trials: int = 100

guesses: List[int] = [0] * (r+1) # record wrong guesses ad relative offset distance
for _ in range(trials):
    f: int = random.randint(0, r)
    world: World_1d = World_1d(2 * k * r)

    # take a photo
    photo: Photo_1d = world.take_photo(f, k, r)
    # print(f"{world=}")
    # print(f"{photo=}")

    guess = guess_offset()
    guesses[photo.offset - guess] += 1

    # print(f"guessed position: {guess} actual offset: {photo.offset}")

print(f"{guesses=}")


# # Data for plotting
# t = [i for i in range(r+1)]
# s = probabilities

# fig, ax = plt.subplots()
# ax.plot(t, s)

# ax.set(xlabel='offsets (f)', ylabel='probability (p)',
#        title='Probability check of a single photo')
# ax.grid()

# plt.ylim(bottom=0)

# # fig.savefig("test.png")
# plt.show()