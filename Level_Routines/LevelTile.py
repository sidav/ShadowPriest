#represents one cell of a map
#TODO

class Tile:

    _appearance = '?'
    __color = 0xFFFFFF #fuck
    _vision_obstructing = True
    _passable = False

    def __init__(self, appearance, passable, visionObstructing):
        #global _appearance, _passable, _vision_obstructing
        self._appearance = appearance
        self._passable = passable
        self._vision_obstructing = visionObstructing
        
    
    def get_passable(self):
        return self._passable
    
    def get_vision_obstructing(self):
        return self._vision_obstructing