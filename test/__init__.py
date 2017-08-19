from math import nan

import MySQLdb
from numpy import array_equal, array_equiv, NaN
from sqlalchemy import create_engine
import talib

import numpy as np
import tushare as ts
import datetime
from sympy.physics.units import days
conn = MySQLdb.connect(host='10.17.1.118', user='aola', passwd='aola', db='test',charset='utf8')
cur = conn.cursor();
MIN_DATE = '2000-01-01'

def updateNHNL():
    cur.execute('''CREATE TABLE IF NOT EXISTS ST_NHNL_SERIES(
    `Date` DATE NOT NULL PRIMARY KEY, 
    NH INT UNSIGNED NOT NULL DEFAULT 0, 
    NL INT UNSIGNED NOT NULL DEFAULT 0)
    ENGINE=INNODB;''')
    cur.execute('''SELECT MAX(Date) FROM ST_NHNL_SERIES''')
    date = cur.fetchone()[0]
    if(date == None):
        startDate = MIN_DATE
    else:
        startDate = date
    endDate = datetime.date.today()
    temp = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    while(temp.date() <= endDate):
        print(temp)
        temp = temp + datetime.timedelta(days = 1)
        
    print(startDate)
    print(endDate)

updateNHNL()