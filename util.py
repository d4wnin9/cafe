import pickle
import bz2


def d2s(obj):
    return bz2.compress(pickle.dumps(obj))

def s2d(s):
    return pickle.loads(bz2.decompress(s))

