# -*- coding: utf-8 -*-
import sys,os,time
import rqdata
import math
import json

#  该Asset类用于旧版策略回测（存在程序退出后持仓无法还原的问题，不适用于模拟实盘）
class Asset:
    def __init__(self, TotalMoney, Slip = 0.003, Fee = 0.0003, 
                    TradeLog='./tradeinfo.csv', HoldLog='./holdinfo.csv'):
        self.remain = TotalMoney  # 剩余可用资金
        self.total  = self.remain # 总资产
        self.inital = self.remain # 初始资金
        self.slip_point = Slip
        self.fee = Fee
        self.del_list = []
        self.hold = {}  # # code : [股数,成交均价,可卖股数,当日买入股数,持仓天数]
        self.operation = ''
        self.logfile = TradeLog
        f = open(self.logfile,'w')
        f.close()

    def buy(self, code, price, use_money):
        price *= 1 + self.slip_point
        #买入股数
        num = int(use_money / price / 100) * 100

        if num == 0:
            return False

        if code in self.hold:
            self.hold[code][1] = (self.hold[code][0]*self.hold[code][1] + num*price) / (num + self.hold[code][0])
            self.hold[code][0] += num
            self.hold[code][3] += num
            self.hold[code][4] = 0
        else:
            self.hold[code] = [num ,price, 0, num, 0]
        
        self.operation += 'B/%s/%.2f/%d,'%(code,price,num)

        self.remain -= num * price
        if num > 0:
            self.remain -= max(5, int(num * price * self.fee))
        return True

    def sell(self, code, price):
        price *= 1 - self.slip_point
        
        self.remain += self.hold[code][2] * price
        if self.hold[code][2] > 0:
            self.remain -= max(5,int(self.hold[code][2] * price * self.fee))

        self.operation += 'S/%s/%.2f/%d,'%(code,price,self.hold[code][2])

        if self.hold[code][0] - self.hold[code][2] == 0:
            self.hold[code] = [0,0,0,0,0]
            self.del_list.append(code)
        else:
            self.hold[code][0] -= hold[code][2]
            self.hold[code][2] = 0
            self.hold[code][4] = 0

    def after_trade(self, curdate):  #交易结束后当日新买入股票变为可卖出股票 并删去已平仓股票
        for code in self.del_list:
            if self.hold[code][0] != 0:
                continue
            del self.hold[code]
        self.del_list = []
        for code in self.hold:
            self.hold[code][2] += self.hold[code][3]
            self.hold[code][3] = 0 
            self.hold[code][4] += 1
        
        # 统计总资产
        self.total = self.remain
        for code in self.hold:
            price = rqdata.get_1d_data(code, curdate, limit=1, fixed=False, offline=True)['close'].tolist()[0]
            self.total += self.hold[code][0] * price
        
        # 输出当日总资产和操作记录
        f = open(self.logfile,'a')
        f.write('%s,%.2f,%s\n'%(curdate,self.total,self.operation))
        print('[INFO]Date %s TotalMoney'%curdate, self.total)
        f.close()
        self.operation = ''
        return self.total


 
