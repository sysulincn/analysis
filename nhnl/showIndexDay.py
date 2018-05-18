'''
Created on 2018年5月17日

@author: linchengnan
'''
from datetime import date
from datetime import datetime
import json
import os

from dateutil.relativedelta import relativedelta
from jqdatasdk import *  # @UnusedWildImport
import talib
from matplotlib import gridspec
import matplotlib.pyplot as plt
import mpl_finance as mpf
import numpy as np
import pandas as pd  # @UnusedImport
import tushare as ts
import index as idx
import chart

def read_file(name):
    result = {}
    if(os.path.isfile(name)):
        with open(name, 'r') as load_f:
            result = json.load(load_f)
    return result


def write_file(json, dictValue):
    with open(json, "w") as file:
        json.dump(dictValue, file)
        
        
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
    
    def resize(self, _):
        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)
    

plt.rcParams['font.sans-serif']=['SimHei']#中文编码
plt.rcParams['axes.unicode_minus'] =False #减号unicode编码
plt.style.use('dark_background')
gs = gridspec.GridSpec(5, 1, height_ratios=[2, 1, 1, 1, 1]) 
fig = plt.figure()
fig.suptitle("指数")
ax_index = fig.add_subplot(gs[0])
ax_volume = fig.add_subplot(gs[1])
ax_macd = fig.add_subplot(gs[2])
ax_forceIndex = fig.add_subplot(gs[3])
ax_nhnl = fig.add_subplot(gs[4])

# endDate = date.today()
endDate = date(2017,6,1)
startDate = endDate - relativedelta(months=18)
data = ts.get_k_data('sh000902', start=startDate.strftime('%Y-%m-%d'), end=endDate.strftime('%Y-%m-%d'))

chart.drawK(data, ax_index, [(5, 'r'), (10, 'Orange'), (30, 'c')])
chart.drawVolume(data, ax_volume, [(5, 'r'), (10, 'Orange')])
chart.drawMacd(data, ax_macd)
chart.drawForceIndex(data, ax_forceIndex)
nhDict = read_file('nh.json')
nlDict = read_file('nl.json')
getValueArray = lambda d,index : d.get(index, 0)
nhs = [getValueArray(nhDict,x) for x in data['date']]
nls = [getValueArray(nlDict,x) for x in data['date']]
chart.drawNhnl(ax_nhnl, nhs, nls)


fig.subplots_adjust(hspace=0,wspace=0)
fig.subplots_adjust(left=0.06,right=1, bottom=0.1, top=0.95)
cursor = Cursor(fig)

plt.connect('motion_notify_event', cursor.mouse_move)
plt.connect('resize_event', cursor.resize)
plt.show()

