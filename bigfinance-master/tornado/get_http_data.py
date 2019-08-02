import pandas as pd
import numpy as np
import os

now_file = os.path.abspath(os.path.dirname(__file__))
up_file = os.path.abspath(os.path.join(os.getcwd(), ".."))
#up_file = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
trend_result_path = up_file+'/result/3_industry/trend/'

#读取trend的txt数据并转化为tornado的list数据
def read_trend_txt():
    trend_dict_list = []
    code = '000001.XSHE'
    with open(trend_result_path+code+'.txt','r') as f:
        dict_name_list = f.readline().strip().split(' ')
        line = f.readline().strip()
        while(line):
            trend_dict = {}
            data_list = line.split(' ')
            for i in range(len(dict_name_list)):
                dict_name = dict_name_list[i]
                trend_dict[dict_name] = data_list[i]
            trend_dict_list.append(trend_dict)
            line = f.readline().strip()
    return trend_dict_list