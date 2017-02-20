from matplotlib import gridspec
from matplotlib.finance import candlestick_ohlc

import data
import datetime as dt
import index as idx
import matplotlib.ticker as ticker
import numpy as np
import tushare as ts


def drawK(df, ax_k, ema):
    ax_volume = ax_k.twinx()
    quotes = []
    i = 0
    for _, row in df.iterrows():
        quotes.append((i, row['open'], row['high'], row['low'], row['close']))
        i += 1
    
    candlestick_ohlc(ax_k, quotes, colorup='r', colordown='g', width=0.6)
    for n,color in ema:
        ax_k.plot(np.arange(len(df)), idx.ema(df['close'], n), linewidth=0.8, color=color)
    ax_k.set_xlim(-0.3, len(df) + 0.3)
    ax_k.set_ylim(min(df['low']), max(df['high']))
    ax_volume.set_ylim(0, 3 * df['volume'].max())
# fig, ax_volume =
# ax_volume=plt.subplot2grid((10, 1), (9, 0), rowspan=1, colspan=1, sharex=ax_k)
    ax_volume.fill_between(np.arange(len(df)), 0, df['volume'], facecolor='peru', alpha=0.5, interpolate=True)
    ax_volume.plot(np.arange(len(df)), df['volume'], 'k-', linewidth=0.2, alpha=0.5)

def drawMacd(df, ax, fastN=10, slowN=22, signalN=7):
    macd = idx.ema(df['close'], fastN) - idx.ema(df['close'], slowN)
    signal = idx.ema(macd, signalN)
    barValue = (macd - signal) * 2
    ax.bar(np.arange(len(df)) - 0.5, barValue, width=1, edgecolor = 'k', color=['r' if v > 0 else 'g' for v in barValue])
    ax.plot(np.arange(len(df)), macd, lw=0.8, color='white', alpha=0.3)
    ax.plot(np.arange(len(df)), signal, lw=0.8, color='yellow', alpha=0.3)

def drawSafeZone(df, ax, lookback=10, mutliOfAverageDownPenetration=2, maxConinuousDecline=3):
    DnPen = df['low'].shift() - df['low']
    DnPen.apply(lambda lows : 0 if lows < 0 else lows)
    
    
def drawForceIndex(df, ax):
    forceIndex = (df['close'] - df['close'].shift()).fillna(0)*df['volume']
    ax.plot(np.arange(len(df)), idx.ema(forceIndex, 2), lw=0.5, color='orange')
    ax.plot([0,len(df)], [0, 0], color='w', lw=0.5)

def plotDailyK(code, fig, plotNum=int(180)):
    df = ts.get_k_data(code)
    if(df.size > plotNum):
        df = df.tail(plotNum)

    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1])
    ax_k = fig.add_subplot(gs[0])
    ax_macd = fig.add_subplot(gs[1], sharex = ax_k)
    ax_forceIndex = fig.add_subplot(gs[2], sharex = ax_k)
#     lines = []
#     lines.append(ax_k.plot())
    
    fig.suptitle(code)
    
    drawK(df, ax_k, [(5, 'Orange'), (10, 'Orchid')]) 
    drawMacd(df, ax_macd)
    drawForceIndex(df, ax_forceIndex)
    
    majorFormatter = Formatter(df['date'])
    majorLocator = MonthLocator(df['date'])
    minorLocator = WeekLocator(df['date'])
    ax_macd.xaxis.set_major_formatter(majorFormatter)
    ax_macd.xaxis.set_major_locator(majorLocator)
    ax_macd.xaxis.set_minor_locator(minorLocator)
    
    fig.subplots_adjust(hspace=0,wspace=0)
    fig.autofmt_xdate()
    fig.subplots_adjust(left=0.06,right=1, bottom=0.1, top=0.95)

def plotWeeklyK(code, fig, plotNum=52 * 4):
#      gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1])
    ax = fig.add_subplot(111)
    df = ts.get_k_data(code, ktype='W')
    if(df.size > plotNum):
        df = df.tail(plotNum)
    ax_volume = ax.twinx()
    quotes = []
    i=0
    for _,row in df.iterrows():
        quotes.append((i,row['open'],row['high'],row['low'],row['close']))
        i+=1
    
    candlestick_ohlc(ax, quotes, colorup='r', colordown='g', width=0.6)
    ax.plot(np.arange(len(df)), idx.ema(df['close'].values, 26), linewidth=0.8)
    ax.set_xlim(-0.3, len(df) + 0.3)
    ax.set_ylim(min(df['low']), max(df['high']))
    ax_volume.set_ylim(0, 3 * df['volume'].max())
    # fig, ax_volume = 
    # ax_volume=plt.subplot2grid((10, 1), (9, 0), rowspan=1, colspan=1, sharex=ax)
    ax_volume.fill_between(np.arange(len(df)), 0, df['volume'], facecolor='peru', alpha=0.5, interpolate=True)
    ax_volume.plot(np.arange(len(df)), df['volume'], 'k-', linewidth=0.2) 
    
    majorFormatter = Formatter(df['date'])
    majorLocator = MonthLocator(df['date'])
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_major_locator(majorLocator)

class Formatter(ticker.Formatter):
    def __init__(self, dateStrArr):
        self.dateStrArr = dateStrArr
    
    def __call__(self, lows, pos=None):
        lows = int(np.round(lows))
        if lows >= len(self.dateStrArr) or lows < 0:
            return ''
        return ''.join(self.dateStrArr.values[lows][2:].split('-'))

class MonthLocator(ticker.Locator):
    def __init__(self, dateStrArr):
        self.dateStrArr = dateStrArr
    
    def __call__(self):
        d = dict()
        i = 0
        for dateStr in self.dateStrArr:
            monthStr = dateStr[:-3]
            if monthStr not in d :
                d[monthStr] = i
            i += 1
        return d.values()

class WeekLocator(ticker.Locator):
    def __init__(self, dateStrArr):
        self.dateStrArr = dateStrArr
    
    def __call__(self):
        d = dict()
        i = 0
        for dateStr in self.dateStrArr:
            date = dt.datetime.strptime(dateStr, '%Y-%m-%d').strftime('%Y%W')
            if date not in d:
                d[date] = i
            i += 1
        return d.values()