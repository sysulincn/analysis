from math import nan

import MySQLdb
from numpy import array_equal, array_equiv, NaN
from sqlalchemy import create_engine
import talib

import numpy as np
import tushare as ts



def createTable(cur):
    sql = 'DROP TABLE IF EXISTS Test'
    cur.execute(sql)
    sql = '''CREATE TABLE IF NOT EXISTS Test(
            Code VARCHAR(100) NOT NULL PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            High DOUBLE UNSIGNED,
            HighDate DATE,
            Low DOUBLE UNSIGNED,
            LowDate DATE) ENGINE=INNODB DEFAULT CHARSET='UTF8';
            '''
    cur.execute(sql)

conn = MySQLdb.connect(host='10.17.1.118', user='aola', passwd='aola', db='test',charset='utf8')
cur = conn.cursor()

df = ts.get_stock_basics()
values = [tuple(x) for x in df[['code', 'name']].values]
sqlInsert = '''replace into Test(Code,Name)VALUES(%s,%s)'''
cur.executemany(sqlInsert, values)

conn.commit()
cur.close()
conn.close()

