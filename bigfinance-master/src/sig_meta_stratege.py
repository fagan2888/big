# -*- coding: utf-8 -*-
# __author__ = 'Li sz'

# 本脚本的功能为对收益进行回测
import sig_data
import pandas as pd 
import numpy as np
import tushare as ts 
import datetime
import os
import copy
import warnings
import sig_fra
import sharpe_2
import index_24
import sys
from rqdata import up_file,now_file
sys.path.append(now_file)
import get_code_and_pro as gcap

#warnings.filterwarnings("ignore")

buy_fee = 1.0008 #买入手续费万8
sell_fee = 0.9992 #卖出手续费万18
Slippage = 0.003 #滑点
buy_need = 1.03 #上界
sell_need = 0.98 #下界
#Slippage = 0
Original_gold = 100000

dp_code = '999999.XSHG'
dp_trade_date = sig_data.get_dp_trade_date(dp_code)#上证指数的交易日期列表
#dp_trade_date = np.array([str(i) for i in dp_trade_date])

Expression =['close_EMA_5#2#1&trend']
meta_stra_name = 'trend_long_short'
result_save_path = up_file+'/result/'+meta_stra_name

class Worth:
    
    #初始化函数，初始化元素为股票代码，分数阶差分阶数，可操作资金，此股票仓位，买入价格，卖出价格，净值，模型名字，
    #原始数据bar，时间，操作,一个bar数据的窗口大小，本金，还剩多少天买，还剩多少天卖
    
    def __init__(self,code = '',w = 10,gold = 0,position = 0,asset = 0,buy_price = 0,sell_price = 0,now_date = '',
                pure_value = 1,date = '',operation = 'noo',original_gold = Original_gold,buy_due = 0,sell_due = 0,trade_date_list = [],
                now_bar = [],obuy_price = 0,expre_Sig = []):
        self.code = code #股票代码 
        self.w = w #m每日数据获取的窗口大小
        self.gold = gold #钱
        self.position = position #仓位
        self.asset = asset #总的财产
        self.buy_price = buy_price #当天的买入价格，每天更新
        self.sell_price = sell_price #当天的卖出价格，每天更新
        self.ori_buy_price = obuy_price #买入当天的买入价格
        self.pure_value = pure_value #净值
        self.date = date #买入时间的前一天，因为是开盘买入，所以能用的数据只能到前一天
        self.operation = operation #操作
        self.original_gold = original_gold #本金
        self.buy_due = buy_due #还剩多少天买，盘后减一
        self.sell_due = sell_due #买了后还剩多少天卖，盘后减一
        self.trade_date_list = trade_date_list  #这只股票的交易时间列表
        self.now_date = now_date # 当天的时间，每天更新
        self.now_bar = now_bar #当天的数据bar，每天更新
        self.expre_Sig =  expre_Sig #每天的expression的信号
        self.l_or_s = 'noo' #判断是做多还是做空
    #某一天的买入卖出函数
    
    def one_code_trade(self,):
        #all_buy_price = 100*self.buy_price*buy_fee*(1+Slippage)#加入了滑点和手续费
        #all_sell_price = 100*self.sell_price*sell_fee*(1-Slippage)#加入了滑点和手续费
        all_buy_price = 100*self.buy_price#不加入滑点和手续费
        all_sell_price = 100*self.sell_price#不加入滑点和手续费
        if(not self.now_bar.empty and 'close' in self.now_bar.keys()):
            settle = self.now_bar['close'].iloc[-2]  #得到昨天的收盘价，用来判断涨跌停
            close = self.now_bar['close'].iloc[-1]
        else:
            settle = self.buy_price  #当出现了那天没有数据后，用前一天的trade_price代替
            close = self.buy_price

        trade_gold = 0 #交易金钱
        trade_price = 0 #交易价格
        is_make_money = 0
        if(self.sell_price>0.9*settle and self.sell_price<1.1*settle):#涨跌停不能买卖
            #做多或者做空
            if(self.l_or_s == 'noo' and 
                (self.operation == 'long' or self.operation == 'short') 
                and self.gold>all_buy_price and self.buy_price!=0): 
                    #buy_position = int(self.gold/all_buy_price)
                    buy_position = 1 #只买一手
                    self.position = self.position+buy_position#不用迭代的方式会出现股票价格大跌时再次买入资产断崖式下跌
                    trade_gold = all_buy_price*buy_position
                    trade_price = self.buy_price
                    self.gold = self.gold-all_buy_price*buy_position
                    self.l_or_s = copy.copy(self.operation)
                    self.ori_buy_price = self.buy_price
            #卖出
            elif(self.operation == 'sell' and self.position>0 and self.sell_price!=0):
                trade_gold = all_sell_price*self.position           
                trade_price = self.sell_price
                if(self.l_or_s == 'long'):#做多是正常卖出，本金增加
                    self.gold = self.gold+all_sell_price*self.position
                    if(trade_price>self.ori_buy_price):
                        is_make_money = 1
                else:#做空是还贷买入，本金其实是减少了的
                    self.gold = self.gold-all_sell_price*self.position+2*self.position*100*self.ori_buy_price
                    if(trade_price<self.ori_buy_price):
                        is_make_money = 1
                self.position = 0
        if(self.operation == 'long'):
            self.asset = self.gold+100*self.position*close
        else:#做空的净值其实是要减去仓位乘以当天的收盘的
            self.asset = self.gold+100*self.position*self.ori_buy_price
        self.pure_value = self.asset/self.original_gold
        return self.position,trade_gold,close,trade_price,self.now_date,self.expre_Sig,is_make_money
    
    '''
    #得到操作信号
    def get_operation(self,):
        if(not self.now_bar.empty):
            if(self.expre_Sig[0] == 2 and self.expre_Sig[1] == 2 and self.expre_Sig[2] == 4): #or self.expre_Sig[2] == 2):
                self.operation = 'long'
            elif(self.expre_Sig[0] == 1 and self.expre_Sig[1] == 1 and self.expre_Sig[2] == 1): #and self.expre_Sig[4] == 1):
                self.operation = 'short'
            elif(self.l_or_s == 'long' and (self.expre_Sig[0] == 1 or self.expre_Sig[1] == 1 or self.expre_Sig[2] == 1)): #加入全局风控
                self.operation = 'sell'
            elif(self.l_or_s == 'short' and (self.expre_Sig[0] == 2 or self.expre_Sig[1] == 2 or self.expre_Sig[2] == 4)): #加入全局风控
                self.operation = 'sell'
        return self.operation
    '''
    def get_operation(self,):
        if(not self.now_bar.empty):
            if(self.expre_Sig[0] == 1): #or self.expre_Sig[2] == 2):
                self.operation = 'long'
            elif(self.expre_Sig[1] == 1): #加入全局风控
                self.operation = 'short'
        return self.operation

    # 得到买入和卖出的价格
    def get_trade_price(self,):
        if(not self.now_bar.empty and 'close' in self.now_bar.keys()):
            self.buy_price = self.now_bar['close'].iloc[-1] #以当天收盘价为买入价格
            self.sell_price = self.now_bar['close'].iloc[-1] #以当天收盘价为卖出价格
        
    #得到单只股票的交易时间列表
    def get_trade_date_list(self,):
        #self.trade_date_list = sig_data.get_wm_data(self.code).index.values
        self.trade_date_list = pd.read_csv(up_file+'/index/'+self.code+'.csv',index_col='date').index.values #这样直接读取离线数据会快很多
        #self.trade_date_list = np.array([str(i) for i in self.trade_date_list ])
        self.trade_date_list = np.array([int(i) for i in self.trade_date_list ])
    #买卖日期初始化
    def due_init(self,):
        self.buy_due = 0 #信号出来的当天买
        self.sell_due = 0 #信号出来的当天卖
    
    #买日期更新
    def buy_due_close(self,):
        self.buy_due = self.buy_due-1
    
    #卖日期更新
    def sell_due_close(self,):
        self.sell_due = self.sell_due-1
    
    #得到现在的数据bar
    def get_now_bar(self,now_date):
        self.now_date = now_date
        #(now_date,type(self.now_date),self.code)
        data = sig_data.get_windows_data(self.code,self.now_date,self.w)
        self.now_bar = copy.copy(data)
    
    #更新每天的交易价格，这个后面可以改成在交易时才更新#################
    def update_trade_price(self,now_date):
        self.get_now_bar(now_date)
        self.get_trade_price()
    
    # 目前的思路是分每个交易日的数据输入，得到每天的一个交易，如果是大于0就买，小于0就卖，
    # 因为一个的信号是得到了两天的操作，也就是说明天和后天的操作都被确定，但是这样可能出现两天的操作相悖，
    # 也就是会出现一天中又买又卖，目前的处理是买就加一，卖就减一，那么如果两天的操作相悖的话就会抵消。
    def update_Worth(self,):
        self.due_init()
        self.update_trade_price(self.date) # 得到第二天的bar，更新买入卖出的价格，这个在实际操作的时候要放到交易时
        self.get_trade_date_list() # 得到单只股票的交易时间列表
        if(not self.now_bar.empty and 'close' in self.now_bar.keys()):
            return self.now_bar['close'].iloc[-1],sig_data.get_windows_data(dp_code,self.now_date,self.w)['close'].iloc[-1]
        else:
            return 0,0
    

