import math
import numpy as np

DEFAULT_WINDOW_SIZE = 8
DEFAULT_FREQUENCY = 12 # samples per day

def l2(data):
    actual = sum(data) / len(data)
    l2s = [math.pow(d - actual, 2) for d in data]
    return sum(l2s)

def mean(data):
    return sum(data) / len(data)

def slidingWindow(data, width=DEFAULT_WINDOW_SIZE, fun=l2):
    expand = [data[0] for _ in range(0, width)]
    expand.extend(data)
    expand.extend(data[-1] for _ in range(0,width))

    discs = []
    for i in range(width, width+len(data)):
        before = fun(expand[i-width:i])
        after = fun(expand[i:i+width])
        whole = fun(expand[i-width:i+width])
        disc = (whole - (after+before)) / width
        discs.append(disc)

    assert(len(data) == len(discs))
    return discs

def thresholding(data):
    indices = [i for i in range(0, len(data)) if data[i] > 0]
    log_disc = np.log([abs(d) for d in data if d > 0])
    centered = log_disc - np.mean(log_disc)
    norm = centered / np.std(centered)
    
    filtered = [indices[i] for i in range(0, len(norm)) if norm[i] > 1]
    return filtered

def interpolate(xs, ys, freq=DEFAULT_FREQUENCY): # freq = nb samples per day
    xs_days = [x.timestamp()/86400.0 for x in xs]
    step = 1.0 / freq
    newXs = np.arange(xs_days[0], xs_days[-1], step)

    newYs = np.interp(newXs, xs_days, ys)
    return newXs, newYs
