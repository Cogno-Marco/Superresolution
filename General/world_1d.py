import random as rng
from typing import List
from general.photo_1d import Photo_1d

class World_1d:
    
    def __init__(self, size: int = 10_000):
        """Generates and returns a new world with a given size (defaults to a size of 10_000)"""
        self._world: List[int] = [rng.randint(0,1) for i in range(size)]
    
    def __str__(self) -> str:
        return "W: " + self._world.__str__()
    
    def get_world(self):
        return self._world
        
    def count_whites(self, ind: int, r: int = 2) -> int:
        """Returns how many white micropixels there are in range [ind, ind+r]. Defaults to r=2"""
        return sum(self._world[ind:ind+r])
    
    def get_pixel_color_value(self, ind: int, r: int = 2) -> float:
        """Returns the scaled color of a macropixel with position [ind, ind+r]. Defaults to r=2"""
        return self.count_whites(ind, r) / r
    
    def get_world_macros(self, offset: int, r: int = 2) -> List[float]:
        """Returns the value of each p"""
        return [self.get_pixel_color_value(i + offset, r) for i in range(0, len(self._world), r)]
    
    def get_world_whites_count(self, offset: int, r: int = 2) -> List[int]:
        """Returns the number of each white micropixels in each world macropixel from offset f"""
        return [self.count_whites(i + offset, r) for i in range(0, len(self._world), r)]
    
    def take_photo(self, ind: int, k: int = 1_000, r:int = 2) -> Photo_1d:
        """
        returns a photo of the world starting at a given index
        uses a circular photo
        defaults to k=1_000 and r=2
        """
        if ind + k * r <= len(self._world):
            return Photo_1d([rng.choice(self._world[ind+r*i:ind+r*(i+1)]) for i in range(k)], ind)
        else:
            # outside photo range, use a circular tactic
            whites: List[int] = [0] * k
            for i in range(k*r):
                whites[int(i/r)] += self._world[(ind+i)%len(self._world)]
            return Photo_1d([1 if rng.random() < whites[i]/r else 0 for i in range(k)], ind)