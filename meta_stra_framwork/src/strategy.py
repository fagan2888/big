import sys
sys.path.append('.')
import click
import requests
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows',    None)
import json
import traceback
from rqalpha.api import *
from rqalpha import run_func
import os
#import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import params
import talib
#from sig_meta_stratege import main
from rqdata import up_file,now_file
k = 10
#up_file = '/Users/wode/Documents/signal_framework/big/meta_stra_framwork'

def read_trend_txt():
    trend_dict = {}
    param =  params.PARAMS
    with open(param['_signal_save_path']+'code/all_operation.txt','r') as f:
        dict_name_list = f.readline().strip().split(' ')
        for i in range(len(dict_name_list)):
            dict_name = dict_name_list[i]
            trend_dict[dict_name] = []
        line = f.readline().strip()
        while(line):
            data_list = line.split(' ')
            for i in range(len(dict_name_list)):
                dict_name = dict_name_list[i]
                trend_dict[dict_name].append(data_list[i])
            line = f.readline().strip()
    trend_fra = pd.DataFrame(trend_dict)
    #trend_fra.set_index(['time'],inplace = True)
    if(param['_optimal']):
        os.remove(param['_signal_save_path']+'code/all_operation.txt')
    return trend_fra

def myround(value, n):
    if value > 0:
        return round((value + 10**(-n-8)), n)
    else:
        return round((value - 10**(-n-8)), n)

def init(context):
    context.signals         = pd.read_csv(up_file+'/result/quick/quick_sig.csv',index_col = 0)
    context.signals         = context.signals[context.signals.code!='601360.XSHG']
    context.signals.time    = context.signals.time.map(lambda x:str(x))
    context.operlist        = []
    context.selllist        = []
    context.period       = 5
    

def before_trading(context):
    now = context.now.strftime('%Y%m%d')
    yes = get_previous_trading_date(now).strftime('%Y%m%d')
    selected = context.signals[np.multiply(context.signals.time==yes,context.signals.operation == 'long')]
    selled = context.signals[np.multiply(context.signals.time==now,context.signals.operation == 'long_sell')]
    
    if selected.empty:
        context.operlist = []
    else:
        context.operlist = list(selected.code)
        
    if(selled.empty):
        context.selllist = []
    else:
        context.selllist = list(selled.code)
        
def buy(context, bar_dict):
    now = context.now.strftime('%Y%m%d')
    if context.operlist:
        positions = context.portfolio.positions
        cash1      = context.portfolio.cash
        cash       = cash1
        if len(positions) == 0:
            cash       = cash1/3


        cash_each = 0
        if len(context.operlist) > 50:
            cash_each = cash / len(context.operlist) * 0.9
        if len(context.operlist) < 10:
            cash_each = cash / 10
        else:
            cash_each = cash / 100 * 0.9
        for code in context.operlist:
            try:
                snap = current_snapshot(code)
                if is_suspended(code):
                    #停牌无法买入
                    continue
                if is_st_stock(code):
                    #st股票不考虑
                    continue
                if snap.low >= snap.limit_up:
                    #print('bad limit_up', now, code)
                    #一字涨停无法买入
                    continue
                #print('buy', now, code, cash_each, snap.last)
                order_value(code, cash_each,snap.open)
            except Exception as e:
                print(code,e)

def sell(context, bar_dict):
    now = context.now.strftime('%Y%m%d')
    #print(context.selllist)
    if(context.selllist):
        positions = context.portfolio.positions
        for code, position in positions.items():
            try:
                snap = current_snapshot(code)
                history_prices = history_bars(code,context.period+1,'1d','close')
                avg = talib.MA(history_prices,context.period)
                #止亏
                if(snap.low<position.avg_price*0.95 and snap.high>position.avg_price*0.95):
                    order_target_percent(code,0,position.avg_price*0.95)
                #止盈
                elif(snap.low<position.avg_price*1.10 
                and snap.high>position.avg_price*1.10 and history_prices[-1] - avg[-1] < 0 and history_prices[-2] - avg[-2] > 0):
                    order_target_percent(code,0,position.avg_price*1.10)
                elif(code in context.selllist):  
                    if position.sellable > 0:
                        if is_suspended(code):
                            #停牌无法卖出
                            continue
                        if snap.last <= snap.limit_down:
                            #print('bad limit_down', now, code)
                            #一字跌停无法卖出
                            continue
                        if snap.last >= snap.limit_up:
                            #涨停不用卖出
                            #print('good limit_up', now, code)
                            continue
                        #print('sell', now, code, position.sellable,snap.last)
                        
                        order_target_percent(code, 0, snap.last)
            except Exception as e:
                print(code,snap)

def handle_bar(context, bar_dict):
    now = context.now.strftime('%Y%m%d')
    before_trading(context)
    buy(context, bar_dict)
    sell(context, bar_dict)
    after_trading(context)
    #plot('market', context.portfolio.market_value/context.portfolio.total_value)
    #plot('stocknum', len(context.operlist))
    #print('%s, %4.2f, %10.2f' % (now, context.portfolio.market_value/context.portfolio.total_value, context.portfolio.total_value))
def after_trading(context):
    pass

if __name__ == "__main__":
    param =  params.PARAMS
    results = run_func(init=init, handle_bar=handle_bar, config=param['_config'])