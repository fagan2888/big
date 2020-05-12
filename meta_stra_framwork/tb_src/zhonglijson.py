import pandas as pd
import numpy as np
import copy
import json
import tushare as ts

from rqdata import now_file,up_file
signal_path = up_file+'/tb_signal'
index_path = up_file+'/tb_index'
data_len = 20

def get_code_list():
    code_list = ts.get_hs300s()['code']
    for i in range(len(code_list)):
        if(str(code_list[i])[0]=='6'):
            code_list[i] = str(code_list[i]) + '.XSHG'
        else:
            code_list[i] = str(code_list[i]) + '.XSHE'
    return code_list.tolist()

def get_ind_type(use_index):
    ind_type = {}
    ind_type['G'] = [0,1]
    ind_type['L'] = [0,1]
    for i in range(len(use_index)):
        index_name = use_index[i]
        if('+' not in index_name and '*' not in index_name):
            if('HS' in index_name):
                ind_type['G'].append(i+2)
            else:
                ind_type['L'].append(i+2)
    return ind_type            

def get_one_data(use,signal,data,data_len): 
    for i in range(len(use)-data_len):
        one_data = {}
        split_close = signal['close'].iloc[i:i+data_len]
        split_open = signal['open'].iloc[i:i+data_len]
        if(np.sum(split_close <=0)!=0 or np.sum(split_open <=0)!=0):
            continue
        else:
            TF=pd.DataFrame(use.iloc[i:i+data_len].values.tolist())
            TF.insert(0,'T',np.ones([data_len,1]).astype(int))
            TF.insert(0,'F',np.zeros([data_len,1]).astype(int))
            TF=TF.values.tolist()
            one_data['inds'] =TF
            #one_data['inds'] = use.iloc[i:i+data_len].values.tolist()
            one_data['close_prices'] = split_close.values.tolist()
            one_data['open_prices'] = split_open.values.tolist()

        data.append(one_data)
    return data

def get_zl_data(code_list):
    data = []
    for code in code_list[0:30]:
        try:
            index = pd.read_csv(index_path+'/'+code+'.csv')
            signal = pd.read_csv(signal_path+'/'+code+'.csv')
            use_index = signal.columns.values[len(index.columns.values):].tolist()
            nei = copy.copy(use_index)
            for _index in use_index:
                if('+' in _index or '*' in _index):
                    nei.remove(_index)
            use = signal[nei]
            data = get_one_data(use,signal,data,data_len)
        except Exception as e:
            print(code,e)
    result = {}
    result['data'] = data
    result["ind_type"] = get_ind_type(nei)
    # 字典转换成json 存入本地文件
    with open(up_file+'/input.json','w') as f:
        # 设置不转换成ascii  json字符串首缩进
        f.write( json.dumps(result,ensure_ascii=False,indent=2 ) )

    return result

if __name__ == "__main__":
    code_list = get_code_list()
    r = get_zl_data(code_list)