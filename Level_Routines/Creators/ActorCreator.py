from ..Units.Actor import Actor
from Routines.SidavRandom import rand

# This whole file contains placeholders for now and needs to be tweaked.


def create_guard(x, y, rank):
    if rank == 0:
        color = (32, 192, 32)
        name = 'Guard'
    if rank == 1:
        color = (176, 160, 0)
        name = 'Guard Officer'
    guard = Actor(x, y, 'G', color, name)
    return guard

