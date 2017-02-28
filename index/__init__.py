import numpy as np

def ema(lows, n):
    lows = np.asarray(lows)
    def gen(lows, n):
        factor = 2 / (n + 1)
        ema,i = 0, 1
        while i <= len(lows):
            if i <= n :
                ema = ema * (1 - 1/i) + lows[i-1] * 1/i
            else:
                ema = ema * (1 - factor) + lows[i-1] * factor
            yield ema
            i+=1
    return np.asarray(list(gen(lows,n)))



