# -*- coding: utf-8 -*-
# __author__ = 'Li sz'

# 本脚本的功能为信号计算


import pandas as pd 
import numpy as np
import datetime
import os
import copy
import warnings
import sig_data
import Cal_fra
import re
from rqdata import up_file,now_file
import params

param = params.PARAMS
result_save_path = param['_signal_save_path']+'sig'
signal_lf = param['signal_lf']
warnings.filterwarnings("ignore")

_win_list = [1,2,3,4,5] #trend对应的窗口
ema_w_list = [3,5,10,20] #trend对应的平滑窗口
trend_index_name = 'close' #trend对应的index

Expression = ['MACD#0#1&thre','close_EMA_12#close_EMA_26#1&cross']

trend_result = ['1_num','-1_num','0_num','sum']
#信号类
class Signal:
    
    #初始化函数，目前类里面元素定为股票（期货）代码，信号类型（阈值类，交叉类），持续时间
    def __init__(self, expression = [],code_list = [],HScode = param['HS_code'],date = ''):#code = ''):
        #self.code = code
        self.date = date
        self.expression = expression+Expression
        self.input_expression = expression
        self.code_list = code_list
        self.type_list = np.array(self.get_type_list(self.expression))
        self.life = {}
        self.signal = {}
        self.signal_date = {}
        self.expre_sig = {}
        self.trend = {}
        self.HScode =  HScode
    #对大势判断系统进行初始化
    def trend_init(self,):
        for ema_w in ema_w_list:
            self.trend[trend_index_name+'_ema_'+str(ema_w)] = np.zeros(len(_win_list))
    #对多股票信号系统的生命，指标，和信号进行初始化
    def dict_init(self,):
        for code in self.code_list:
            self.life[code] = np.zeros(len(self.type_list))
            self.signal[code] = np.zeros(len(self.type_list))
            self.signal_date[code] = np.zeros(len(self.type_list))
            self.expre_sig[code] = np.zeros(len(self.expression))
        self.trend_init()

    #根据expression得到type_list
    def get_type_list(self,expression):#得到type_list
        type_list = []
        for expre in expression:
            _expression = re.sub('[()]', '',expre)
            add_l=_expression.split('+')
            mul_l = []
            for al in add_l:
                mul_l = copy.copy(mul_l)+al.split('*')
            
            type_list += copy.copy(mul_l)
        type_list = list(set(type_list)) 
        return type_list

    #阈值型信号
    def threshold_sig(self,data,code,type_name,lf = 1,thre_direction = 1,Save = True):
        index_name,index_thre,thre_direction = type_name.split('&')[0].split('#')
        index_thre = float(index_thre)
        if((thre_direction == '1' and data[index_name].iloc[-1] >= index_thre) 
            or (thre_direction == '0' and data[index_name].iloc[-1] <= index_thre)):
            if(Save):
                self.signal[code][self.type_list == type_name] = 1
                self.life[code][self.type_list == type_name] = lf
                self.signal_date[code][self.type_list == type_name] = self.date
            return 1
        else:
            return 0
        
    #趋势型信号
    def trend_sig(self,data,code,type_name,lf = 1,thre_direction = 1,Save = True):
        index_name,trend_num,thre_direction = type_name.split('&')[0].split('#')
        trend_num = int(trend_num)
        if(len(data) < trend_num):
            return 0
        if(thre_direction == '1' ):
            d = data[index_name].diff()
            d = d.apply(lambda x:x/x if x>0 else x-x)
        elif(thre_direction == '0' ):
            d = data[index_name].diff()
            d = d.apply(lambda x:x/x if x<0 else x-x)
        if(d.iloc[-trend_num:].sum() == trend_num):
            if(code != self.HScode and Save):
                self.signal[code][self.type_list == type_name] = 1
                self.life[code][self.type_list == type_name] = lf
                self.signal_date[code][self.type_list == type_name] = self.date
            return 1
        else:
            return 0
    
    #交叉信号
    def cross_sig(self,data,code,type_name,lf = 1,Save = True):#thre_direction0是死叉，1是金叉
        index_name_short,index_name_long,thre_direction = type_name.split('&')[0].split('#')
        if((thre_direction == '1' and (data[index_name_short].iloc[-2] < data[index_name_long].iloc[-2] 
            and data[index_name_short].iloc[-1] > data[index_name_long].iloc[-1])) or ((thre_direction == '0' and (data[index_name_short].iloc[-2] > data[index_name_long].iloc[-2] 
            and data[index_name_short].iloc[-1] < data[index_name_long].iloc[-1])))):
            if(Save):
                self.signal[code][self.type_list == type_name] = 1
                self.life[code][self.type_list == type_name] = lf
                self.signal_date[code][self.type_list == type_name] = self.date
            return 1
        else:
            return 0
    
    def diff_sig(self,data,code,type_name,lf = 1,Save = True):#指标差值,1是前者大于后者，0是后者大于前者
        index_name_1,index_name_2,thre_direction = type_name.split('&')[0].split('#')
        if((thre_direction == '0' and data[index_name_1].iloc[-1] < data[index_name_2].iloc[-1]) 
            or (thre_direction == '1' and data[index_name_1].iloc[-1] > data[index_name_2].iloc[-1])):
            if(Save):
                self.signal_date[code][self.type_list == type_name] = self.date
                self.signal[code][self.type_list == type_name] = 1
                self.life[code][self.type_list == type_name] = lf
            return 1
        else:
            return 0


    def times_sig(self,data,code,type_name,trace_type_name = 'times',lf = 1,Save = True):
        #trace_type_name = 'close_EMA_20#close_EMA_50#1&cross'
        split_name = type_name.split('&')
        trace_type_name = split_name[1]+'&'+split_name[-3]
        sub_type_name = split_name[0]+'&'+split_name[-2]
        times_num = int(split_name[2])
        sub_sig_list = []
        if('times' not in trace_type_name):
            self.get_expre_sig(data,code,trace_type_name)
            trace_date = self.signal_date[code][self.type_list == trace_type_name][0]
            if(trace_date in data.index.tolist()):
                data = data.loc[trace_date:]
        for i in range(len(data)-1):
            sub_data = data.iloc[:(len(data)-i)]
            if('thre' in type_name):
                sub_sig = self.threshold_sig(sub_data, code, type_name = sub_type_name,Save = False,lf = 1)
            elif('cross' in type_name):
                sub_sig = self.cross_sig(sub_data, code, type_name = sub_type_name, Save = False,lf = 1)
            elif('diff' in type_name):
                sub_sig = self.diff_sig(sub_data, code, type_name = sub_type_name, Save = False,lf = 1)
            elif ('trend' in type_name):
                sub_sig = self.trend_sig(sub_data, code, type_name = sub_type_name, Save = False,lf = 1)
            else:
                sub_sig = 0
            sub_sig_list.append(sub_sig)
        print(self.date,len(data),np.array(sub_sig_list).sum(),data.index.tolist()[0])
        if(np.array(sub_sig_list).sum() >= times_num):
            if(Save):
                self.signal[code][self.type_list == type_name] = 1
                self.life[code][self.type_list == type_name] = lf
                self.signal_date[code][self.type_list == type_name] = self.date
            return 1
        else:
            return 0
    
    #得到和expression匹配的信号
    def get_expre_sig(self,data,code,type_name):
        if('times' in type_name):
            self.date,self.times_sig(data, code, type_name = type_name, lf = signal_lf[4])
        elif('thre' in type_name):
            self.threshold_sig(data, code, type_name = type_name, lf = signal_lf[0])
        elif('cross' in type_name):
            self.cross_sig(data, code, type_name = type_name, lf = signal_lf[1])
        elif ('trend' in type_name):
            self.trend_sig(data, code, type_name=type_name, lf = signal_lf[2])
        elif('diff' in type_name):
            self.diff_sig(data, code, type_name = type_name, lf = signal_lf[3])
        else:
            print("can't cal"+type_name)
    
    #得到不同的数据和expression匹配的信号
    def type_sig(self,data,code):
        for type_name in self.type_list:
            if('HS' in type_name):#计算全局风控
                hs_data = copy.copy(sig_data.get_windows_data(self.HScode,self.date,w = 100))
                self.get_expre_sig(hs_data,code,type_name)
            else:
                self.get_expre_sig(data,code,type_name)
        for i in range(0,len(self.input_expression)):#可以在这里变成只算输入的expression
            expre = self.input_expression[i]  
            self.expre_sig[code][i] = Cal_fra.replace_exp(expre,self.get_type_list([expre]),self.type_list,self.signal[code])

    #计算对应指数的大趋势
    def trend_cal(self,now_date):
        index_data = copy.copy(sig_data.get_windows_data(self.HScode,now_date,w = 100))
        for ema_w in ema_w_list:
            for i in range(len(_win_list)):
                ac_type_name = copy.copy(trend_index_name+'_EMA_'+str(ema_w)+'#'+str(_win_list[i])+'#1&trend')
                positive_type_name = copy.copy(trend_index_name+'_EMA_'+str(ema_w)+'#'+str(_win_list[i])+'#0&trend')
                if(self.trend_sig(index_data,self.HScode,ac_type_name)==1):
                    self.trend[trend_index_name+'_ema_'+str(ema_w)][i] = 1
                elif(self.trend_sig(index_data,self.HScode,positive_type_name)==1):
                    self.trend[trend_index_name+'_ema_'+str(ema_w)][i] = -1
                else:
                    self.trend[trend_index_name+'_ema_'+str(ema_w)][i] = 0
    #信号随时间更新
    def update(self,):
        self.write_code_result()#在更新之前写入分股票结果
        #self.write_time_result()#在更新之前写入分时结果
        #self.write_trend_result()#在更新之前写入趋势结果
        for code in self.code_list:
            self.life[code][self.life[code] != 0] = self.life[code][self.life[code] != 0] - 1
            self.signal[code][self.life[code] == 0] = 0
            self.signal_date[code][self.life[code] == 0] = 0

    #把结果按股票代码分类写入txt文件
    def write_code_result(self,):
        w_s = result_save_path+'code/'
        if(not os.path.exists(w_s)):
            os.makedirs(w_s)
        for code in self.code_list:
            if not os.path.exists(w_s+code+'.txt'):
                with open(w_s+code+'.txt','a') as f:
                    f.write('time'+' ')
                    for type_name in self.type_list:
                        f.write(type_name)
                        if(type_name == self.type_list[-1]):
                            f.write('\n')
                        else:
                            f.write(' ')
                    f.close()
            else:
                with open(w_s+code+'.txt','a') as f:
                    f.write(str(self.date)+' ')
                    for i in range(len(self.signal[code])):
                            f.write(str(self.signal[code][i]))
                            if(i == (len(self.signal[code])-1)):
                                f.write('\n')
                            else:
                                f.write(' ')
                    f.close()
    
    def write_trend_result(self,):
        w_s = result_save_path+'trend/'
        if(not os.path.exists(w_s)):
            os.makedirs(w_s)
        for code in self.code_list:
            if not os.path.exists(w_s+code+'.txt'):
                with open(w_s+code+'.txt','a') as f:
                    f.write('time'+' ')
                    for type_name in trend_result:
                        f.write(type_name)
                        if(type_name == trend_result[-1]):
                            f.write('\n')
                        else:
                            f.write(' ')
            else:
                with open(w_s+code+'.txt','a') as f:
                    f.write(self.date+' ')
                    for _type_index in ['1','-1','0','sum']:
                        the_num = 0
                        if(_type_index == 'sum'):
                            for ema_w in ema_w_list:
                                the_num = the_num + copy.copy(self.trend[trend_index_name+'_ema_'+str(ema_w)].sum())
                            f.write(str(the_num)+'\n')
                        else:
                            for ema_w in ema_w_list:
                                the_num = the_num + copy.copy(sum(self.trend[trend_index_name+'_ema_'+str(ema_w)] == int(_type_index)))
                            f.write(str(the_num)+' ')

    #把结果按时间分类写入txt文件
    def write_time_result(self,):
        w_s = result_save_path+'date/'
        if(not os.path.exists(w_s)):
            os.makedirs(w_s)
        with open(w_s+self.date+'.txt','a') as f:
            f.write('code'+' ')
            for type_name in self.type_list:
                f.write(type_name)
                if(type_name == self.type_list[-1]):
                    f.write('\n')
                else:
                    f.write(' ')
            for code in self.code_list:
                f.write(code+' ')
                for i in range(len(self.signal[code])):
                        f.write(str(self.signal[code][i]))
                        if(i == (len(self.signal[code])-1)):
                            f.write('\n')
                        else:
                            f.write(' ')

if __name__ == "__main__":
    Expression = ['close_EMA_5#2#1&cross']

    Sig = Signal(expression= Expression,code_list = ['000002.SZ','000001.SZ'])#创建信号系统
    Sig.dict_init()#初始化信号系统
    print(Sig.life,Sig.signal,Sig.expre_sig)
    print(Sig.life['000002.SZ'])