import tushare as ts
import matplotlib as mpl
from matplotlib.widgets import MultiCursor
mpl.use('Qt5Agg')
from matplotlib.pyplot import axvline, axhline
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib import style
from matplotlib.ticker import Formatter

import numpy as np
import datetime as dt
import ticker

code = '300104'
today = dt.date.today();
deltaOneYear = dt.timedelta(days=550)
start = (today - deltaOneYear).strftime("%Y-%m-%d")
  
df = ts.get_k_data(code, start=start)
ax = plt.subplot2grid((10, 1), (0, 0), rowspan=8, colspan=1)
# subset = df[['date', 'open', 'high', 'low', 'close', 'volume']]
# converter = mdates.strpdate2num('%Y-%m-%d')
# subset['date'] = subset['date'].apply(converter)
quotes=[]
majorFormatter = ticker.MajorFormatter(df['date'])
# minorFormatter = ticker.MinorFormatter(df['date'])
majorLocator = ticker.MajorLocator(df['date'])
minorLocator = ticker.MinorLocator(df['date'])
i=0
for index,row in df.iterrows():
    quotes.append((i,row['open'],row['high'],row['low'],row['close']))
    i+=1
candlestick_ohlc(ax, quotes, colorup='r', colordown='g', width=0.6)
plt.title(code)
# fig, ax2 = 
ax2=plt.subplot2grid((10, 1), (8, 0), rowspan=2, colspan=1, sharex=ax)
fig = plt.gcf()
plt.plot(np.arange(len(df)), df['volume'])
ax2.xaxis.set_major_formatter(majorFormatter)
ax2.xaxis.set_major_locator(majorLocator)
ax2.xaxis.set_minor_locator(minorLocator)
fig.subplots_adjust(hspace=0,wspace=0)
plt.setp(plt.xticks()[1], rotation=30, ha='right')
fig.subplots_adjust(left=0.03,right=1, bottom=0.06, top=0.97)
# maxx = len(df) - 1
# ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
# MultiCursor(fig.canvas, (ax,ax2),color='y',lw=1)

plt.show()

# print(ts.get_latest_news())