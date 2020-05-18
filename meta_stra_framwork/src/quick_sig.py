import numpy as np
import pandas as pd
import json
import copy
import re
from rqdata import up_file,now_file
import params

def threshold_sig(data,type_name):
    if('HS' in type_name):
        HS_code = params.PARAMS['HS_code']
        #print(data.index)
        use_data = pd.read_csv(up_file+'/index/'+HS_code+'.csv',index_col='date').loc[data.index]
    else:
        use_data = copy.copy(data)
    #print(type_name)
    index_name,index_thre,thre_direction = type_name.split('&')[0].split('#')
    index_thre = float(index_thre)
    if(thre_direction == '1'): 
        data[type_name] = (use_data[index_name] >= index_thre)*1
    elif(thre_direction == '0'):
        data[type_name] = (use_data[index_name] <= index_thre)*1
    return data    
    
def diff_sig(data,type_name):
    if('HS' in type_name):
        HS_code = params.PARAMS['HS_code']
        use_data = pd.read_csv(up_file+'/index/'+HS_code+'.csv',index_col='date')
    else:
        use_data = copy.copy(data)
    index_name_1,index_name_2,thre_direction = type_name.split('&')[0].split('#')
    if(index_name_1 == index_name_2):
        print('error,two same index can not cal sig')
    else:
        if(thre_direction == '0'): 
            data[type_name] = ((use_data[index_name_1]-use_data[index_name_2])<=0)*1
        elif(thre_direction == '1' ):
            data[type_name] = ((use_data[index_name_1]-use_data[index_name_2])>=0)*1
    return data

def cross_sig(data,type_name):#thre_direction0是死叉，1是金叉
    if('HS' in type_name):
        HS_code = params.PARAMS['HS_code']
        use_data = pd.read_csv(up_file+'/index/'+HS_code+'.csv',index_col='date')
    else:
        use_data = copy.copy(data)
    index_name_short,index_name_long,thre_direction = type_name.split('&')[0].split('#')
    if(index_name_short == index_name_long):
        print('error,two same index can not cal sig')
    else:
        if(thre_direction == '1'):
            now = (use_data[index_name_short]-use_data[index_name_long])>0
            yes = (use_data[index_name_short]-use_data[index_name_long])<0
            result = now.shift(1)*yes
            result.iloc[0] = 0
        elif(thre_direction == '0'):
            now = (use_data[index_name_short]-use_data[index_name_long])<0
            yes = (use_data[index_name_short]-use_data[index_name_long])>0
            result = now.shift(1)*yes
            result.iloc[0] = 0
        data[type_name] = result
    return data

def trend_sig(data,type_name):
    if('HS' in type_name):
        HS_code = params.PARAMS['HS_code']
        use_data = pd.read_csv(up_file+'/index/'+HS_code+'.csv',index_col='date')
    else:
        use_data = copy.copy(data)
    index_name,trend_num,thre_direction = type_name.split('&')[0].split('#')
    trend_num = int(trend_num)
    if(len(use_data) < trend_num):
        print('error,can not cal trend sig length less than trend num')
        return data
    if(thre_direction == '1' ):
        d = use_data[index_name].diff()
        d = d.apply(lambda x:x/x if x>0 else x-x)
    elif(thre_direction == '0' ):
        d = use_data[index_name].diff()
        d = d.apply(lambda x:x/x if x<0 else x-x)
    trend = []
    for i in range(len(data)):
        if(i<trend_num):
            trend.append((d.iloc[:i].sum() == trend_num)*1)
        else:
            trend.append((d.iloc[(i-trend_num):i].sum() == trend_num)*1)
    data[type_name] = trend
    return data

def cal_sig(type_name,data):
    #print(type_name)
    if('thre' in type_name):
        data = threshold_sig(data,type_name)
    elif('cross' in type_name):
        data = cross_sig(data,type_name)
    elif('diff' in type_name):
        data = diff_sig(data,type_name)
    elif('trend' in type_name):
        data = trend_sig(data,type_name)
    else:
        print("can't cal"+type_name)
    return data

def get_type_list(expression):#得到type_list
    type_list = []

    _expression = re.sub('[()]', '',expression)
    add_l=_expression.split('+')
    mul_l = []
    for al in add_l:
        mul_l = copy.copy(mul_l)+al.split('*')

    type_list += copy.copy(mul_l)
    type_list = list(set(type_list)) 
    return type_list

def multiply_divide(s):#计算一个不含括号的最小乘除单元，用split分隔*或/然后计算
    #print(s)
    ret = int(s.split('*')[0]) * int(s.split('*')[1]) if '*' in s else int(s.split('/')[0]) / int(
        s.split('/')[1])
    return ret
 
