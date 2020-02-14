import params
import copydata
import re
import copy
import get_new_expre
import pandas as pd
from rqdata import up_file,now_file
import quick_sig as qs
import time
import sig_data
import os
import KB

def get_day_code():
    param =  params.PARAMS
    KB.copy_day_data(param['code_list'])
    KB.copy_day_data([param['HS_code']])
    ori_expre,code_list = param['_Expression'],param['code_list']
    _code_list = copy.copy(code_list)
    for code in code_list:
        if(sig_data.cal_index_data(code) == 0):
            _code_list.remove(code)
    HS_code = param['HS_code']
    sig_data.cal_index_data(HS_code)
    qs.get_signal(_code_list,ori_expre,param['begin_date'])
    new_signal = pd.read_csv(up_file+'/result/quick/quick_sig.csv')
    now_time = time.strftime("%Y%m%d", time.localtime())
    new_code = new_signal[new_signal['time'] == now_time]
    new_buy = new_code[new_code['operation'] == 'long']['code']
    new_sell = new_code[new_code['operation'] == 'long_sell']['code']
    print('buy',new_buy)
    print('sell',new_sell)

if __name__ == "__main__":
    get_day_code()