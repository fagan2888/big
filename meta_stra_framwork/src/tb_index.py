import pandas as pd
import numpy as np
import talib as ta
import math
import diff
import copy

######
#重叠指标
######

def calculateEMA(df,name,period,d = 0): #period 为天数参数
    """计算指数移动平均"""
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    Array=np.array(df[str(name)])
    _df[str(name) + '_EMA_' + str(period)] = ta.EMA(Array, period)
    return _df

def calculateMA(df,name,period,d = 0): #period 为天数参数
    """计算移动平均"""
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    Array=np.array(df[str(name)])
    _df[str(name) + '_MA_' + str(period)] = ta.MA(Array, period)
    return _df

def calculateSMA(df,name,period,d = 0): #period 为天数参数
    """计算简单移动平均"""
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    Array=np.array(df[str(name)])
    _df[str(name) + '_SMA_' + str(period)] = ta.SMA(Array, period)
    return _df

def calculateWMA(df,name,period,d = 0): #period 为天数参数
    """计算加权移动平均"""
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    Array=np.array(df[str(name)])
    _df[str(name) + '_WMA_' + str(period)] = ta.WMA(Array, period)
    return _df

def calculateDEMA(df,name,period,d = 0): #period 为天数参数
    """计算双移动平均"""
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    Array=np.array(df[str(name)])
    _df[str(name) + '_DEMA_' + str(period)] = ta.DEMA(Array, period)
    return _df

def calculateTEMA(df,name,period,d = 0): #period 为天数参数
    """计算三重指数移动平均"""
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    Array=np.array(df[str(name)])
    _df[str(name) + '_TEMA_' + str(period)] = ta.TEMA(Array, period)
    return _df

def calculateTRIMA(df,name,period,d = 0): #period 为天数参数
    """计算三角移动平均"""
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    Array=np.array(df[str(name)])
    _df[str(name) + '_TRIMA_' + str(period)] = ta.TRIMA(Array, period)
    return _df

def calculateKAMA(df,name,period,d = 0): #period 为天数参数
    """计算考夫曼自适应移动平均"""
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    Array=np.array(df[str(name)])
    _df[str(name) + '_KAMA_' + str(period)] = ta.KAMA(Array, period)
    return _df

def calculateMAMA(df,name,d = 0): #period 为天数参数
    """计算MESA自适应移动平均"""
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    Array=np.array(df[str(name)])
    _df[str(name) + '_MAMA'] = ta.MAMA(Array)
    return _df

