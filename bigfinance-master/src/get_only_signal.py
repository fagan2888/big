import numpy as np
import pandas as pd
import sig_fra
import sig_data
import tushare as ts
import copy
import os
from copydata import get_all_industry_code_list,get_industry_code_list,get_code_list
dp_code = '999999.XSHG'
dp_trade_date = sig_data.get_dp_trade_date()#上证指数的交易日期列表

Expression = ['close_EMA_5#close_EMA_10&cross','RSI_6#85#1&thre',
              'J#100#1&thre','close_EMA_12#close_EMA_26&cross&HS','K#40#1&thre&HS']

def get_all_code(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        return files #当前路径下所有非目录子文件 

def get_date(_nowdate):#trade_date放里面还是放外面
    if(_nowdate != dp_trade_date[-1]):
        _nowdate = dp_trade_date[np.where(dp_trade_date == _nowdate)[0][0]+1]
        return _nowdate
    else:
        print("have done")
        return 0
        
def get_now_bar(code,now_date,w = 100):
    data = sig_data.get_windows_data(code,now_date,w)
    now_bar = copy.copy(data)
    return now_bar

def cal_index_data(code_list,off_line=False):
    _code_list = copy.copy(code_list)
    if(not off_line):
        for code in code_list:
            if(sig_data.cal_index_data(code) == 0):
                _code_list.remove(code)
        sig_data.cal_index_data('999999.XSHG')
    if('999999.XSHG' in code_list):
        _code_list.remove('999999.XSHG')
    print('final',len(_code_list))
    return _code_list
    
def main():
    #industry_name_list = ['金融行业','家电行业','电器行业']
    #code_list = get_industry_code_list(industry_name_list)
    code_list = get_all_industry_code_list()
    begin_year = 2010
    _init_date = dp_trade_date[dp_trade_date>=(str(begin_year)+'0101')][0]
    last_code_list = cal_index_data(code_list)
    Sig = sig_fra.Signal(expression= Expression,code_list = last_code_list,date = _init_date)#创建信号系统
    Sig.dict_init()
    while(Sig.date):
        for _code in Sig.code_list:
            now_bar = copy.copy(get_now_bar(_code,Sig.date,w = 100))
            if(not now_bar.empty and len(now_bar)>1):#要求不仅非空而且长度要大于1
                Sig.type_sig(data = copy.copy(now_bar),code = _code) #Sig计算
            else:
                Sig.expre_sig[_code] = np.zeros(len(Sig.expression))
        Sig.update()
        Sig.date = copy.copy(get_date(Sig.date)) #Sig的日期更新

if __name__ == '__main__':
    main()