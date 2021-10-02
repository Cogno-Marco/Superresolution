import random as rng
from typing import List

class World_1d:
    
    def __init__(self, size: int = 10_000):
        """Generates and returns a new world with a given size (defaults to a size of 10_000)"""
        self._world: List[int] = [rng.randint(0,1) for i in range(size)]
    
    def getWorld(self):
        return self._world
        
    def count_whites(self, ind: int, r: int = 2) -> int:
        """Returns how many white micropixels there are in range [ind, ind+r]. Defaults to r=2"""
        return sum(self._world[ind:ind+r])
    
    def getPixelColorValue(self, ind: int, r: int = 2) -> float:
        """Returns the scaled color of a macropixel with position [ind, ind+r]. Defaults to r=2"""
        return self.count_whites(ind, r) / r
    
    def photo(self, ind: int, k: int = 1_000, r:int = 2) -> List[int]:
        """
        returns a photo of the world starting at a given index
        uses a circular photo
        defaults to k=1_000 and r=2
        """
        #TODO: replace using Photo_1d class
        if ind + k * r <= len(self._world):
            return [rng.choice(self._world[ind+r*i:ind+r*(i+1)]) for i in range(k)]
        else:
            # outside photo range, use a circular tactic
            whites: List[int] = [0] * k
            for i in range(k*r):
                whites[int(i/r)] += self._world[(ind+i)%len(self._world)]
            return [1 if rng.random() < whites[i]/r else 0 for i in range(k)]