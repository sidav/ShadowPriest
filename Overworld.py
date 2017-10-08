import ShadowPriest as Main
from ShadowPriest import MAP_WIDTH, MAP_HEIGHT

#Represents the global map.
class Overworld:
    overworldMap = [[None] * MAP_WIDTH for _ in range(MAP_HEIGHT)]
