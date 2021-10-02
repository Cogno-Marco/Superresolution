from general.world_1d import World_1d
from general.photo_1d import Photo_1d

# registration algorithm:
# compare each macropixel of a photo with a macropixel of the world at an offset
# compute the product of all macropixels values (p if white, 1-p if black)
# the final value is the probability that the photo was taken at that offset
# the final registration offset is the offset where the product is highest

# to check that the algorithm works we show that:
# 1. probability at the offset where the photo was taken > probability at other offsets
# 2. as k increases we're less likely to guess a wrong offset compared to the one where the photo was actually taken

# world setup
k = 5
r = 2
f = 0
world = World_1d(2 * k * r)

# take a photo
photo = world.take_photo(f, k, r)
print(world)
print(photo)

# calculate the product probability
probabilities = []
for i in range(0, r+1):
    probability = 1
    for p, mu in zip(world.get_world_macros(i, r), photo.get_macros()):
        probability *= p if mu == 1 else (1-p)
    probabilities.append(probability)

print(probabilities)