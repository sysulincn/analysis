import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib import style
import datetime as dt

date = (dt.date.today() - dt.timedelta(days=1)).strftime('%Y-%m-%d')

dataframe = ts.get_k_data('300104', start = date)

subset = dataframe[['open', 'high', 'low', 'close', 'volume']]

# converter = mdates.strpdate2num('%Y-%m-%d')
# subset['date'] = subset['date'].apply(converter)


quotes = [tuple(x) for x in subset.values]
ax = plt.gca()
candlestick_ohlc(ax, quotes)
i = 0
for tup in quotes:
    tup[0] = i
    i += 1
print(quotes)

plt.show()