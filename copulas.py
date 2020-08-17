import numpy as np

@np.vectorize
def zoc_copula1(a, b, t=.5):
    if np.abs(a-b)>t:
        c = np.minimum(a, b)
    elif np.abs(a+b-1) > 1-t:
        c = np.maximum(a+b-1, 0)
    else:
        c = (a+b)/2 - t/2
    return c

@np.vectorize
def zoc_copula2(a, b, t=.5):
    if a < t and b < t:
        c = np.maximum(a+b-t, 0)
    else:
        c = np.minimum(a, b)
    return c
