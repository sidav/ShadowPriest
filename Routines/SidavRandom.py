import time

LCG_X = 1


def rand(mod):
    global LCG_X
    LCG_A = 14741
    LCG_C = 757
    LCG_M = 77777677777
    LCG_X = (LCG_A*LCG_X + LCG_C) % LCG_M
    return LCG_X%mod


def rand_bool():
    return bool(rand(2))


def srand(seed):
    global LCG_X
    LCG_X = seed


def randomize():
    int(time.time())
    # srand(random.getrandbits(32))
