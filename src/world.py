import numpy as np

from functools import lru_cache


# TODO still actually only works on 1D worlds.
class World:

    def __init__(self, size: int, d: int = 1, b: float = 0.5):
        """
        :param size: The size of the world in micropixels over each dimension.
        :param d: The number of dimensions of the world, defaults to 1.
        :param b: The average color of the world, that is, the probability that any micropixel is white. Default is 0.5.
        """
        if d != 1:
            raise ValueError("World's of sizes != 1 are not yet implemented.")

        self.b = b
        self.d = d
        self.size = size

        # Random array with d dimensions, of size `size` each.
        # Distribution is uniform over [0, 1) so lower than `b` is white.
        self._micro = np.random.rand(*([size] * d)) < b

    def macros(self, offset: int, resolution: int) -> np.ndarray:
        """
        As `macros` but the color is not normalized between 0 and 1.

        :param offset: The offset in micropixels.
        :param resolution: The resolution of the macropixels (on each dimension).
        :return: The color of the macros, as the number of white micropixels they contain.
        """
        # Shift by the offset.
        shifted = np.roll(self._micro, -offset)
        # Each row is a macropixel.
        grouped = np.reshape(shifted, (-1, resolution))
        # Each macro is the sum of the micros.
        return np.sum(grouped, axis=1)

    def macros_norm(self, offset: int, resolution: int) -> np.ndarray:
        """
        Get the color p of the macros when looking with a certain offset.

        :param offset: The offset in micropixels.
        :param resolution: The resolution of the macropixels (on each dimension).
        :return: The average color of the macros between 0 and 1.
        """
        # Just divide the raw sums.
        return self.macros(offset, resolution) / (resolution ** self.d)

    def picture(self, offset: int, resolution: int) -> np.ndarray:
        """
        Take a picture of the world with a certain resolution at a certain offset.

        :param offset: The offset of the picture.
        :param resolution: The resolution of the picture.
        :return: The picture, an array of macros that are either 0 or 1.
        """
        raw_macros = self.macros_norm(offset, resolution)
        color_choice = np.random.rand(*raw_macros.shape)
        return raw_macros > color_choice

    def __repr__(self) -> str:
        return f"World of size {self.size}{f'^{self.d}' if self.d > 1 else ''} and color {self.b}:\n{self._micro}"
