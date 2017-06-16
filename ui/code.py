'''
Created on 2017å¹?2æœ?28æ—?

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
        