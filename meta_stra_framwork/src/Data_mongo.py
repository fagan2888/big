#-*- coding: utf-8 -*-
# __author__ = 'Li sz'

# 本脚本的功能从公司的mongo数据库为模型数据集的制作，预测2日后收盘价相对于k日前收盘价的涨跌（t+1的交易模式下，买入卖出需要两天）
# 最终得到的函数为输入日期和股票代码，得到3个月内滑动的X和y，其中X为特征矩阵，y不为one_hot向量

import pandas as pd 
import numpy as np 
import sklearn as sl
import tushare as ts
import datetime
import stockstats
import pymongo

up_day = 5 #看五日的涨幅

#up_file = '/Users/wode/Documents/my_project/limit'
up_file = '/root/limit'

def add_months(dt,months):
    targetmonth=months+dt.month
    try:
        dt=dt.replace(year=dt.year+int(targetmonth/12),month=(targetmonth%12))
    except:
        dt=dt.replace(year=dt.year+int((targetmonth+1)/12),month=((targetmonth+1)%12),day=1)
        dt+=datetime.timedelta(days=-1)
    return dt

def get_mclient():
    _ip = '192.168.1.174'
    _port = 27613
    try:
        _mclient = pymongo.MongoClient(_ip, _port)
        _mdb = _mclient['rqalpha_dev4']
        #print(_mclient)
        return _mclient 

    except Exception as e:
        print("[EXCEPTION] [get_mclient] mongo")
        print(e)
        print("[EXCEPTION] [get_mclient] mongo")

    return None

def get_mdb():
    _db = 'rqalpha_dev4'
    # mongo log in
    _mclient = get_mclient()
    if (_mclient is None):
        print("[ERROR] can NOT connect to mongo !!!")
        return -1
    db = _mclient[_db]
    #print(db)
    if (db is None):
        print("[ERROR] can NOT get db : %s" % (_db))
    return db

#得到融资融券数据
def get_rzrq_data_mongo(code,date = ''):
    _db = get_mdb()
    db_type = 'FstDetail'
    if(date != ''):
        query = {'date': date,'code': code}
    else:
        query = {'code': code}
    a = _db.get_collection(db_type).find(query).sort([('_id',1)])
    all_data = pd.DataFrame(list(a))
    return all_data

#得到沪港通数据
def get_hgt_data_mongo(code,date = ''):
    code = code[:6]
    _db = get_mdb()
    db_type = 'HKshszHold'
    if(date != ''):
        query = {'date': date,'code': code}
    else:
        query = {'code': code}
    a = _db.get_collection(db_type).find(query).sort([('_id',1)])
    all_data = pd.DataFrame(list(a))
    return all_data

#得到基金的持仓数据
def get_fund_data_mongo(code,date = ''):
    _db = get_mdb()
    db_type = 'FundHoldings'
    if(date != ''):
        query = {'reportDate': date,'code': code}
    else:
        query = {'code': code}
    a = _db.get_collection(db_type).find(query).sort([('_id',1)])
    all_data = pd.DataFrame(list(a))
    all_data.to_excel(up_file+'/fund/fund_data/'+code+'.xlsx')
    return all_data

def get_min_data_mongo(code,date = ''):
    _db = get_mdb()
    db_type = 'k1min'
    if(date != ''):
        query = {'date': date,'code': code}
    else:
        query = {'code': code}
    a = _db.get_collection(db_type).find(query).sort([('_id',1)])
    all_data = pd.DataFrame(list(a))
    return all_data

def get_day_data_mongo(code,date = ''):
    _db = get_mdb()
    db_type = 'k1day'
    if(date != ''):
        query = {'date': date,'code': code}
    else:
        query = {'code': code}
    a = _db.get_collection(db_type).find(query).sort([('_id',1)])
    all_data = pd.DataFrame(list(a))
    return all_data

def get_1day_vol(code,date):
    _db = get_mdb()
    db_type = 'k1day'
    query = {'date': {'$lte':date},'code':code}
    a = _db.get_collection(db_type).find(query).sort([('_id',-1)])
    vol_sum = 0
    for k in range(up_day):
        vol_sum += a[k+1]['vol']
    return a[0]['vol']/vol_sum

def get_1day_zf_list(code,date):
    _db = get_mdb()
    db_type = 'k1day'
    query = {'date': {'$gt': date},'code':code}
    a = _db.get_collection(db_type).find(query).sort([('_id',1)])
    zf_list = []
    for k in range(up_day):
        if(a[k]['open']!=0):
            zf_list.append((a[k]['close']/a[0]['open']-1)*100)
        else:
            zf_list.append(0)
    return zf_list

def get_1day_now_data(code,date):
    _db = get_mdb()
    db_type = 'k1day'
    query = {'date':date,'code':code}
    a = _db.get_collection(db_type).find_one(query)
    if(a['open']!=0):
        return [a['open'],a['close'],(a['close']/a['open']-1)*100]
    else:
        return [a['open'],a['close'],0]

if __name__ == "__main__":
    code = '000562.XSHE'
    #all_data = get_min_data_mongo(code)
    #all_data.to_excel(up_file+'/data/'+code+'.xlsx')
    #print(all_data)
    print(get_1day_now_data(code,'20200211'))