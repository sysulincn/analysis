
import matplotlib.pyplot as plt
import numpy as np
import tushare as ts
import pandas as pd


# df = ts.get_k_data('300104')
x = [110.30, 113.75, 111.68, 112.28, 111.99, 113.68, 114.55, 114.72, 114.90, 113.74, 112.35,
     111.20, 115.00, 115.50, 115.30, 115.20, 110.96, 111.00, 112.50, 112.20, 113.36, 114.90, 
     117.55, 117.05, 117.10]

print(np.arange(3, 28))

s = pd.Series(x, np.arange(3, 28))
p = s.shift()
dn = p - s
dn = dn.apply(lambda x : x if x > 0 or np.isnan(x) else 0)
# print(np.count_nonzero(dn))
dnAvg = dn.rolling(10).apply(lambda x : np.sum(x) / np.count_nonzero(x))
shortStop = (s - 2 * dnAvg).shift()
protectStop = shortStop.rolling(3).max()
df = pd.DataFrame({'low':s, 'dn': dn, 'dnAvg': dnAvg, 'shortStop': shortStop, 'protectStop':protectStop})

print(df[['low', 'dn', 'dnAvg', 'shortStop', 'protectStop']])
# ax.plot(lows)
# plt.show()

def genSafeZoneIndex_rolling(lows, lookback=10, multi=2, max=3):
    previousLow = lows.shift()
    dn = previousLow - lows
#     dnAvg = dn.rolling(lookback).apply(lambda x : )
    pass

def genSafeZoneIndex_plain(lows, lookback=10, multi=2, max=3):
#     lows = np.asarray(lows)
    len = len(lows)
    i = 0
    previousLow = np.nan
    dnPenArr = []
    stop = []
    sumOfDnPen = 0
    numOfDnPen = 0
    while i < len:
        if(len(dnPenArr) == lookback):
            pass
        dnPen = previousLow - lows[i]
        if(dnPen < 0):
            dnPen = 0
        dnPenArr.append(dnPen)
        previousLow = lows[i]
        i+=1
    