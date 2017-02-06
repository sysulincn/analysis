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
import index as idx

code = '300104'
today = dt.date.today();
deltaOneYear = dt.timedelta(days=550)
start = (today - deltaOneYear).strftime("%Y-%m-%d")
  
df = ts.get_k_data(code, start=start)
# ax = plt.subplot2grid((10, 1), (0, 0), rowspan=9, colspan=1)
fig, ax = plt.subplots()
ax_volume = ax.twinx()
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
ax.plot(np.arange(len(df)), idx.moving_average(df['close'], 10, type='simple'), linewidth=0.8)
# ax.plot(np.arange(len(df)), idx.moving_average(df['close'], 13), 'r-', linewidth=0.5)
plt.title(code)

ax.xaxis.set_major_formatter(majorFormatter)
ax.xaxis.set_major_locator(majorLocator)
ax.xaxis.set_minor_locator(minorLocator)
ax.set_xlim(-0.3, len(df) + 0.3)
ax.set_ylim(min(df['low']), max(df['high']))
ax_volume.set_ylim(0, 3 * df['volume'].max())
# fig, ax_volume = 
# ax_volume=plt.subplot2grid((10, 1), (9, 0), rowspan=1, colspan=1, sharex=ax)
ax_volume.fill_between(np.arange(len(df)), 0, df['volume'], facecolor='peru', alpha=0.5, interpolate=True)
ax_volume.plot(np.arange(len(df)), df['volume'], 'k-', linewidth=0.2)
fig.subplots_adjust(hspace=0,wspace=0)
fig.autofmt_xdate()
fig.subplots_adjust(left=0.03,right=1, bottom=0.06, top=0.97)
# plt.setp(fig.axes[0].getx_sticklabels(), rotation=30, ha='right')
# fig.set
# maxx = len(df) - 1
# ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
# MultiCursor(fig.canvas, (ax,ax_volume),color='y',lw=1)

plt.show()

# print(ts.get_latest_news())