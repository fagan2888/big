# -*- coding:UTF-8 -*-
import pymongo
import numpy as np
from gmsdk import md

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

def ATS(x,step=0):
    #step=5 #默认是0
    n=len(x)
    #print(n)
    #print(n)
    chpts=np.mat([[0,x[0]]])
    if(step==0):
        step=np.max([1,int(np.round(n/10))])
    #print(step)
    sp=0 #本来是1，但是python是从0开始的，所以改成了0
    x0=sp
    #print(np.r_[0:step+1],x[np.r_[1:(step+1)]])
    b=6*(np.sum(np.r_[0:step+1]*(x[1:(step+2)]))-x[0]*step*(step+1)/2)/(step*(step+1)*(2*step+1))
    ep=sp+step
    diff=x[ep]-x[sp]
    while(np.sign(diff)!=np.sign(b)):
        ep=ep-1
        if(ep<=1):
            print("data constant in first step")
            return
        diff=x[ep]-x[sp]
    while(diff==0):
        ep=ep+1
        if(ep>=n):
            print("slope=0 and data constant after first step")
            return
        diff=x[ep]-x[sp]
    slope=(x[ep]-x[sp])/step
    cs=np.sign(slope)
    while(ep<n-1):
        #print("ep:",ep)
        spstart=sp
        while(np.sign(slope)==cs):
            ep=np.min([sp+step,n-1])
            if(sp==ep):
                break
            diff=x[ep]-x[sp]
            while(diff==0 and ep==sp+1):
                ep=ep-1
                diff=x[ep]-x[sp]
            if(diff==0):
                ep=np.min([sp+step,n-1])
                while(diff==0 and ep<n):
                    ep=ep+1
                    diff=x[ep]-x[sp]
            slope=diff/(ep-sp)
            sp=ep
        #print(spstart,sp,int(cs),np.multiply(x[spstart:sp],int(cs)),np.argmax(np.multiply(int(cs),x[spstart:sp])))
        sp=spstart+(np.argmax(np.multiply(int(cs),x[spstart:sp])))#R语言和python的a:b可能不一样
        #print("sp:",sp)
        new_chpts=[sp,x[sp]]
        chpts=np.row_stack((chpts,new_chpts))
        x0=sp
        cs=-cs
    if(chpts[chpts.shape[0]-1,0]!=n):
        new_chpts=[n-1,x[n-1]]
        chpts=np.row_stack((chpts,new_chpts))
    return(chpts)


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

def get_db_and_close_1(code, start, end):
    ret = md.init("17801016296", "123456")
    # a = md.get_bars(code,60,start, "2017-12-09 15:00:00")
    daily_bars = md.get_dailybars(code, start, end)
    db = []

    flag = 0
    for i in daily_bars:
        d = dailyBar()
        d.strtime = i.strtime
        d.close = i.close
        d.open = i.open
        d.high = i.high
        d.low = i.low
        # print(d.close)
        db.append(d)
        # print(db[flag].close)
        # if(flag>1):
        # print(db[flag-2].close)
        flag = flag + 1
    close = []
    for j in db:
        # print(j.close)
        close.append(j.close)
    return db, close


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
    return db, close

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

def linear_B(code, start, end, h=3):
    db, close = get_db_and_close_2(code, start, end)
    chpt = ATS(close, h)
    #print(len(close), len(chpt))
    if (chpt[0, 1] > chpt[1, 1]):  # 先算出第一个和第二个是低点还是高点
        db[0].s1 = 1
        db[1].s2 = 1
    else:
        db[0].s2 = 1
        db[1].s1 = 1
    for j in np.arange(chpt.shape[0]):  # 判断j的奇偶性，如果是奇数，和第二个的高低性一致，如果是偶数，和第二个的高低性一致
        if (j % 2 == 0):
            # print(j)
            chx = int(chpt[j, 0])
            # print(chx)
            db[chx].s0 = 1
            db[chx].s1 = db[0].s1
            db[chx].s2 = db[0].s2
        else:
            chx = int(chpt[j, 0])
            # print(chx)
            db[chx].s0 = 1
            db[chx].s1 = db[1].s1
            db[chx].s2 = db[1].s2
    return db_to_dict(db)

'''
#code='SHSE.601997'
code='601996.SH'
start='2016-01-03'
end='2017-01-11'
h=3
db=linear_B(code,start,end,h)
'''