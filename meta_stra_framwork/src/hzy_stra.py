import numpy as np
import pandas as pd
import copy
import index_24
import sig_data
from rqdata import up_file,now_file
#对表达式做乘法分配律
def distribute_expre(new_as_list):
    new_expre = ''
    for i in range(1,len(new_as_list)):
        _na = new_as_list[i]
        if(i == 1):
            copy_ne = new_as_list[0]
        else:
            copy_ne = copy.copy(new_expre)
        ne_split = copy_ne.split('+')
        na_split = _na.split('+')
        #new_expre = copy.copy('')
        for ne_s in ne_split:
            for na_s in na_split:
                if(copy_ne == ''):
                    new_expre = copy.copy(na_s)
                elif(new_expre == ''):
                    new_expre = ne_s+'*'+na_s
                else:
                    new_expre += '+'+ne_s+'*'+na_s
    return new_expre


def cal_hzy_data(code,w_1,w_2,w_5,w_6,w_7,day_list_1,vol_mean_period_2,vol_mean_period_3,vol_mean_period_4,vol_mean_period_5,vol_mean_period_7,vol_rate):
    try:
        data = sig_data.get_wm_mongo_data(code)
        data = index_24.calculateMACD(data)
        for d in day_list_1:
            data = index_24.calculateEMA(data,'close',d)

        data = index_24.calculateKlength(data)
        data = index_24.calculateMA(data,'vol',vol_mean_period_2)
        for d in range(1,w_2):
            data = index_24.calculatehistory(data,index_name = 'vol',Period = d)
            data = index_24.calculatehistory(data,index_name = 'Klength',Period = d)
            data = index_24.calculatehistory(data,index_name = 'vol_MA_'+str(vol_mean_period_2),Period = d)

        data = index_24.calculateMA(data,'vol',vol_mean_period_3)

        data = index_24.calculateMA(data,'vol',vol_mean_period_4)
        data = index_24.calculateShadowRate(data)

        data = index_24.calculateMA(data,'vol',vol_mean_period_5)
        data = index_24.calculateLimit(data)
        data = index_24.calculatemultiply(data,index_name = 'LimitUp',rate = 0.99)
        for d in range(0,w_5):
            data = index_24.calculatehistory(data,index_name = 'high',Period = d)
            data = index_24.calculatehistory(data,index_name = 'LimitUp',Period = d)
            data = index_24.calculatehistory(data,index_name = 'LimitUp_multiply_0.99',Period = d)

        for d in range(1,w_6):
            data = index_24.calculatehistory(data,index_name = 'high',Period = d)
            data = index_24.calculatehistory(data,index_name = 'LimitUp',Period = d)

        data = index_24.calculateMA(data,'vol',vol_mean_period_7)
        data = index_24.calculatemultiply(data,index_name = 'vol_MA_'+str(vol_mean_period_7),rate = vol_rate)
        for d in range(1,w_7):
            data = index_24.calculatehistory(data,index_name = 'high',Period = d)
            data = index_24.calculatehistory(data,index_name = 'vol',Period = d)
            data = index_24.calculatehistory(data,index_name = 'LimitUp',Period = d)
            data = index_24.calculatehistory(data,index_name = 'vol_MA_'+str(vol_mean_period_7)+'_multiply_'+str(vol_rate),Period = d)
        data.to_csv(up_file+'/hzy_index/'+code+'.csv',header=True, index='date')
        return 1
    except Exception as e:
        print(e)
        return 0

#多头排列（5 10 20 60均线向上）用均线的趋势信号
def get_hzy_1(w = 2):
    day_list = [5,10,20,60]
    ori = 'close_EMA_'+str(day_list[0])+'#'+str(w)+'#1&trend'
    for d in day_list[1:]:
        ori = ori+'*'+'close_EMA_'+str(d)+'#'+str(w)+'#1&trend'
    return ori

#近期（3天内）阴线缩量，阳线放量 阴线阳线用Klength的和0的阈值信号 放量用今天的量和前几日的均量diff
def get_hzy_2(w = 3,vol_mean_period = 3):
    vol_mean_index = 'vol_MA_'+str(vol_mean_period)
    ori = 'Klength#0#1&thre*vol#'+vol_mean_index+'#1&diff'+'+'+'Klength#0#0&thre*vol#'+vol_mean_index+'#0&diff'
    new_as_list = [ori]
    for d in range(1,w):
        new_as = 'Klength_shift_'+str(d)+'#0#1&thre*vol'+'_shift_'+str(d)+'#'+vol_mean_index+'_shift_'+str(d)+'#1&diff'+'+'+'Klength_shift_'+str(d)+'#0#0&thre*vol'+'_shift_'+str(d)+'#'+vol_mean_index+'_shift_'+str(d)+'#0&diff'
        new_as_list.append(new_as)
    return distribute_expre(new_as_list)

#当天下跌且缩量 趋势和量diff
def get_hzy_3(vol_mean_period = 3):
    vol_mean_index = 'vol_MA_'+str(vol_mean_period)
    hzy_3 = 'close#settle#0&diff*'+'vol#'+vol_mean_index+'#0&diff'
    return hzy_3

#长下影线或缩量十字星最佳（可选）用shadowrate的thre信号
#这里有疑惑就是是否要设定严格等于呢
def get_hzy_4(upper_shadow_rate = 0.8,m = 0.3,n = 0.3,vol_mean_period = 3):
    long_upper_shadow = 'LowerShadowRate#'+str(upper_shadow_rate)+"#1&thre"
    vol_mean_index = 'vol_MA_'+str(vol_mean_period)
    Doji = 'LowerShadowRate#'+str(n)+"#1&thre"+'*'+'UpperShadowRate#'+str(m)+"#1&thre"+'*'+'vol#'+vol_mean_index+'#0&diff'
    hzy_4 = long_upper_shadow + '+' + Doji
    return hzy_4

