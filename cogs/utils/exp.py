import math

def calculate(_from, to):
    ret = 0

    i = _from
    while i < to:
        if i == 0:
            ret += 1
        else:
            ret += math.floor(30 * math.pow(1.25, i))

        i += 1

    return ret