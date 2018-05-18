from matplotlib import gridspec
from mpl_finance import candlestick_ohlc
import mpl_finance as mpf
import data
import datetime as dt
import index as idx
import matplotlib.ticker as ticker
import numpy as np
import tushare as ts


def drawK(df, ax_k, ema):
    quotes = []
    d = 0
    for _, row in df.iterrows():
        quotes.append((d, row['open'], row['high'], row['low'], row['close']))
        d += 1
    
    candlestick_ohlc(ax_k, quotes, colorup='r', colordown='g', width=0.6)
    for n,color in ema:
        ax_k.plot(np.arange(len(df)), idx.ema(df['close'], n), linewidth=0.8, color=color)

def drawVolume(data, ax_volume, ema):
    mpf.volume_overlay(ax_volume, data['open'], data['close'], data['volume'], colorup='r', colordown='g', width=1, alpha=0.8)
    for n,color in ema:
        ax_volume.plot(np.arange(len(data)), idx.ema(data['volume'], n), linewidth=1, color=color)

def drawMacd(df, ax_index, fastN=12, slowN=26, signalN=9):
    macd = idx.ema(df['close'], fastN) - idx.ema(df['close'], slowN)
    signal = idx.ema(macd, signalN)
    barValue = (macd - signal) * 2
    ax_index.bar(np.arange(len(df)) - 0.5, barValue, width=1, edgecolor = 'k', color=['r' if v > 0 else 'g' for v in barValue])
    ax_index.plot(np.arange(len(df)), macd, lw=0.8, color='white', alpha=1)
    ax_index.plot(np.arange(len(df)), signal, lw=0.8, color='yellow', alpha=1)

def drawNhnl(ax_nhnl, nhs, nls):
    nhnl = list(map(lambda x : x[0]-x[1], zip(nhs, nls)))
    ax_nhnl.bar(np.arange(len(nhs)) - 0.5, nhnl, width=1, edgecolor='k', color=['r' if v > 0 else 'g' for v in nhnl])
#     ax_nhnl.plot(np.arange(len(nhs)), nhs, lw=0.8, color='r', alpha=1)
#     ax_nhnl.plot(np.arange(len(nhs)), nls, lw=0.8, color='y', alpha=1)
#     ax_nhnl.plot([0, len(nhs)], [0, 0], lw=1, color='white')

def drawSafeZone(df, ax_index, lookback=10, multi=2, maxContinuousDecline=3):
    previous = df['low'].shift()
    dnPen = (previous - df['low']).apply(lambda x : x if x > 0 or np.isnan(x) else 0)
    dnPenAvg = dnPen.rolling(lookback).apply(lambda x : np.sum(x) / np.count_nonzero(x))
    stops = (df['low'] - multi * dnPenAvg).shift()
    protectStop = stops.rolling(maxContinuousDecline).max()
    ax_index.plot(np.arange(len(df)), protectStop)
    
def drawForceIndex(df, ax_index, ema=[(2, 'red'), (13, 'yellow')]):
    forceIndex = (df['close'] - df['close'].shift()).fillna(0)*df['volume']
    for n,color in ema:
        ax_index.plot(np.arange(len(df)), idx.ema(forceIndex, n), lw=0.5, color=color)
    ax_index.plot([0,len(df)], [0, 0], color='w', lw=0.5)

def plotDailyK(df, fig):
    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1])
    ax_k = fig.add_subplot(gs[0])
    ax_macd = fig.add_subplot(gs[1], sharex = ax_k)
    ax_forceIndex = fig.add_subplot(gs[2], sharex = ax_k)
#     lines = []
#     lines.append(ax_k.plot())
    drawK(df, ax_k, [(5, 'Orange'), (10, 'Orchid')]) 
    drawSafeZone(df, ax_k)
    drawMacd(df, ax_macd, fastN=12, slowN=26, signalN=9)
    drawForceIndex(df, ax_forceIndex)
    
    majorFormatter = Formatter(df['date'])
#     majorLocator = MonthLocator(df['date'])
#     minorLocator = WeekLocator(df['date'])
    ax_macd.xaxis.set_major_formatter(majorFormatter)
#     ax_macd.xaxis.set_major_locator(majorLocator)
#     ax_macd.xaxis.set_minor_locator(minorLocator)
    
    fig.subplots_adjust(hspace=0,wspace=0)
    fig.autofmt_xdate()
    fig.subplots_adjust(left=0.06,right=1, bottom=0.1, top=0.95)

def plotWeeklyK(df, fig):
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    ax_k = fig.add_subplot(gs[0])
    ax_macd = fig.add_subplot(gs[1], sharex = ax_k)
    drawMacd(df, ax_macd, fastN=12, slowN=24, signalN=8)
    ax_volume = ax_k.twinx()
    quotes = []
    d=0
    for _,row in df.iterrows():
        quotes.append((d,row['open'],row['high'],row['low'],row['close']))
        d+=1
    
    candlestick_ohlc(ax_k, quotes, colorup='r', colordown='g', width=0.6)
    ax_k.plot(np.arange(len(df)), idx.ema(df['close'].values, 26), linewidth=0.8)
    ax_k.set_xlim(-0.3, len(df) + 0.3)
    ax_k.set_ylim(min(df['low']), max(df['high']))
    ax_volume.set_ylim(0, 3 * df['volume'].max())
    # fig, ax_volume = 
    # ax_volume=plt.subplot2grid((10, 1), (9, 0), rowspan=1, colspan=1, sharex=ax_k)
    ax_volume.fill_between(np.arange(len(df)), 0, df['volume'], facecolor='peru', alpha=0.5, interpolate=True)
    ax_volume.plot(np.arange(len(df)), df['volume'], 'k-', linewidth=0.2) 
    
    majorFormatter = Formatter(df['date'])
#     majorLocator = MonthLocator(df['date'])
    ax_k.xaxis.set_major_formatter(majorFormatter)
#     ax_k.xaxis.set_major_locator(majorLocator)
    
    fig.subplots_adjust(hspace=0,wspace=0)
    fig.autofmt_xdate()
    fig.subplots_adjust(left=0.06,right=1, bottom=0.1, top=0.95)

class Formatter(ticker.Formatter):
    def __init__(self, dateStrArr):
        self.dateStrArr = dateStrArr
    
    def __call__(self, lows, _=None):
        lows = int(np.round(lows))
        if lows >= len(self.dateStrArr) or lows < 0:
            return ''
        return ''.join(self.dateStrArr.values[lows][2:].split('-'))

# class MonthLocator(ticker.Locator):
#     def __init__(self, dateStrArr):
#         self.dateStrArr = dateStrArr
#     
#     def __call__(self):
#         for dateStr in self.dateStrArr:
#             monthStr = dateStr[:-3]
#             if monthStr not in d :
#                 d[monthStr] = d
#             d += 1
#         return d.values()

# class WeekLocator(ticker.Locator):
#     def __init__(self, dateStrArr):
#         self.dateStrArr = dateStrArr
#     
#     def __call__(self):
#         d = dict()
#         d = 0
#         for dateStr in self.dateStrArr:
#             date = dt.datetime.strptime(dateStr, '%Y-%m-%d').strftime('%Y%W')
#             if date not in d:
#                 d[date] = d
#             d += 1
#         return d.values()
