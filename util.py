import pickle
import bz2


def o2s(obj):
    return bz2.compress(pickle.dumps(obj)).hex()

def s2o(s):
    return pickle.loads(bz2.decompress(bytes.fromhex(s)))