class Result:
    def __init__(self,date_list = [],asset_list = [],y_pre_list = [],position_list = [],
                 trade_gold_list = [],close_list = [],trade_price_list = [],trade_date_list = [],
                 gold_list = [],code_list = [],is_make_money = [],expre_sig_list =[]):
        self.date_list = date_list #时间list
        self.asset_list = asset_list #资金list
        self.close_list = close_list #资金list
        self.y_pre_list = y_pre_list #操作list
        self.position_list = position_list #仓位list
        self.trade_gold_list = trade_gold_list #交易金额list
        self.close_list = close_list #closelist
        self.trade_price_list = trade_price_list #交易价格list
        self.trade_date_list = trade_date_list #交易时间list
        self.gold_list = gold_list #所剩现金list
        self.code_list = code_list #操作股票列表
        self.expre_sig_list = expre_sig_list
        self.is_make_money = is_make_money #操作是否挣钱


class CStock:#计算选股模型的净值
    #初始化函数，类里面的元素为目前的资金，单位为元，已经买入的股票列表，
    #明天要买入的股票列表，要卖出的股票列表，总共可以挑选的股票列表
    def __init__(self,_nowdate='',ori_gold = 0,gold = 0,asset = 0,have_buy_stocks_list = [],have_buy_stocks_Worth = [],
                 tomorrow_buy_stocks_list = [],tomorrow_buy_stocks_Worth = [],dp_trade_date = dp_trade_date,close = 1,
                 today_sell_stocks_list = [],could_choose_stocks_list = [],result = Result(),all_choose_stocks_list = [],
                 init_close = 0,Expression = [],result_save_path = result_save_path):
        self.ori_gold = ori_gold #本金
        self._nowdate = _nowdate
        self.gold = gold #现有可投入资金
        self.asset = asset #现有总资金
        self.hbsl = have_buy_stocks_list #已经买了的股票列表
        self.hbsW = have_buy_stocks_Worth #已经买了的股票的worth列表
        self.tbsl = tomorrow_buy_stocks_list #将要买的股票列表
        self.tbsW = tomorrow_buy_stocks_Worth #将要买的股票的worth列表
        self.tssl = today_sell_stocks_list #今天要卖的股票列表
        self.ccsl = could_choose_stocks_list #可以挑选的股票列表
        self.acsl = all_choose_stocks_list #所有可以挑选的股票列表
        self.result = result
        self.dp_trade_date = dp_trade_date
        self.close = close # 用来算持仓不动的结果 
        self.init_close = init_close # 第一个收盘
        self.Sig = sig_fra.Signal(expression= Expression,code_list = self.ccsl,date = _nowdate)#创建信号系统
        self.Sig.dict_init()#初始化信号系统

        self.result_save_path = result_save_path

    #得到日期
    def get_date(self,):#trade_date放里面还是放外面
        if(self._nowdate != dp_trade_date[-1]):
            self._nowdate = dp_trade_date[np.where(dp_trade_date == self._nowdate)[0][0]+1]
            return 1
        else:
            print("have done")
            return 0
    
    #得到每只股票的资金
    def get_every_code_gold(self,):
        if(len(self.tbsl)):
            #evg = int(self.gold/(len(self.tbsl))) #所有股票均分现有资金
            evg = int(self.gold/(3*len(self.tbsl))) #所有股票均分现有资金的三分之一
            self.gold = self.gold-evg*len(self.tbsl) #得到现有资金
            return evg #更新每只股票的资金
        return len(self.tbsl)
    
    #买bar
    def buy_bar(self,):
        every_gold = self.get_every_code_gold()#这里必须放到循环前面，不然会导致买多只股票时后面的股票分到的钱为0
        for _code,_worth in zip(self.tbsl,self.tbsW):#####这里以后可能还要改，因为可能有些信号不是立即买，那么分配钱就有问题#######
            _worth.gold = every_gold
            if(_worth.buy_due <= 0):
                position,trade_gold,close,trade_price,trade_date,expre_sig,is_make_money = _worth.one_code_trade()
                if(trade_gold>0): #如果交易金额大于0
                    self.add_result(_code,position,trade_gold,close,trade_price,trade_date,expre_sig,is_make_money)
                    self.hbsl.append(_code)
                    self.hbsW.append(_worth)
                else:#如果出现涨停或者钱不够没有买，则下一次再根据信号买
                    self.gold = self.gold + _worth.gold #把没有交易的股票的钱拿回来

                
                
    #卖bar
    def sell_bar(self,):
        for _code,_worth in zip(self.hbsl,self.hbsW):
            if(_code in self.tssl):
                position,trade_gold,close,trade_price,trade_date,expre_sig,is_make_money = _worth.one_code_trade()
                if(trade_gold>0): #如果交易金额大于0
                    self.gold = self.gold + _worth.gold #这里要放条件判断的下面，否则会出现累加的情况
                    self.add_result(_code,position,trade_gold,close,trade_price,trade_date,expre_sig,is_make_money)
                if(_worth.position <= 0):#清除已买股票列表和worth列表中仓位为0的股票
                    self.hbsl.remove(_code)
                    self.hbsW.remove(_worth)
    
    #用昨天的信号得到今天天要买的股票和worth
    def get_tbsl(self,):
        self.tbsl,self.tbsW = [],[] #将今天要买的股票列表和worth清空
        for _code in self.ccsl:
            _worth = Worth(code = _code,gold = 0,position = 0,asset = 0,buy_price = 0,w = 100,
                          sell_price = 0,pure_value = 1,date = self._nowdate,operation = 'noo',obuy_price = 0,
                          expre_Sig=copy.copy(self.Sig.expre_sig[_code]))#买入用的是昨天的信号和昨天的大趋势
            
            self_close,temp = _worth.update_Worth()
            if(temp): #用来计算持仓不动的结果,当数据中没有close的时候不改变
                self.close = temp
                if(self.init_close == 0):
                    self.init_close = self.close
                self.close = self.close/self.init_close
			#计算今天的信号，给第二天用
            if(not _worth.now_bar.empty and len(_worth.now_bar)>1):#要求不仅非空而且长度要大于1
                self.Sig.trend_cal(self._nowdate) #trend计算
                self.Sig.type_sig(data = copy.copy(_worth.now_bar),code = _code) #Sig计算
            else:
                self.Sig.expre_sig[_code] = np.zeros(len(self.Sig.expression))
            #把今天要买的股票加入列表
            _opera = copy.copy(_worth.get_operation())
            if(_opera == 'long' or _opera == 'short' or _opera == 'noo'):
                self.write_one_code_result(_code,_opera)
            if(_worth.date in _worth.trade_date_list and 
                (_opera == 'long' or _opera == 'short') 
                and _worth.code not in self.hbsl):
                self.tbsl.append(_code)    
                self.tbsW.append(_worth)
            self.result.y_pre_list.append(copy.copy(self.Sig.expre_sig[_code]))
    
    #得到今天要卖的股票列表
    def get_tssl(self,):
        self.tssl = []
        for _code,_worth in zip(self.hbsl,self.hbsW):
            _worth.expre_Sig = self.Sig.expre_sig[_code]#卖出用的当天的信号，因为这个函数在得到买入股票之后，信号已经更新了
            if(_worth.now_date in _worth.trade_date_list and 
                ( _worth.get_operation() == 'sell' and _worth.sell_due <= 0
                or _code not in self.ccsl)): #出现卖的信号或者换仓的时候平仓
                self.tssl.append(_code)
                self.write_one_code_result(_code,'sell')
                #_worth.operation = 'sell'

    #开盘前操作
    def before_open(self,):
		#更新买卖价格为当天开盘和收盘
        for _code,_worth in zip(self.tbsl,self.tbsW):
            _worth.buy_due_close() #买due减一
            _worth.update_trade_price(self._nowdate)
        for _code,_worth in zip(self.hbsl,self.hbsW):
            _worth.sell_due_close() #卖due减一
            _worth.update_trade_price(self._nowdate)
        self.get_tssl() #得到今天要卖的股票列表
        self.get_tbsl() #获得今天要买的股票列表和worth
        self.write_all_code_result()
        self.Sig.date = self._nowdate #Sig的日期更新

    #盘后操作
    def after_close(self,):
        self.update_gold() #先更新资金量，再更新将要买的列表
        for _code,_worth in zip(self.hbsl,self.hbsW):
            if(not _worth.now_bar.empty and 'close' in _worth.now_bar.keys()):
                if(_worth.l_or_s == 'long'):#这里也要分是做多还是做空
                    _worth.asset = _worth.gold+100*_worth.position*_worth.now_bar['close'].iloc[-1]#在更新now_bar之前更新已买入股票的资产
                else:
                    _worth.asset = _worth.gold+100*_worth.position*_worth.ori_buy_price#在更新now_bar之前更新已买入股票的资产
            #这里还要重复是因为在不交易的时候也能更新持仓净值，否则就会出现直线                                             
        self.Sig.update()
    
    #每天交易结束之后把每只买了的股票的剩余资金加起来
    def update_gold(self,):
        for _worth in self.hbsW: #这里还是改成了已经买了的股票，之前已经把没有买成功的股票的钱加起来
            self.gold = self.gold + _worth.gold
            _worth.gold = 0 #把每只股票里的gold清零

    #交易bar
    def trade_bar(self,):#卖的操作没有jie
        self.before_open() #盘前操作
        self.sell_bar() #卖
        self.buy_bar() #买
        self.after_close() #盘后操作
        if(self.get_date() == 0): #更新日期，如果到了最后一个交易日，无法再继续更新日期
            return 0
        return 1
    
    #得到总的资产，是剩下的钱加上持仓的股票的asset
    def get_asset(self,):
        self.asset = self.gold
        for _code,_worth in zip(self.hbsl,self.hbsW):
            self.asset = self.asset + _worth.asset
    #自动交易
    def trade(self,):
        self.result.date_list.append(self._nowdate)
        flag = self.trade_bar()
        self.get_asset()
        self.result.asset_list.append(self.asset)
        self.result.close_list.append(float(self.close))
        self.result.gold_list.append(float(self.asset/self.result.asset_list[0]))
        if(flag == 0):
            return 0
        return self._nowdate
    
    #把trade_result_list结果储存
    def add_result(self,code,position,trade_gold,close,trade_price,trade_date,expre_sig,is_make_money):
        self.result.position_list.append(position)
        self.result.trade_gold_list.append(trade_gold)
        #self.result.close_list.append(close)
        self.result.trade_price_list.append(trade_price)
        self.result.trade_date_list.append(str(trade_date))#+'_'+code)
        self.result.expre_sig_list.append(str(expre_sig))
        self.result.code_list.append(code)
        self.result.is_make_money.append(is_make_money)

    def write_all_code_result(self,):
        w_s = self.result_save_path+'code/'
        if not os.path.exists(w_s):
            os.makedirs(w_s)
        if not os.path.exists(w_s+'all_operation.txt'):
            with open(w_s+'all_operation.txt','a') as f:
                f.write('time'+' '+'code'+' '+'operation\n')
                f.close()
        for code in self.tbsl:
            with open(w_s+'all_operation.txt','a') as f:
                f.write(str(self._nowdate)+' '+code+' '+'buy\n')
                f.close()
        for code in self.tssl:
            with open(w_s+'all_operation.txt','a') as f:
                f.write(str(self._nowdate)+' '+code+' '+'sell\n')
                f.close()

    def write_one_code_result(self,code,operation):
        w_s = self.result_save_path+'code/'
        if not os.path.exists(w_s):
            os.makedirs(w_s)
        if not os.path.exists(w_s+code+'_operation.txt'):
            with open(w_s+code+'_operation.txt','a') as f:
                f.write('time'+' '+'operation\n')
                f.close()
        with open(w_s+code+'_operation.txt','a') as f:
            #print(str(operation),)
            f.write(str(self._nowdate)+' '+str(operation)+'\n')
            f.close()
            

