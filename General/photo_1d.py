from typing import List

class Photo_1d:
    
    def __init__(self, photo: List[int], offset: int):
        self.photo = photo
        self.offset = offset #offset at which the photo was taken
        
    def __str__(self) -> str:
        return self.photo.__str__()
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def get_macros(self) -> List[int]:
        return self.photo