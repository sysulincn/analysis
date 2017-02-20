import numpy as np

def ma(lows, n, type='exponential'):
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    lows = np.asarray(lows)
    if type == 'simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()

    a = np.convolve(lows, weights, mode='full')[:len(lows)]
    a[:n] = a[n]
    return a

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


lows = np.arange(100)

print(ma(lows, 10))
print(ema(lows, 10))