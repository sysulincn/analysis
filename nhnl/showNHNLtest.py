'''
Created on 2018年5月17日

@author: linchengnan
'''
from datetime import date
from datetime import datetime
import json
import operator
import os
import time

from dateutil.relativedelta import relativedelta
from jqdatasdk import *  # @UnusedWildImport
import talib

import index as idx
import matplotlib.pyplot as plt
import mpl_finance as mpf
import numpy as np
import pandas as pd  # @UnusedImport
import tushare as ts


def read_file(name):
    result = {}
    if(os.path.isfile(name)):
        with open(name, 'r') as load_f:
            result = json.load(load_f)
    return result


def write_file(json, dictValue):
    with open(json, "w") as file:
        json.dump(dictValue, file)
        
        
nhDict = read_file('nh.json')
nlDict = read_file('nl.json')
endDate = date(2017, 6, 1)
startDate = endDate - relativedelta(months=18)
data = ts.get_k_data('sh000902', start=startDate.strftime('%Y-%m-%d'), end=endDate.strftime('%Y-%m-%d'))
nhs = [nhDict.get(x,0) for x in data['date']]
nls = [nlDict.get(x,0) for x in data['date']]
print(list(map(lambda x : x[0]-x[1], zip(nhs, nls))))
