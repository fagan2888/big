# -*- coding: utf-8 -*-
import pandas as pd
import sys,os,time
import math
import rqdata as rq
import json
import copy
from rqdata import up_file,now_file
#import tushare as ts

def get_code_list():
    code_list = ts.get_hs300s()['code']
    for i in range(len(code_list)):
        if(str(code_list[i])[0]=='6'):
            code_list[i] = str(code_list[i]) + '.XSHG'
        else:
            code_list[i] = str(code_list[i]) + '.XSHE'
    return code_list.tolist()

def get_industry_code_list(industry_name_list_list):
    ind_code_list = []
    ind_data_all = pd.read_excel(up_file+'/pic/ind_data_all.xlsx')
    for industry_name_list in industry_name_list_list:
        _code_list = []
        for industry_name in industry_name_list:
            ind_data_one = ind_data_all[ind_data_all['industry']==industry_name]['ts_code'].tolist()
            code_list = copy.copy(ind_data_one)
            #print(len(code_list))
            for i in range(len(code_list)):
                if(str(code_list[i])[0]=='6'):
                    _code_list.append((str(code_list[i])[0:6] + '.XSHG'))
                else:
                    _code_list.append((str(code_list[i])[0:6] + '.XSHE'))
        ind_code_list.append(_code_list)
    return ind_code_list

def get_all_industry_code_list():
    code_list = ts.get_industry_classified()['code'].tolist()
    for i in range(len(code_list)):
        if(str(code_list[i])[0]=='6'):
            code_list[i] = str(code_list[i]) + '.XSHG'
        else:
            code_list[i] = str(code_list[i]) + '.XSHE'
    return code_list

def copy_data(code):
    #print(time.strftime("%Y%m%d", time.localtime()))
    L = rq.history_bars(code, end=time.strftime("%Y%m%d", time.localtime()), fmt='list')['data']
    #L = rq.history_bars(code, end='20190619', fmt='list')['data']
    f = open(up_file+'/wmdata/'+code,'w',encoding='utf-8')
    f.write(json.dumps(L))
    f.close() 
    print(code,'copy finished.')

def get_bk_codes(bkname):
    L = []
    f = open(up_file+'/stocks/'+bkname+'.txt','r',encoding='utf-8')
    for line in f.readlines():
        code = line.strip().split('\t')[0][-6:]
        if code[0] == '6':
            code += '.XSHG' 
        else:
            code += '.XSHE'
        try:
            rq.history_bars(code, time.strftime("%Y%m%d", time.localtime(time.time()-864000)), time.strftime("%Y%m%d", time.localtime(time.time()-86400)))
            L.append(code)
        except Exception as e:
            print(repr(e))
            continue
    f.close()
    return L


def main(stockcodes):
    #stockcodes = get_code_list()
    for code in stockcodes:
        copy_data(code)

if __name__ == '__main__':
    main()
    #copy_data('000032.XSHE')
