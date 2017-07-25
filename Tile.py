#represents one cell of a map
#TODO
class Tile:
 _appearance = '?'
 __color = 0xFFFFFF #fuck
 _visionObstructing = True
 _passable = False
 def __init__(self, appearance, passable, visionObstructing):
     #global _appearance, _passable, _visionObstructing
     self._appearance = appearance
     self._passable = passable
     self._visionObstructing = visionObstructing