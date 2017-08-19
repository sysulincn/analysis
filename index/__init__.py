import numpy as np


def ema(lows, n):
    lows = np.asarray(lows)
    def gen(lows, n):
        factor = 2 / (n + 1)
        ema,d = 0, 1
        while d <= len(lows):
            if d <= n :
                ema = ema * (1 - 1/d) + lows[d-1] * 1/d
            else:
                ema = ema * (1 - factor) + lows[d-1] * factor
            yield ema
            d+=1
    return np.asarray(list(gen(lows,n)))