#根据给定的周期列表计算所有的均线
def calculate_allMA(df,name,period_list,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    Array=np.array(df[str(name)])
    _df[str(name) + '_MAMA'],_df[str(name) + '_FAMA'] = ta.MAMA(Array)
    for period in period_list:
        _df[str(name) + '_MA_' + str(period)] = ta.MA(Array, period)
        _df[str(name) + '_SMA_' + str(period)] = ta.SMA(Array, period)
        _df[str(name) + '_WMA_' + str(period)] = ta.WMA(Array, period)
        _df[str(name) + '_DEMA_' + str(period)] = ta.DEMA(Array, period)
        _df[str(name) + '_TEMA_' + str(period)] = ta.TEMA(Array, period)
        _df[str(name) + '_TRIMA_' + str(period)] = ta.TRIMA(Array, period)
        _df[str(name) + '_KAMA_' + str(period)] = ta.KAMA(Array, period)
        _df[str(name) + '_EMA_' + str(period)] = ta.EMA(Array, period)
    return _df
##########
#还有三重指数移动平均线没写
##########

#布林带
def calculateBBANDS(df,period,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray=np.array(df['close'])
    H_line,M_line,L_line=ta.BBANDS(CloseArray, timeperiod=period, nbdevup=2, nbdevdn=2, matype=0)
    _df['H_line_'+ str(period)]=H_line
    _df['M_line_'+ str(period)]=M_line
    _df['L_line_'+ str(period)]=L_line
    return _df

#Midpoint over period
def calculateMAVP(df,period,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray=np.array(df['close'])
    _df['MAVP_'+ str(period)]=ta.MAVP(CloseArray,period)
    return _df

#希尔伯特瞬时变换
#Moving average with variable period
#Midpoint Price over period
#抛物线指标
#抛物线扩展指标
def calculateOverlap_others(df,period_list,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['HT']=ta.HT_TRENDLINE(CloseArray)
    _df['MIDPOINT']=ta.MIDPOINT(CloseArray)
    _df['MIDPRICE']=ta.MIDPRICE(HighArray,LowArray)
    _df['SAR']=ta.SAR(HighArray,LowArray)
    _df['SAREXT']=ta.SAREXT(HighArray,LowArray)
    for period in period_list:
        periods =np.array([period]*len(_df), dtype=float)
        _df['MAVP_'+ str(period)]=ta.MAVP(CloseArray,periods)
        H_line,M_line,L_line=ta.BBANDS(CloseArray, timeperiod=period, nbdevup=2, nbdevdn=2, matype=0)
        _df['H_line_'+ str(period)]=H_line
        _df['M_line_'+ str(period)]=M_line
        _df['L_line_'+ str(period)]=L_line
    return _df

######
#价格转换型指标
######

#平均价格
#中位数价格
#代表性价格
#加权收盘价
def calculatePRICETransform(df,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['AVGPRICE']=ta.AVGPRICE(OpenArray,HighArray,LowArray,CloseArray)
    _df['MEDPRICE']=ta.MEDPRICE(HighArray,LowArray)
    _df['TYPPRICE']=ta.TYPPRICE(HighArray,LowArray,CloseArray)
    _df['WCLPRICE']=ta.WCLPRICE(HighArray,LowArray,CloseArray)
    return _df

######
#周期指标
######

#希尔伯特变换
#主导周期
#主导循环
#相位构成
#正弦波
#趋势与周期模式
def calculateCycle(df,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['dcperiod']=ta.HT_DCPERIOD(CloseArray)

    _df['dcphase']=ta.HT_DCPHASE(CloseArray)

    _df['inhpase'],_df['quadrature']=ta.HT_PHASOR(CloseArray)

    _df['sine'],_df['leadsine'] = ta.HT_SINE(CloseArray)

    _df['trendmode']=ta.HT_TRENDMODE(CloseArray)

    return _df

######
#波动率指标
######

#平均真实波动幅度
def calculateATR(df,period,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['ATR_'+ str(period)]=ta.ATR(HighArray,LowArray,CloseArray,period)
    return _df

#归一化的平均真实波动幅度
def calculateNATR(df,period,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['NATR_'+ str(period)]=ta.NATR(HighArray,LowArray,CloseArray,period)
    return _df

#真实波动幅度
def calculateTRANGE(df,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['TRANGE']=ta.TRANGE(HighArray,LowArray,CloseArray)
    return _df

def calculateallVolitility(df,period_list,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    for period in period_list:
        _df['ATR_'+ str(period)]=ta.ATR(HighArray,LowArray,CloseArray,period)
        _df['NATR_'+ str(period)]=ta.NATR(HighArray,LowArray,CloseArray,period)
        _df['TRANGE']=ta.TRANGE(HighArray,LowArray,CloseArray)
    return _df

######
#数学运算指标
######

#根据给定的周期列表计算所有的周期数学运算
def calculateMathOperator(df,period_list,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    df['add']=ta.ADD(HighArray,LowArray)
    #最高价与最低价之差
    _df['sub']=ta.SUB(HighArray,LowArray)
    #最高价与最低价之乘
    _df['mult']=ta.MULT(HighArray,LowArray)
    #最高价与最低价之除
    _df['div']=ta.DIV(HighArray,LowArray)
    for period in period_list:
        #收盘价的每30日移动求和

        df['sum_'+ str(period)]=ta.SUM(CloseArray,period)

        #收盘价的每30日内的最大最小值

        df['min_'+ str(period)], df['max_'+ str(period)] = ta.MINMAX(CloseArray, timeperiod=period)

        #收盘价的每30日内的最大最小值对应的索引值（第N行）

        df['minidx_'+ str(period)], df['maxidx_'+ str(period)] = ta.MINMAXINDEX(CloseArray, timeperiod=period)
    return _df

######
#统计学
######

#线性回归
def calculateLINEARREG(df,period,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['LINEARREG_'+ str(period)]=ta.LINEARREG(CloseArray,period)
    return _df

#线性回归斜率的正切角度
def calculateLINEARREG_ANGLE(df,period,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['LINEARREG_ANGLE_'+ str(period)]=ta.LINEARREG_ANGLE(CloseArray,period)
    return _df

#线性回归截距
def calculateLINEARREG_INTERCEPT(df,period,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['LINEARREG_INTERCEPT_'+ str(period)]=ta.LINEARREG_INTERCEPT(CloseArray,period)
    return _df

#线性回归斜率
def calculateLINEARREG_SLOPE(df,period,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['LINEARREG_SLOPE_'+ str(period)]=ta.LINEARREG_SLOPE(CloseArray,period)
    return _df

#标准差
def calculateSTDDEV(df,period,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['STDDEV_'+ str(period)]=ta.STDDEV(CloseArray,period)
    return _df

#时间序列预测
def calculateTSF(df,period,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['TSF_'+ str(period)]=ta.TSF(CloseArray,period)
    return _df

#方差
def calculateVAR(df,period,d = 0): #period 为天数参数
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['VAR_'+ str(period)]=ta.VAR(CloseArray,period)
    return _df

def calculate_allStatistic(df,period_list,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    for period in period_list:
        _df['LINEARREG_'+ str(period)]=ta.LINEARREG(CloseArray,period)
        _df['LINEARREG_ANGLE_'+ str(period)]=ta.LINEARREG_ANGLE(CloseArray,period)
        _df['LINEARREG_INTERCEPT_'+ str(period)]=ta.LINEARREG_INTERCEPT(CloseArray,period)
        _df['LINEARREG_SLOPE_'+ str(period)]=ta.LINEARREG_SLOPE(CloseArray,period)
        _df['STDDEV_'+ str(period)]=ta.STDDEV(CloseArray,period)
        _df['TSF_'+ str(period)]=ta.TSF(CloseArray,period)
        _df['VAR_'+ str(period)]=ta.VAR(CloseArray,period)
    return _df


######
#数学转换
######

def calculate_allMathtransform(df,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['SIN']=ta.SIN(CloseArray)
    _df['COS']=ta.COS(CloseArray)
    _df['TAN']=ta.TAN(CloseArray)
    _df['ASIN']=ta.ASIN(CloseArray)
    _df['ACOS']=ta.ACOS(CloseArray)
    _df['ATAN']=ta.ATAN(CloseArray)
    _df['SINH']=ta.SINH(CloseArray)
    _df['COSH']=ta.COSH(CloseArray)
    _df['CEIL']=ta.CEIL(CloseArray)
    _df['DIV']=ta.DIV(HighArray,LowArray)
    _df['FLOOR']=ta.FLOOR(CloseArray)
    _df['EXP']=ta.EXP(CloseArray)
    _df['LN']=ta.LN(CloseArray)
    _df['LOG10']=ta.LOG10(CloseArray)
    _df['SQRT']=ta.SQRT(CloseArray)
    return _df

######
#动量指标
######

#MACD
def calculateMACD(df, fastPeriod=12, slowPeriod=26, signalPeriod=9,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['MACD'],_df['MACDsignal'],_df['MACDhist']=ta.MACD(CloseArray , fastperiod=fastPeriod, slowperiod=slowPeriod, signalperiod=signalPeriod)
    return _df

#带可控MA类型的MACD
def calculateMACDEXT(df, fastPeriod=12, slowPeriod=26, signalPeriod=9,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['MACDEXT'],_df['MACDEXTsignal'],_df['MACDEXThist']=ta.MACDEXT(CloseArray , fastperiod=fastPeriod, slowperiod=slowPeriod, signalperiod=signalPeriod)
    return _df

#绝对价格振荡器
def calculateAPO(df, fastPeriod=12, slowPeriod=26,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['APO']=ta.APO(CloseArray , fastperiod=fastPeriod, slowperiod=slowPeriod)
    return _df

#钱德动量摆动指标
def calculateCMO(df, period,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['CMO_'+ str(period)]=ta.CMO(CloseArray , period)
    return _df

#动量
def calculateMOM(df, period,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['MOM_'+ str(period)]=ta.MOM(CloseArray , period)    
    return _df

#比例价格振荡器
def calculatePPO(df,fastPeriod=12, slowPeriod=26,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['PPO']=ta.PPO(CloseArray ,fastperiod=fastPeriod, slowperiod=slowPeriod)
    return _df

#变化率
def calculateROC(df, period,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['ROC_'+ str(period)]=ta.ROC(CloseArray , period)    
    return _df

#变化率百分比
def calculateROCP(df, period,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['ROCP_'+ str(period)]=ta.ROCP(CloseArray , period)      
    return _df

#变化率的比率
def calculateROCR(df, period,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['ROCR_'+ str(period)]=ta.ROCR(CloseArray , period)    
    return _df

#变化率的比率100倍
def calculateROCR100(df, period,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['ROCR100_'+ str(period)]=ta.ROCR100(CloseArray , period)    
    return _df

#相对强弱指标
def calculateRSI(df, period,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['RSI_'+ str(period)]=ta.RSI(CloseArray , period)    
    return _df

#三重光滑EMA的日变化率
def calculateTRIX(df, period,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['TRIX_'+ str(period)]=ta.TRIX(CloseArray , period)    
    return _df

#随机相对强弱指标
def calculateSTOCHRSI(df, period,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    _df['STOCHRSI_fastk_'+ str(period)],_df['STOCHRSI_fastd_'+ str(period)]=ta.STOCHRSI(CloseArray , period)    
    return _df

def calculate_allMOM(df,period_list,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    for period in period_list:
        _df['CMO_'+ str(period)]=ta.CMO(CloseArray , period)
        _df['MOM_'+ str(period)]=ta.MOM(CloseArray , period)  
        _df['ROC_'+ str(period)]=ta.ROC(CloseArray , period)
        _df['ROCP_'+ str(period)]=ta.ROCP(CloseArray , period) 
        _df['ROCR_'+ str(period)]=ta.ROCR(CloseArray , period)
        _df['ROCR100_'+ str(period)]=ta.ROCR100(CloseArray , period) 
        _df['RSI_'+ str(period)]=ta.RSI(CloseArray , period)  
        _df['TRIX_'+ str(period)]=ta.TRIX(CloseArray , period) 
        _df['STOCHRSI_fastk_'+ str(period)],_df['STOCHRSI_fastd_'+ str(period)]=ta.STOCHRSI(CloseArray , period)
    _df = calculateMACD(_df)
    _df = calculateMACDEXT(_df)
    _df = calculateAPO(_df)
    _df = calculatePPO(_df)
    return _df

######
#交易量指标
######

def calculateAllvolume(df,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    VolArray = np.array([float(x) for x in df['vol'].values])
    #print(VolArray)
    _df['AD'] = ta.AD(HighArray,LowArray,CloseArray,VolArray)
    _df['ADOSC'] = ta.ADOSC(HighArray,LowArray,CloseArray,VolArray)
    _df['OBV'] = ta.OBV(CloseArray,VolArray)
    return _df

######
#形态识别
######

def calculateAllPattern_Recog(df,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = diff.data_frame_diff(df,d)
    CloseArray = np.array(df['close'])
    HighArray = np.array(df['high'])
    LowArray = np.array(df['low'])
    OpenArray = np.array(df['open'])
    VolArray = np.array(df['vol'])
    _df['CDL2CROWS'] = ta.CDL2CROWS(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDL3INSIDE'] = ta.CDL3INSIDE(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDL3LINESTRIKE'] = ta.CDL3LINESTRIKE(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDL3OUTSIDE'] = ta.CDL3OUTSIDE(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDL3STARSINSOUTH'] = ta.CDL3STARSINSOUTH(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDL3WHITESOLDIERS'] = ta.CDL3WHITESOLDIERS(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLABANDONEDBABY'] = ta.CDLABANDONEDBABY(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLADVANCEBLOCK'] = ta.CDLADVANCEBLOCK(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLBELTHOLD'] = ta.CDLBELTHOLD(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLBREAKAWAY'] = ta.CDLBREAKAWAY(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLCLOSINGMARUBOZU'] = ta.CDLCLOSINGMARUBOZU(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLCONCEALBABYSWALL'] = ta.CDLCONCEALBABYSWALL(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLCOUNTERATTACK'] = ta.CDLCOUNTERATTACK(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLDARKCLOUDCOVER'] = ta.CDLDARKCLOUDCOVER(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLDOJISTAR'] = ta.CDLDOJISTAR(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLDRAGONFLYDOJI'] = ta.CDLDRAGONFLYDOJI(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLENGULFING'] = ta.CDLENGULFING(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLEVENINGDOJISTAR'] = ta.CDLEVENINGDOJISTAR(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLEVENINGSTAR'] = ta.CDLEVENINGSTAR(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLGAPSIDESIDEWHITE'] = ta.CDLGAPSIDESIDEWHITE(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLGRAVESTONEDOJI'] = ta.CDLGRAVESTONEDOJI(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLHAMMER'] = ta.CDLHAMMER(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLHANGINGMAN'] = ta.CDLHANGINGMAN(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLHARAMI'] = ta.CDLHARAMI(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLHARAMICROSS'] = ta.CDLHARAMICROSS(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLHIKKAKE'] = ta.CDLHIKKAKE(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLHIKKAKEMOD'] = ta.CDLHIKKAKEMOD(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLHOMINGPIGEON'] = ta.CDLHOMINGPIGEON(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLIDENTICAL3CROWS'] = ta.CDLIDENTICAL3CROWS(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLINNECK'] = ta.CDLINNECK(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLINVERTEDHAMMER'] = ta.CDLINVERTEDHAMMER(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLKICKING'] = ta.CDLKICKING(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLKICKINGBYLENGTH'] = ta.CDLKICKINGBYLENGTH(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLLADDERBOTTOM'] = ta.CDLLADDERBOTTOM(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLLONGLEGGEDDOJI'] = ta.CDLLONGLEGGEDDOJI(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLLONGLINE'] = ta.CDLLONGLINE(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLMARUBOZU'] = ta.CDLMARUBOZU(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLMATCHINGLOW'] = ta.CDLMATCHINGLOW(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLMATHOLD'] = ta.CDLMATHOLD(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLMORNINGDOJISTAR'] = ta.CDLMORNINGDOJISTAR(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLMORNINGSTAR'] = ta.CDLMORNINGSTAR(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLONNECK'] = ta.CDLONNECK(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLPIERCING'] = ta.CDLPIERCING(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLRICKSHAWMAN'] = ta.CDLRICKSHAWMAN(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLRISEFALL3METHODS'] = ta.CDLRISEFALL3METHODS(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLSEPARATINGLINES'] = ta.CDLSEPARATINGLINES(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLSHOOTINGSTAR'] = ta.CDLSHOOTINGSTAR(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLSHORTLINE'] = ta.CDLSHORTLINE(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLSPINNINGTOP'] = ta.CDLSPINNINGTOP(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLSTALLEDPATTERN'] = ta.CDLSTALLEDPATTERN(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLSTICKSANDWICHR'] = ta.CDLSTICKSANDWICH(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLTAKURI'] = ta.CDLTAKURI(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLTASUKIGAP'] = ta.CDLTASUKIGAP(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLTHRUSTING'] = ta.CDLTHRUSTING(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLTRISTAR'] = ta.CDLTRISTAR(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLUNIQUE3RIVER'] = ta.CDLUNIQUE3RIVER(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLUPSIDEGAP2CROWS'] = ta.CDLUPSIDEGAP2CROWS(OpenArray,HighArray,LowArray,CloseArray)
    _df['CDLXSIDEGAP3METHODS'] = ta.CDLXSIDEGAP3METHODS(OpenArray,HighArray,LowArray,CloseArray)
    
    return _df

def calculateAll_tbindex(df):
    name = 'close'
    period_list = [2,5,7,12,14,26,30,40,60]
    df = calculate_allMA(df,name,period_list)
    df = calculateOverlap_others(df,period_list)
    df = calculatePRICETransform(df)
    df = calculateCycle(df)
    df = calculateMathOperator(df,period_list)
    df = calculateallVolitility(df,period_list)
    df = calculate_allStatistic(df,period_list)
    df = calculate_allMathtransform(df)
    df = calculate_allMOM(df,period_list)
    df = calculateAllvolume(df)
    df = calculateAllPattern_Recog(df)
    return df