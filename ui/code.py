'''
Created on 2017年2月28日

@author: linchengnan
'''
import tushare as ts

print(ts.get_stock_basics().loc['002230'])

class Stock(object):
    '''
    classdocs
    '''

    def __init__(self, code):
        '''
        Constructor
        '''
        