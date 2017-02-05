from matplotlib import ticker
import numpy as np
import datetime as dt

class MajorFormatter(ticker.Formatter):
    def __init__(self, dateStrArr):
        self.dateStrArr = dateStrArr
    
    def __call__(self, x, pos=None):
        x = int(np.round(x))
        if x >= len(self.dateStrArr) or x < 0:
            return ''
        return ''.join(self.dateStrArr.values[x][2:].split('-'))

class MinorFormatter(ticker.Formatter):
    def __init__(self, dateStrArr):
        self.dateStrArr = dateStrArr    
    
    def __call__(self, x, pos=None):
        x = int(np.round(x))
        if x >= len(self.dateStrArr) or x < 0:
            return ''
        return self.dateStrArr.values[x][-2:]

class MajorLocator(ticker.Locator):
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

class MinorLocator(ticker.Locator):
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