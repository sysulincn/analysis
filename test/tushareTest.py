'''
Created on 2017年6月21日

@author: linchengnan
'''
import tushare as ts
import datetime
from time import strptime
# 
# df = ts.get_suspended()
# print(df)
# 
# df = ts.get_terminated()
# print(df)
# df = ts.get_stock_basics()

# suspended = ts.get_suspended()
terminated = ts.get_terminated()
current = ts.get_stock_basics()
print(terminated)