# 得到交易一些记录，para_data是净值和资金的记录，每天都有记录；
# trade_data是交易的记录，只有在交易时才会有记录
def para_result(para_data,trade_data,C_S):
    #para_data['asset']=copy.copy(C_S.result.asset_list)
    para_data['dp_pure']=copy.copy(C_S.result.close_list)
    para_data['pure_value']=copy.copy(C_S.result.gold_list) #这里是净值序列
    #para_data['expre_sig']=copy.copy(C_S.result.y_pre_list)
    
    trade_data['code']=copy.copy(C_S.result.code_list)
    trade_data['expre_sig']=copy.copy(C_S.result.expre_sig_list)
    trade_data['is_make_money']=copy.copy(C_S.result.is_make_money)
    #trade_data['close']=copy.copy(C_S.result.close_list)
    trade_data['trade_price']=copy.copy(C_S.result.trade_price_list)
    trade_data['trade_gold']=copy.copy(C_S.result.trade_gold_list)
    trade_data['position']=copy.copy(C_S.result.position_list)
    
    return para_data,trade_data

def get_code_list():
    code_list = ts.get_hs300s()['code']
    for i in range(len(code_list)):
        if(str(code_list[i])[0]=='6'):
            code_list[i] = str(code_list[i]) + '.XSHG'
        else:
            code_list[i] = str(code_list[i]) + '.XSHE'
    return code_list.tolist()

