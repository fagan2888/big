#-*- coding: utf-8 -*-
# __author__ = 'Li sz'

import pandas as pd 
import numpy as np 
import Data_mongo
import os
from rqdata import up_file,now_file
import tushare as ts

d_name_list = ['date','code','open','close','zf','kb_num','1d_zf',
                    '2d_zf','3d_zf','4d_zf','5d_zf','vol_5d']

def get_code_list():
    code_list = ts.get_hs300s()['code']
    for i in range(len(code_list)):
        if(str(code_list[i])[0]=='6'):
            code_list[i] = str(code_list[i]) + '.XSHG'
        else:
            code_list[i] = str(code_list[i]) + '.XSHE'
    #print(type(code_list))
    return code_list.tolist()

def get_kb_num(code,date):
    data = Data_mongo.get_min_data_mongo(code,date)
    limit_up = data['high'].max()
    kb_num = 0
    flag = 0
    for i in range(len(data)):
        od = data.iloc[i]
        if(od.low == limit_up):
            flag = 1
        else:
            if(flag == 1):
                kb_num += 1
                #print(i)
            flag = 0
    return kb_num

def result_dict_init():
    rd = {}
    for d_n in d_name_list:
        rd[d_n] = []
    return rd
    
def main():
    result_dict = result_dict_init()
    with open(up_file+'/code/code.txt','r') as f:
        line = f.readline()
        while(line):
            try:
                data_list = []
                dt = line.split(' ')
                code = str(dt[1][0:11])
                date = str(dt[0])
                data_list += [date,code]
                data_list += Data_mongo.get_1day_now_data(code,date)
                data_list += [get_kb_num(code,date)]
                data_list += Data_mongo.get_1day_zf_list(code,date)
                data_list += [Data_mongo.get_1day_vol(code,date)]
                for data,d_n in zip(data_list,d_name_list):
                    result_dict[d_n].append(data)
            except Exception as e:
                print(e,code,date)
            line = f.readline()
    result_fra = pd.DataFrame(result_dict)
    result_fra.to_excel(up_file+'/result/result.xlsx')

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        
        return files  # 当前路径下所有非目录子文件

def get_mongo_data():
    code_list = file_name('/root/meta_stra_framwork/wmdata')
    for code in code_list:
        data = Data_mongo.get_rzrq_data_mongo(code)
        if(not data.empty):
            #data.to_excel(up_file+'/rzrq/'+code+'.xlsx')
            data.to_csv(up_file+'/rzrq/'+code+'.csv')

def copy_min_data(code_list):
    for code in code_list:
        all_data = Data_mongo.get_min_data_mongo(code)
        if(not all_data.empty):
            all_data.to_excel(up_file+'/data/'+code+'.xlsx')

def copy_day_data(code_list):
    for code in code_list:
        all_data = Data_mongo.get_day_data_mongo(code)
        if(not all_data.empty):
            print('copy '+code+' finished')
            all_data.to_csv(up_file+'/day_data/'+code+'.csv')
        else:
            print('copy '+code+' falled')

if __name__ == "__main__":
    #get_mongo_data()
    code_list = pd.read_excel(now_file+'/all_code.xlsx')['code']
    copy_day_data(code_list)