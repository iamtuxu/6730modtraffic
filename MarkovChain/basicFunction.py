import numpy as np
import time


def randomDisplacementDeviation(mean, SD):
    t = int(round(time.time() * 1000)) % 4294967296
    np.random.seed(t)
    res = np.random.normal(mean, SD, 1)
    if res[0] < 0:
        res[0] = 0
    return res[0]
