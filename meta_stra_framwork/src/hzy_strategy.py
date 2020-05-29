import sys
sys.path.append('.')
import click
import requests
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows',    None)
import json
import traceback
import requests
import pandas as pd
from rqalpha.api import *
from rqalpha import run_func
import os
#import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import talib
import params
#from rqalpha.api import get_turnover_rate
k = 10
hzy_siganl_path = '/Users/wode/Documents/signal_framework/big/meta_stra_framwork/result/hzy/'

def myround(value, n):
    if value > 0:
        return round((value + 10**(-n-8)), n)
    else:
        return round((value - 10**(-n-8)), n)

def init(context):
    
    #code_list = ['000001.XSHE','600000.XSHG']
    #code_list = get_code_list()
    #expression = ['(close#7#1&thre+close#open#1&cross)*high#8#0&thre','(low#7#1&thre+close#open#1&cross)*high#8#0&thre']
    context.signals         = pd.read_csv(hzy_siganl_path+'last_sig.csv')
    #print(context.signals)
    context.signals         = context.signals[context.signals.code!='601360.XSHG']
    context.signals.time    = context.signals.time.map(lambda x:str(x))
    #print(context.signals,context.signals.time)
    context.operlist        = []
    context.selllist        = []
    context.opergroup       = 3
    context.period       = 5

def before_trading(context):
    now = context.now.strftime('%Y%m%d')
    yes = get_previous_trading_date(now).strftime('%Y%m%d')
    selected = context.signals[np.multiply(context.signals.time==now,context.signals.operation == 'long')]
    selled = context.signals[np.multiply(context.signals.time==now,context.signals.operation == 'long_sell')]
    #print(context.signals[context.signals.time==yes])
    if selected.empty:
        context.operlist = []
    else:
        context.operlist = list(selected.code)
        
    if(selled.empty):
        context.selllist = []
    else:
        context.selllist = list(set(list(selled.code)))
        
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
            #tr = rqalpha.api.get_turnover_rate(code,count = 1,expect_df=True)
            #print(tr)
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
                order_value(code, cash_each,snap.open)
            except Exception as e:
                print(e)
                
                
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
                #if(code in context.selllist):
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
                #elif(snap.low<position.avg_price*0.90 and snap.high>position.avg_price*0.90):
                    #order_target_percent(code,0,position.avg_price*0.90)
                #elif(snap.low<position.avg_price*1.10 and snap.high>position.avg_price*1.10 and history_prices[-1] - avg[-1] < 0 and history_prices[-2] - avg[-2] > 0):
                    #order_target_percent(code,0,position.avg_price*1.10)
            except Exception as e:
                print(e)
def handle_bar(context, bar_dict):
    now = context.now.strftime('%Y%m%d')
    before_trading(context)
    buy(context, bar_dict)
    sell(context, bar_dict)
    after_trading(context)
    plot('market', context.portfolio.market_value/context.portfolio.total_value)
    #plot('stocknum', len(context.operlist))
    print('%s, %4.2f, %10.2f' % (now, context.portfolio.market_value/context.portfolio.total_value, context.portfolio.total_value))
def after_trading(context):
    pass

if __name__ == "__main__":
    param =  params.PARAMS
    results = run_func(init=init, handle_bar=handle_bar, config=param['_config'])