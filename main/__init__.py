from matplotlib import style
from mpl_finance import candlestick_ohlc
from matplotlib.pyplot import axvline, axhline
from matplotlib.ticker import Formatter
from matplotlib.widgets import MultiCursor

import chart
import datetime as dt
import index as idx
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import ticker
import tushare as ts


def main():
    plt.style.use('dark_background')
    code = 'sh000902'
    
    df = ts.get_k_data(code, start='2017-12-13')
    
    fig = plt.figure();
    fig.suptitle(code)
    chart.plotDailyK(df, fig)
    cursor = Cursor(fig)
    plt.connect('motion_notify_event', cursor.mouse_move)
    plt.connect('resize_event', cursor.resize)
    plt.show()

class Cursor(object):
    def __init__(self, fig):
        self.fig = fig
        self.lines = list(map(lambda ax_index:ax_index.axvline(color='w', animated=True), fig.axes))
        fig.canvas.draw()
        self.background = fig.canvas.copy_from_bbox(self.fig.bbox) 
    
    def mouse_move(self, event):
        if not event.inaxes:
            return
        lows = int(event.xdata)
        for line in self.lines:
            line.set_xdata(lows) 
        self.fig.canvas.restore_region(self.background)
        for d in np.arange(len(self.lines)):
            self.fig.axes[d].draw_artist(self.lines[d])
        self.fig.canvas.blit(self.fig.bbox)
    
    def resize(self, event):
        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)
    
if __name__ == "__main__":
    main()