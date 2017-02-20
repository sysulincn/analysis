import tushare as ts
import matplotlib as mpl
from matplotlib.widgets import MultiCursor
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
import chart

def main():
    plt.style.use('dark_background')
    code = '603568'
    fig = plt.figure();
    chart.plotDailyK(code, fig)
    fig.canvas.draw()
    cursor = Cursor(fig)
    plt.connect('motion_notify_event', cursor.mouse_move)
    plt.show()

class Cursor(object):
    def __init__(self, fig):
        self.fig = fig
        self.lines = list(map(lambda ax:ax.axvline(color='w'), fig.axes))
        self.background = fig.canvas.copy_from_bbox(self.fig.bbox) 
    
    def mouse_move(self, event):
        if not event.inaxes:
            return
        lows = int(event.xdata)
        for line in self.lines:
            line.set_xdata(lows) 
        self.fig.canvas.restore_region(self.background)
        for i in np.arange(len(self.lines)):
            self.fig.axes[i].draw_artist(self.lines[i])
        self.fig.canvas.blit(self.fig.bbox)

if __name__ == "__main__":
    main()