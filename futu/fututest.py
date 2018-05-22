'''
Created on 2018年5月22日

@author: linchengnan
'''
import futuquant as ft


quote_ctx = ft.OpenQuoteContext(host="119.29.141.202", port=11111)

print(quote_ctx.get_history_kline('SH.000902', start='2017-01-01', end='2017-04-01'))