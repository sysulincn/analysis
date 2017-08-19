'''
Created on 2017年8月17日

@author: linchengnan
'''
from _datetime import timedelta
import datetime

import pymysql

import tushare as ts
from time import strftime


cursor = pymysql.connect('10.17.1.118', 'aola', 'aola', 'test').cursor()
df = ts.get_stock_basics()
def makeSureCreateTable():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS NHNL_Cache(
        Code CHAR(6) NOT NULL PRIMARY KEY,
        NH DOUBLE NULL DEFAULT NULL,
        NHDate DATE NULL DEFAULT NULL,
        NL DOUBLE NULL DEFAULT NULL,
        NLDate DATE NULL DEFAULT NULL
    )ENGINE=INNODB;''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS NHNL_Data(
        `Date` DATE NOT NULL PRIMARY KEY,
        NH INT UNSIGNED NOT NULL,
        NL INT UNSIGNED NOT NULL
    )ENGINE=INNODB;''')

def getFromDateFromDb():
    cursor.execute('SELECT MAX(Date) FROM NHNL_Data')
    return cursor.fetchone()[0]

def calculateNHNL(d):
    dateStr = d.strftime('%Y-%m-%d')
    print(dateStr)
    codeList = ts.get_stock_basics(date=dateStr)['code']
    print(codeList)
    pass


makeSureCreateTable()
toDate = datetime.date.today()
fromDate = getFromDateFromDb()
if fromDate == None:
    fromDate = toDate + timedelta(weeks=-52)

d = fromDate
while d <= toDate :
    print("calculating nhnl on date : ", d)
    calculateNHNL(d)
    pass
    d = d + timedelta(days=1)