#近期有放量涨停板但没有连板（可选）用limit来判断涨跌停
#这里用high来判断涨停板
#不连板怎么量化
def get_hzy_5(w = 3,vol_mean_period = 3):
    vol_mean_index = 'vol_MA_'+str(vol_mean_period)
    ori = 'high#LimitUp#1&diff*vol#'+vol_mean_index+'#1&diff'
    for d in range(1,w):
        ori = ori+'+'+'high'+'_shift_'+str(d)+'#LimitUp'+'_shift_'+str(d)+'#1&diff*vol'+'_shift_'+str(d)+'#'+vol_mean_index+'_shift_'+str(d)+'#1&diff'
    new_as_list = [ori]
    for d in range(w-1):
        new_as = 'high'+'_shift_'+str(d)+'#LimitUp'+'_shift_'+str(d)+'#1&diff'+'*'+'high'+'_shift_'+str(d+1)+'#LimitUp_multiply_0.99'+'_shift_'+str(d+1)+'#0&diff' + '+' +'high'+'_shift_'+str(d+1)+'#LimitUp'+'_shift_'+str(d+1)+'#1&diff'+'*'+'high'+'_shift_'+str(d)+'#LimitUp_multiply_0.99'+'_shift_'+str(d)+'#0&diff' + '+' +'high'+'_shift_'+str(d)+'#LimitUp_multiply_0.99'+'_shift_'+str(d)+'#0&diff'+'*'+'high'+'_shift_'+str(d+1)+'#LimitUp_multiply_0.99'+'_shift_'+str(d+1)+'#0&diff'
        new_as_list.append(new_as)
    return distribute_expre(new_as_list)

#价格在涨停板阳线上方（可选）？应该用个最低价和涨停那天的最高价
def get_hzy_6(w = 3):
    ori = 'high#LimitUp#1&diff*close#high#1&diff'
    for d in range(1,w):
        ori = ori + '+' + 'high'+'_shift_'+str(d)+'#LimitUp'+'_shift_'+str(d)+'#1&diff*close#high'+'_shift_'+str(d)+'#1&diff'      
    return ori

#前面n日内，出现了涨停板，且成交量很大（大于均量的2到3倍）
def get_hzy_7(w = 3,vol_rate = 2,vol_mean_period = 3):
    vol_mean_index = 'vol_MA_'+str(vol_mean_period)+'_multiply_'+str(vol_rate)
    ori = 'high#LimitUp#1&diff*vol#'+vol_mean_index+'#1&diff'
    for d in range(1,w):
        ori = ori + '+' + 'high'+'_shift_'+str(d)+'#LimitUp'+'_shift_'+str(d)+'#1&diff*vol'+'_shift_'+str(d)+'#'+vol_mean_index+'_shift_'+str(d)+'#1&diff'      
    return ori

def get_hzy_stra(code_list,w_1 = 2,w_2 = 3,w_5 = 3,w_6 = 3,w_7 = 3,day_list_1 = [5,10,20,60],vol_mean_period_2 = 3,vol_mean_period_3 = 3,vol_mean_period_4 = 3,vol_mean_period_5 = 3,vol_mean_period_7 = 3,vol_rate = 2,upper_shadow_rate = 0.8,m = 0.3,n = 0.3):
    for code in code_list:
        cal_hzy_data(code,w_1 = w_1,w_2 = w_2,w_5 = w_5,w_6 = w_6,w_7 = w_7,day_list_1 = day_list_1,vol_mean_period_2 = vol_mean_period_2,vol_mean_period_3 = vol_mean_period_3,vol_mean_period_4 = vol_mean_period_4,vol_mean_period_5 = vol_mean_period_5,vol_mean_period_7 = vol_mean_period_7,vol_rate = vol_rate)
    #hzy_stra = get_hzy_1(w = w_1)+'+'+get_hzy_2(w = w_2,vol_mean_period = vol_mean_period_2)+'+'+get_hzy_3(vol_mean_period = vol_mean_period_3)+'+'+get_hzy_4(upper_shadow_rate = upper_shadow_rate,m = m,n = n,vol_mean_period = vol_mean_period_4)+'+'+get_hzy_5(w = w_5,vol_mean_period = vol_mean_period_5)+'+'+get_hzy_6(w = w_6)+'+'+get_hzy_7(w = w_7,vol_rate = vol_rate,vol_mean_period = vol_mean_period_7)
    hzy_as_list = [get_hzy_1(w = w_1),get_hzy_2(w = w_2,vol_mean_period = vol_mean_period_2),get_hzy_3(vol_mean_period = vol_mean_period_3),get_hzy_4(upper_shadow_rate = upper_shadow_rate,m = m,n = n,vol_mean_period = vol_mean_period_4),get_hzy_5(w = w_5,vol_mean_period = vol_mean_period_5),get_hzy_6(w = w_6),get_hzy_7(w = w_7,vol_rate = vol_rate,vol_mean_period = vol_mean_period_7)]
    hzy_stra = distribute_expre(hzy_as_list)
    return [hzy_stra,'MACD#0#0&thre']

if __name__ == "__main__":
    code_list = ['000001.XSHE']
    print(get_hzy_stra(code_list))