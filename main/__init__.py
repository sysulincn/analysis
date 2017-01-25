import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib import style

import numpy as np
import datetime as dt

style.use('seaborn-dark-palette')
 
today = dt.date.today();
deltaOneYear = dt.timedelta(days=366)
start = (today - deltaOneYear).strftime("%Y-%m-%d")
  
dataframe = ts.get_k_data('300104', start=start)
  
fig = plt.figure()
ax = plt.gca()
subset = dataframe[['date', 'open', 'high', 'low', 'close', 'volume']]
converter = mdates.strpdate2num('%Y-%m-%d')
subset['date'] = subset['date'].apply(converter)

quotes = [tuple(x) for x in subset.values]

candlestick_ohlc(ax, quotes, colorup='r', colordown='g')
ax.grid(True)

plt.show()

# print(ts.get_latest_news())