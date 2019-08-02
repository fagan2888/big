# -*- coding:UTF-8 -*-
import numpy as np
#import matplotlib.pyplot as plt
import pymongo

def get_mclient():
    _ip = '118.89.243.183'
    _port = 47263
    _password = "Wode*2359.com"
    try:

        _mclient = pymongo.MongoClient(_ip, _port)
        _mdb = _mclient['admin']
        _mdb.authenticate('root', _password)

        print(_mclient)
        return _mclient

    except Exception as e:
        print("[EXCEPTION] [get_mclient] mongo")
        print(e)
        print("[EXCEPTION] [get_mclient] mongo")

    return None


def get_dbs():
    _db = 'k1day'  # mongo log in
    _mclient = get_mclient()
    if (_mclient is None):
        print("[ERROR] can NOT connect to mongo !!!")
        return -1

    db = _mclient[_db]
    print(db)
    if (db is None):
        print("[ERROR] can NOT get db : %s" % (_db))
    return db


def get_k1day_data(code, start, end, key):
    db = get_dbs()
    query = {'date': {'$gte': start, '$lte': end}}
    a = db.get_collection(code).find_one(query)
    close = []
    while (a):
        date = a['date']
        # print(date)
        query = {'date': {'$gt': date, '$lte': end}}
        close.append(a[key])
        a = db.get_collection(code).find_one(query)
    return close


class dailyBar:
    def __init__(self):
        self.strtime = ''
        self.close = 0
        self.high = 0
        self.open = 0
        self.low = 0
        self.s0 = 0  # 是否是变化点
        self.s1 = 0  # 是否是高点
        self.s2 = 0  # 是否是低点


def get_close(daily_bar):
    close = []
    for i in daily_bar:
        close.append(i.close)
    return close

def db_to_dict(db):
    db_dict=[]
    for i in np.arange(len(db)):
        _dict={}
        _dict['strtime']=db[i].strtime
        _dict['close'] = db[i].close
        _dict['high'] = db[i].high
        _dict['low'] = db[i].low
        _dict['open'] = db[i].open
        _dict['s0'] = db[i].s0
        _dict['s1'] = db[i].s1
        _dict['s2'] = db[i].s2
        db_dict.append(_dict)
    return db_dict

def get_db_and_close_2(code, start, end):
    db = []
    _db = get_dbs()
    query = {'date': {'$gte': start, '$lte': end}}
    a = _db.get_collection(code).find_one(query)
    close = []
    while (a):
        date = a['date']
        # print(date)
        query = {'date': {'$gt': date, '$lte': end}}
        database = ['', 'j', 't', 'tq']
        close.append(a[database[0] + 'close'])
        d = dailyBar()
        d.strtime = date
        d.close = a[database[0] + 'close']
        d.open = a[database[0] + 'open']
        d.high = a[database[0] + 'high']
        d.low = a[database[0] + 'low']
        db.append(d)
        a = _db.get_collection(code).find_one(query)
        dict_of_db = db_to_dict(db)
    return dict_of_db

