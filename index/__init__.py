import numpy as np

def ma(x, n, type='exponential'):
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if type == 'simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()

    a = np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

def ema(x, n):
    x = np.asarray(x)
    def gen(x, n):
        factor = 2 / (n + 1)
        ema,i = 0, 1
        while i <= len(x):
            if i <= n :
                ema = ema * (1 - 1/i) + x[i-1] * 1/i
            else:
                ema = ema * (1 - factor) + x[i-1] * factor
            yield ema
            i+=1
    return np.asarray(list(gen(x,n)))


x = np.arange(100)

print(ma(x, 10))
print(ema(x, 10))