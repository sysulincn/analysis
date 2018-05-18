'''
Created on 2018年5月15日

@author: linchengnan
'''
from datetime import date
from datetime import datetime
import json
import os

from dateutil.relativedelta import relativedelta
from numpy import *  # @UnusedWildImport
from jqdata import *
import pandas as pd  # @UnusedImport

def read_file(name):
    result = {}
    if(os.path.isfile(name)):
        with open(name, 'r') as load_f:
            result = json.load(load_f)
    return result


def write_file(json, dictValue):
    with open(json, "w") as file:
        json.dump(dictValue, file)


def updateAndPrint():
    date_now = date.today()
    nhDict = read_file('nh.json')
    nlDict = read_file('nl.json')
    date_start = date_now - relativedelta(years=1)#默认取一年数据
    if(nhDict):
        date_start = datetime.strptime(max(nhDict.keys()), '%Y-%m-%d').date()
    if(nlDict):
        tmpDate = datetime.strptime(max(nlDict.keys()), '%Y-%m-%d').date()
        if tmpDate > date_start : date_start = tmpDate
    if(date_start >= date_now):
        return
    allsec = get_all_securities(types=['stock'])
    date_fetch_data = date_start - relativedelta(years=1)
    date_valid = date_now - relativedelta(years =1 )#只获取上市一年后的股票作为参考
    securityList = allsec[allsec.start_date <= date_valid].index.tolist()
    panel = get_price(security=securityList,start_date=date_fetch_data,
                      end_date=date_now,fields=['close'],fq='post')
    df = panel['close']
    if(date_start >= max(df.index).date()):
        return
    
    tradeDays = get_trade_days(start_date=date_fetch_data)
    for code in df.columns:
        values = df[code]
        print("doing code:" + code)
        nh = nan
        nl = nan
        nhDate = nan
        nlDate = nan
        for d in tradeDays[searchsorted(tradeDays,date_start):]:
            aYearAgo = tradeDays[searchsorted(tradeDays, d - relativedelta(years =1))]
            value = nan
            if(d in values.index):
                value = values.loc[d]
            if(isnan(value)): continue #没有值则跳过
            if(isnan(values.loc[aYearAgo])): continue #一年前还没有上市，因此不纳入nhnl计算范围
            if(nh is nan or nhDate < aYearAgo):#更新nh和nhDate
                nhDate = values.loc[aYearAgo:d].idxmax().date()
                if(nhDate is not nan):
                    nh = values.loc[nhDate]
            if(value >= nh):#判定在当天创新高
                nh = value
                nhDate = d
                key = d.strftime('%Y-%m-%d')
                if key in nhDict:
                    nhDict[key] += 1
                else:
                    nhDict[key] = 1
                continue
            if(nl is nan or nlDate < aYearAgo):#更新nl和nlDate
                nlDate = values.loc[aYearAgo:d].idxmin().date()
                if(nlDate is not nan):
                    nl = values.loc[nlDate]
            if(value <= nl):
                nl = value
                nlDate = d
                key = d.strftime('%Y-%m-%d')
                if(key in nlDict):
                    nlDict[key] += 1
                else:
                    nlDict[key] = 1
        write_file("nh.json", nhDict)
        write_file("nl.json", nlDict)


auth('18122743790', '743790')
updateAndPrint()