def get_all_code(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        return files #当前路径下所有非目录子文件  


def All_trade(code_list,begin_date,result_save_path = result_save_path,Expression = Expression):
    para_name = 'year/'
    para_data,trade_data = {},{}
    ori_gold = 100000000
    C_S = CStock(ori_gold = ori_gold,_nowdate = begin_date,could_choose_stocks_list = code_list,all_choose_stocks_list = code_list,
                    gold = ori_gold,asset = 0,have_buy_stocks_list = [],have_buy_stocks_Worth = [],
                    tomorrow_buy_stocks_list = [],tomorrow_buy_stocks_Worth = [],result = Result(asset_list = [],close_list = [],
                    y_pre_list = [],position_list = [],trade_gold_list = [],trade_price_list = [],date_list = [],trade_date_list = [],
                    gold_list = [],code_list = [],is_make_money = [],expre_sig_list =[]),today_sell_stocks_list = [],Expression = Expression,result_save_path = result_save_path)
    while(C_S.trade()): #and C_S._nowdate[0:4]==begin_date[0:4]):#当到第二年时重置净值和仓位
        pass
    para_data,trade_data = para_result(para_data,trade_data,C_S)
    date_list = [int(a) for a in C_S.result.date_list]
    para_data = pd.DataFrame(para_data,index = date_list)
    
    if(not os.path.exists(result_save_path+para_name)):
            os.makedirs(result_save_path+para_name)

    para_data.to_excel(result_save_path+para_name+str(begin_date)[0:4]+"_pure.xlsx", header=True, index=True)
    trade_date_list = [int(a) for a in C_S.result.trade_date_list]
    trade_data = pd.DataFrame(trade_data,index = trade_date_list)
    trade_data.to_excel(result_save_path+para_name+str(begin_date)[0:4]+"_trade.xlsx", header=True, index=True)

    return C_S.result.gold_list[-1]

def main(result_save_path = result_save_path,Expression = Expression):
    code_list = ['000001.XSHE','000016.XSHE']#,'601398.XSHG','000027.XSHE','000046.XSHE']
    #code_list = get_all_code(now_file+'/wmdata')
    #code_list = get_code_list()
    _code_list = copy.copy(code_list)
    off_line=False
    if(not off_line):
        for code in code_list:
            if(sig_data.cal_index_data(code) == 0):
                _code_list.remove(code)
        sig_data.cal_index_data('999999.XSHG')
    if('999999.XSHG' in code_list):
        _code_list.remove('999999.XSHG')
    begin_year = 2015
    begin_date = dp_trade_date[dp_trade_date>=int((str(begin_year)+'0101'))][0]
    WD_pv = All_trade(_code_list,begin_date,result_save_path,Expression)
    print(WD_pv)

if __name__ == "__main__":
    for w in [5,10,20,40,80]:
        _Expression =['close_EMA_'+str(w)+'#2#1&trend','close_EMA_'+str(w)+'#2#0&trend']
        _meta_stra_name = 'trend_long_short'
        _result_save_path = up_file+'/result/'+_meta_stra_name+'/'+str(w)+'/'
        main(result_save_path = _result_save_path,Expression = _Expression)