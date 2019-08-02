# -*- coding: utf-8 -*-
import sys,os,time
import rqdata
from asset import Asset
import talib as ta
import pandas as pd
import numpy as np
import argparse
import get_code_and_pro as mn
import evaluate as ev
import argparse

def kdj_calc(highs, lows, closes, v1=9,v2=3,v3=3,mtype=0):
    K, D = ta.STOCH(highs,lows,closes,
        fastk_period=v1,slowk_period=v2,
        slowk_matype=mtype,slowd_period=v3,slowd_matype=mtype)
    J = []
    for i in range(len(K)):
        J.append(3*K[i]-2*D[i])
    return K,D,np.array(J)

def macd_calc(closes,v1=12,v2=26,v3=9):
    return ta.MACD(closes,fastperiod=v1, slowperiod=v2, signalperiod=v3)

class StrategyDemo:
    def __init__(self, startdate, enddate, totalmoney, period, logfile='./tradeinfo.csv'):
        self.HS_DATA = rqdata.history_bars('399300.XSHE',start='20120101',end=enddate)['data']
        
        self.totalmoney = totalmoney
        self.asset = Asset(totalmoney, TradeLog=logfile)
        self.startdate = startdate
        self.enddate = enddate
        self.prevdate = None
        self.period = period

    # 每日的交易函数
    # curdate 当前日期 buy_status 是否允许交易 clr_status 是否强制空仓
    def trade(self, curdate, buy_status, clr_status):
        if clr_status:
            for code in self.asset.hold:
                L = rqdata.get_1d_data(code, curdate, offline=True)
                if L.shape[0] < 30:
                    continue
                opens= np.array(L['open'].tolist())
                self.asset.sell(code, opens[-1])
        if buy_status:
            codelist, weights = mn.main(self.prevdate)
            for i in range(len(codelist)):
                code = codelist[i]
                weight = weights[i]
                L = rqdata.get_1d_data(code, curdate, offline=True)
                if L.shape[0] < 30:
                    continue
                opens = np.array(L['open'].tolist())
                self.asset.buy(code, opens[-1], min(self.asset.remain, self.asset.total*weight))

    # 返回最终净值
    def run(self):
        startdate = self.startdate
        enddate = self.enddate
        jz = self.totalmoney        

        count = 0
        for i in range(30, self.HS_DATA.shape[0]):
            curdate = self.HS_DATA['date'][i]
            self.prevdate = self.HS_DATA['date'][i-1]
            if curdate < startdate or curdate > enddate:
                continue
            self.trade(curdate, count==0, count==0)
            if count == 0:
                count = self.period
            jz = self.asset.after_trade(curdate)
            count -= 1

        return jz / self.totalmoney


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('--start','-s', required = True, type = str)
    #parser.add_argument('--end','-e', required = True, type = str)
    parser.add_argument('--funding','-f', type = int, default=10000000)
    parser.add_argument('--period','-p', type = int, default=60)
    
    args = parser.parse_args()
    #st = StrategyDemo(args.start, args.end, args.funding, args.period)
    st = StrategyDemo('20160101','20190401',10000000,60)
    st.run()
    ev.eval_model()