def remove_md(s):# 将不含括号的表达式里的乘除先递归计算完
    #print('ori',s)
    if '*' not in s and '/' not in s:
        return s# 没有乘除的话递归结束
    else:# 匹配一个最小乘除单元，调用multiply_divide计算，将结果拼接成一个新的表达式进行递归处理
        k = re.search(r'-?[\d\.]+[*/]-?[\d\.]+', s).group()
        s = s.replace(k, '+' + str(multiply_divide(k))) if len(re.findall(r'-', k)) == 2 else s.replace(k, str(
            multiply_divide(k)))
        #print('remove',s)
        return remove_md(s)
 
def add_sub(s):# 计算没有乘除的表达式，得出最后不包含括号表达式的运算结果
    l = re.findall(r'([\d\.]+|-|\+)',s)#将表达式转换成列表，
    #print(l)
    if l[0] == '-':#如果第一个数是负数，对其进行处理
        l[0] = l[0] + l[1]
        del l[1]
    sum = int(l[0])
    for i in range(1, len(l), 2):# 循环计算结果
        #print(l[i + 1])
        if l[i] == '+' and l[i + 1] != '-':
            sum += int(l[i + 1])
        elif l[i] == '+' and l[i + 1] == '-':
            sum -= int(l[i + 2])
        elif l[i] == '-' and l[i + 1] == '-':
            sum += int(l[i + 2])
        elif l[i] == '-' and l[i + 1] != '-':
            sum -= int(l[i + 1])
    return sum
 
def basic_operation(s):# 计算一个基本的4则运算
    s = s.replace(' ', '')
    return add_sub(remove_md(s))# 调用前面定义的函数，先乘除，后加减
 
def calculate(expression):# 计算包含括号的表达式
    if not re.search(r'\([^()]+\)', expression):# 匹配最里面的括号，如果没有的话，直接进行运算，得出结果
        return basic_operation(expression)
    k = re.search(r'\([^()]+\)', expression).group()# 将匹配到的括号里面的表达式交给basic_operation处理后重新拼接成字符串递归处理
    expression = expression.replace(k, str(basic_operation(k[1:len(k) - 1])))
    return calculate(expression)
    
def replace_exp(expression_list,data,code):
    for expression in expression_list:
        new_expre = []
        type_list = get_type_list(expression)
        for _type in type_list:
            if(_type not in data.columns.tolist()):
                data = cal_sig(_type,data)
        for i in range(len(data)):
            new_expression = copy.copy(expression)
            for _type in type_list:
                temp_bool = data[_type].iloc[i]
                if(np.isnan(temp_bool)):
                    new_expression = copy.copy(new_expression.replace(_type,str(0)))
                else:
                    new_expression = copy.copy(new_expression.replace(_type,str(int(temp_bool))))
            if('nan' in new_expression):
                new_expre.append(0)
            else:
                new_expre.append(calculate(new_expression))
        data[expression] = np.array(new_expre)
    
    data.to_csv(up_file+'/signal/'+code+'.csv')
    return data[expression_list]>0

def get_trade_date(code,expression,begin_date):
    #data = pd.read_csv(up_file+'/index/'+code+'.csv',index_col='date').loc[begin_date:]
    data = pd.read_csv(up_file+'/index/'+code+'.csv',index_col='date').loc[begin_date:]
    code_sig = replace_exp(expression,data,code)
    code_sig.loc[:,'code'] = code
    return code_sig[code_sig[expression[0]]]['code'],code_sig[code_sig[expression[1]]]['code']

def get_signal(_code_list,expression,begin_date):
    all_buy,all_sell = pd.Series([]),pd.Series([])
    for code in _code_list:
        try:
        #print(code)
            buy_date,sell_date = get_trade_date(code,expression,begin_date)
            all_buy = all_buy.append(buy_date)
            all_sell = all_sell.append(sell_date)
        except Exception as e:
            print(code,e) 
    buy_df = pd.DataFrame(all_buy)
    buy_df['operation'] = 'long'
    buy_df.columns = ['code','operation']
    sell_df = pd.DataFrame(all_sell)
    sell_df['operation'] = 'long_sell'
    sell_df.columns = ['code','operation']
    signal = sell_df.append(buy_df)
    signal['time'] = [str(x) for x in signal.index.tolist()]
    result = signal.reset_index(drop=True).sort_values(by = ['time'],axis = 0,ascending = True)
    
    return result