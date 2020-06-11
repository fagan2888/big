import json
import copy
import pandas as pd
import numpy as np
import tushare as ts
from rqdata import up_file,now_file
import os

def get_new_o(or_s,nei):
    os_s = or_s.split('|')
    new_o = ''
    if('1' in os_s):
        return 0
        #pass
    else:
        for o in os_s:
            if(o == '0'):
                continue
            else:
                if(new_o == ''):
                    new_o += nei[int(o)-2]
                else:
                    new_o += '+'
                    new_o += nei[int(o)-2]
        if(new_o==''):
            return 0
        else:
            return new_o

def distribute_expre(new_as_list):
    new_expre = ''
    for _na in new_as_list:  
        copy_ne = copy.copy(new_expre)
        ne_split = copy_ne.split('+')
        na_split = _na.split('+')
        new_expre = ''
        for ne_s in ne_split:
            for na_s in na_split:
                if(copy_ne == ''):
                    new_expre = copy.copy(na_s)
                elif(new_expre == ''):
                    new_expre = ne_s+'*'+na_s
                else:
                    new_expre += '+'+ne_s+'*'+na_s
    return new_expre

def get_buy_sell(mh_s):
    
    signal_path = up_file+'/signal'
    index_path = up_file+'/index'
    code = '000001.XSHE'

    index = pd.read_csv(index_path+'/'+code+'.csv')
    signal = pd.read_csv(signal_path+'/'+code+'.csv')
    use_index = signal.columns.values[len(index.columns.values):].tolist()
    nei = copy.copy(use_index)
    for _index in use_index:
        if('+' in _index or '*' in _index):
            nei.remove(_index)
    and_s = mh_s.split('&')
    new_as_list = []
    for _as in and_s:
        new_as = get_new_o(_as,nei)
        if(new_as != 0):
            new_as_list.append(new_as)
    #print(new_as_list)
    new_expre = distribute_expre(new_as_list)
    return new_expre

def get_new_expre(zl_expre):
    new_expre = []
    for mh_s in zl_expre.split(':'):
        #print(mh_s)
        new_expre.append(get_buy_sell(mh_s))
    return new_expre

def get_expression_list():
    f = open(up_file+"/json/results1_lsz_0422_r0.2.json", encoding='utf-8')  #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    setting = json.load(f)
    sf = pd.DataFrame(setting).T
    expre_list = []
    for _s in sf.index.values:
        expre_list.append(get_new_expre(_s))
    return expre_list
    #sf.columns.values
    #best_zl_expre = sf.sort_index(axis = 0,ascending = True,by = [0]).index.values[-1]

def get_expression_list_2():
    expre_fra = pd.read_csv(up_file+'/expressions/results1_wzh_0422_r0.2.csv',index_col = 0)
    new_stra_list = []
    for i in expre_fra.values:#[0].split(',')[0].strip("[]''")
        new_stra_list.append([i[0].split(',')[0].strip("[]''"),i[0].split(',')[1].strip("[]''")])
    return new_stra_list

#得到每个json文件的第一个表达式
def get_expression_list_3():
    new_stra_list = []
    for k in range(1,5):
        for j in range(2,6):
            csv_path = up_file+'/expressions/results'+str(k)+'_wzh_0526_r0.'+str(j)+'.csv'
            if(os.path.exists(csv_path)):
                expre = pd.read_csv(csv_path,index_col = 0)
                #for i in expre.values:#[0].split(',')[0].strip("[]''")
                i = expre.values[0]
                new_stra_list.append([i[0].split(',')[0].strip("[]''"),i[0].split(',')[1].strip("[]''")])
            else:
                print(csv_path)
    return new_stra_list

#得到每个json文件的所有表达式
def get_expression_list_4():
    new_stra_list = []
    for k in range(1,5):
        for j in range(2,6):
            csv_path = up_file+'/expressions/results'+str(k)+'_wzh_0526_r0.'+str(j)+'.csv'
            if(os.path.exists(csv_path)):
                expre = pd.read_csv(csv_path,index_col = 0)
                for i in expre.values:#[0].split(',')[0].strip("[]''")
                #i = expre.values[0]
                    new_stra_list.append([i[0].split(',')[0].strip("[]''"),i[0].split(',')[1].strip("[]''")])
            else:
                print(csv_path)
    return new_stra_list

#根据回测结果中的vol和年化收益
def get_selected_code_list(expre):
    diff_file = up_file+'/result/diff/'
    #score = pd.read_excel(diff_file+'score.xlsx')
    ar = pd.read_excel(diff_file+'ar.xlsx',index_col = 0)
    vol = pd.read_excel(diff_file+'vol.xlsx',index_col = 0)
    
    new_code_list = []
    vol_one = vol.loc[:,str(expre)]
    ar_one = ar.loc[:,str(expre)]
    vol_selected = vol_one[vol_one<0.1].index.values
    ar_selected = ar_one[ar_one>0.05].index.values
    for code in vol_selected:
        if(code in ar_selected):
            new_code_list.append(code)
    return new_code_list

if __name__ == "__main__":
    print(len(get_expression_list_3()))