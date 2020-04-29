# -*- coding: utf-8 -*-
# __author__ = 'Li sz'

# 本脚本的功能为对收益进行回测


import pandas as pd 
import numpy as np
import datetime
import os
import copy
import warnings
import json
import index_24
import rqdata
import tb_index
from rqdata import up_file,now_file
import params
#得到沃民的数据

def get_wm_offline_data(code):
    if('XSHG' not in code and 'XSHE' not in code):
        code = code.replace('SH','XSHG').replace('SZ','XSHE')
    f = open(up_file+'/wmdata/'+code)
    wm_pd = []
    try:
        wm_data=json.loads(f.read())
    except Exception as e:
        print('off_line',f.read())
        print('offline',code,e)
    
    
    wm_pd = pd.DataFrame(wm_data,columns = ['date','close','high','open','low','vol','settle','amount','percent'])
    wm_pd['date'] = [int(i) for i in wm_pd['date']]
    wm_pd.set_index(["date"], inplace=True)
    return wm_pd

def get_wm_mongo_data(code):
    if('XSHG' not in code and 'XSHE' not in code):
        code = code.replace('SH','XSHG').replace('SZ','XSHE')
    try:
        wm_pd = pd.read_excel(up_file+'/day_data/'+code+'.xlsx')
        wm_pd['date'] = [int(i) for i in wm_pd['date']]
        wm_pd.set_index(["date"], inplace=True)
    except Exception as e:
        wm_pd = []
        print('offline',code,e)
    return wm_pd

def get_wm_data(code):
    data = rqdata.history_bars(code,start='20120101',end='20190422')['data']#通过tornado获取数据
    #print(data)
    data.set_index(["date"], inplace=True)
    return data

def cal_tb_index_data(code):
    try:
        #data = get_wm_offline_data(code)
        data = get_wm_mongo_data(code)
        if(len(data)>0):
            data = tb_index.calculateAll_tbindex(data)
            data.to_csv(up_file+'/tb_index/'+code+'.csv',header=True, index='date')

    except Exception as e:
        print('calindex',code,e)
        return 0
    
    return 1

def cal_index_data(code):
    try:
        #data = get_wm_offline_data(code)
        data = get_wm_mongo_data(code)
        #data = get_wm_data(code)#通过tornado获取数据
        #print(data)
        data = index_24.calculateEMA(data,'close',5)
        data = index_24.calculateEMA(data,'close',7)
        data = index_24.calculateEMA(data,'close',14)
        data = index_24.calculateEMA(data,'close',21)
        data = index_24.calculateEMA(data,'close',3)
        data = index_24.calculateEMA(data,'close',15)
        data = index_24.calculateEMA(data,'close',30)
        data = index_24.calculateEMA(data,'close',45)
        data = index_24.calculateEMA(data,'close',25)
        data = index_24.calculateEMA(data,'close',50)
        data = index_24.calculateEMA(data,'close',75)
        data = index_24.calculateEMA(data,'close',10)
        data = index_24.calculateEMA(data,'close',20)
        data = index_24.calculateEMA(data,'close',40)
        data = index_24.calculateEMA(data,'close',80)
        data = index_24.calculateTD(data,'close',5,'EMA',3)
        data = index_24.calculateTD(data,'close',10,'EMA',3)
        data = index_24.calculateTD(data,'close',20,'EMA',3)
        data = index_24.calculateTD(data,'close',40,'EMA',3)
        data = index_24.calculateTD(data,'close',80,'EMA',3)
        data = index_24.calculateTD(data,'close',5,'EMA',-3)
        data = index_24.calculateTD(data,'close',10,'EMA',-3)
        data = index_24.calculateTD(data,'close',20,'EMA',-3)
        data = index_24.calculateTD(data,'close',40,'EMA',-3)
        data = index_24.calculateTD(data,'close',80,'EMA',-3)
        data = index_24.calculatehistory(data,'close',4)
        data = index_24.calculateBIAS(data,5)#计算BIAS
        data = index_24.calculateBIAS(data,50)#计算BIAS
        data = index_24.calculateCCI(data)
        data = index_24.calculateKDJ(data)
        data = index_24.calculateWR(data)
        data = index_24.calculateRSI(data,6)
        data = index_24.calculateRSI(data,12)
        data = index_24.calculateROC(data,6)
        data = index_24.calculateROC(data,12)
        data = index_24.calculateRSI(data,24)
        data = index_24.calculateMACD(data)#计算MACD
        data = index_24.calculateMA(data,'close',5)
        data = index_24.calculateMA(data,'close',10)
        data = index_24.calculateMA(data,'close',20)
        data = index_24.calculateMA(data,'close',30)
        data = index_24.calculateMA(data,'close',40)
        data = index_24.calculateMA(data,'close',60)
        data = index_24.calculateKlength(data)
        data = index_24.calculateKUpperLength(data)
        data = index_24.calculateKLowerLength(data)
        data = index_24.calculateMeanAmplitude(data,10)
        data = index_24.calculateBOLL(data,20)
        data = index_24.calculateCR(data,5)
        data = index_24.calculateCCI(data)
        data = index_24.calculateMTM_1(data)
        data = index_24.calculateOBV(data)
        data = index_24.calculateTRIX(data,4,2)
        #data = index_24.calculateSAR(data,6)
        data = index_24.calculateVR(data)
        data = index_24.calculateAR_BR(data)
        data = index_24.calculatePSY(data,6)
        #data = index_24.
        #print(data)
        data.to_csv(up_file+'/index/'+code+'.csv',header=True, index='date')
        return 1
    
    except Exception as e:
        print('calindex',code,e)
        return 0
    
#得到窗口数据
def get_windows_data(code,date,w):
    #data = get_wm_data(code)
    #data = get_wm_offline_data(code)
    #print(up_file+'/index/'+code+'.csv')
    #data = pd.read_csv(up_file+'/index/'+code+'.csv',index_col='date')
    data = pd.read_csv(up_file+'/tb_index/'+code+'.csv',index_col='date')
    date_index = data.index.values
    #date_index = np.array([str(i) for i in date_index])
    date_index = np.array([int(i) for i in date_index])
    if(date in date_index):
        w_data = data[(np.where(date_index == date)[0][0]-w+1):(np.where(date_index == date)[0][0]+1)]
        return w_data
    else:
        return pd.DataFrame([])

def get_dp_trade_date(code):
    #return get_wm_data('999999.SH').index.values
    #code = '999999.SH'
    #dp_index = get_wm_offline_data(code).index.values
    dp_index = get_wm_mongo_data(code).index.values
    #dp_index = np.array([str(i) for i in dp_index])
    dp_index = np.array([int(i) for i in dp_index])
    return dp_index
if __name__ == "__main__":
    #code_list = params.get_code_list()
    #print(len(code_list))
    #for code in code_list:
    code = '999999.XSHG'
    cal_tb_index_data(code)