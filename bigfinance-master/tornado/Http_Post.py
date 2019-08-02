import json
import urllib3.request
import urllib.request
import numpy as np

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

def dict_to_db(_dict):
    dict_db = []
    for i in np.arange(len(_dict)):
        _daily_bar = dailyBar()
        _daily_bar.strtime = _dict[i]['strtime']
        _daily_bar.close = _dict[i]['close']
        _daily_bar.high = _dict[i]['high']
        _daily_bar.low = _dict[i]['low']
        _daily_bar.open = _dict[i]['open']
        _daily_bar.s0 = _dict[i]['s0']
        _daily_bar.s1 = _dict[i]['s1']
        _daily_bar.s2 = _dict[i]['s2']
        dict_db.append(_daily_bar)
    return dict_db

def http_post(code,start,end):
    #url='http://localhost:8000/?code='+code+'&start='+start+'&end='+end
    url = 'http://127.0.0.1:8000/?code=601996.SH&start=2016-08-21&mid=2017-01-11&end=2018-01-08'
    #url = 'http://localhost:8000/?greeting=Salutations'
    #values ={'code':'601996.SH','start':'2016-01-03','end':'2017-01-11'}
    #jdata=json.dumps(values)
    #req = urllib2.Request(url,jdata)
    response = urllib.request.urlopen(url)
    str_of_dict = response.read()
    dict_of_db = eval(str_of_dict)
    print(dict_of_db)
    #db = dict_to_db(dict_of_db)
    return dict_of_db

def get_k1day_data(code, start, end, key):
    db = http_post(code, start, end)
    close = []
    for i in db:
        close.append(i.close)
    return close

if __name__ == "__main__":
    code = '601001.SH'
    start = '2016-01-03'
    # mid = '2017-01-11'
    end = '2018-01-11'
    a = http_post(code,start,end)
    #print(a[0].close)
    #key = 'close'
    #close = get_k1day_data(code, start, end, key)
    #print(close)