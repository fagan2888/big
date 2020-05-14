import sys,os
from collections import defaultdict
import tushare as ts
import pandas as pd

def get_code_list():
    code_list = ts.get_hs300s()['code']
    for i in range(len(code_list)):
        if(str(code_list[i])[0]=='6'):
            code_list[i] = str(code_list[i]) + '.XSHG'
        else:
            code_list[i] = str(code_list[i]) + '.XSHE'
    return code_list.tolist()

def get_all_code_list():
    all_code_list = pd.read_excel(now_file+'/all_code.xlsx',index_col = 0).values
    return [x[0] for x in all_code_list.tolist()]

def get_st_code():
    st = pd.read_excel('/Users/wode/Desktop/学校/系统方案备份/sig_inter.xlsx',index_col = 0)
    return st[st['5day_fre']>0.5].index.tolist()

now_file = os.path.abspath(os.path.dirname(__file__))
up_file = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(up_file)


PARAMS = defaultdict(
begin_date = 20150101,#信号计算开始日期
code_list = ['600000.XSHG','002422.XSHE'],
#code_list = get_all_code_list(),#
#code_list = get_code_list(),#信号计算的股票池
get_code_data = False,#True,#是否重新获得原始数据
#get_code_data = False,#是否重新获得原始数据
HS_code = '999999.XSHG',#'399300.XSHE',#信号中的大盘信号代码
signal_lf = [1,1,1,1,1], #分别对应下面五种信号的生命周期,阈值，交叉，趋势，比较，计数
_signal_save_path = up_file+'/result/mul/', #信号结果储存地址
# 信号的表达式，第一个为做多买入信号，第二个为做多卖出信号
# 信号的构建方法为 
# 阈值型信号 指标名+#+阈值+#+方向(1为大于,0为小于)+&thre,如果为大盘信号，则在最后加上&HS
# 交叉型信号 指标1名+#+指标2名+#+方向(1为金叉,0为死叉)+&cross,如果为大盘信号，则在最后加上&HS
# 趋势型信号 指标1名+#+趋势延续天数+#+方向(1为上涨,0为下跌)+&trend,如果为大盘信号，则在最后加上&HS
# 比较型信号 指标1名+#+指标2名+#+方向(1为指标1大于指标2,0为指标1小于指标2)+&diff,如果为大盘信号，则在最后加上&HS
# 计数型信号 其他信号+&+时间对标信号+&次数+&其他信号类型&+时间对标信号类型+&+times 注意 
# 比如 high#close_EMA_20#1&close_EMA_20#close_EMA_50#0&1&cross&cross&times 在写其他信号和时间对标信号时不写类型
# 如果不想要时间对标信号，可以写一个永远不会成立的时间对标信号，比如low#high#1&diff,这样
# 计数型信号就会计算100天内其他信号发生的次数
# 信号组合可以使用+和*进行或和且逻辑运算,指标名称可在index_24中查询
#_Expression = ['close_MA_5#close_MA_30#1&cross','close_MA_5#1#0&trend'],
#_Expression = ['close_MA_5#close_MA_20#1&cross','close_MA_5#close_MA_10#0&cross'],  
#_Expression = ['close_EMA_7#close_EMA_15#1&diff*close_EMA_15#close_EMA_25#1&diff*close_EMA_15#2#1&trend*close_EMA_25#2#1&trend*MACD#0#1&thre*close#close_shift_4#1&diff*K#40#1&thre&HS',
                #'MACD#0#0&thre+K#40#0&thre&HS'],#+close#close_MA_10#0&cross'],
#_Expression = ['close_EMA_7#close_EMA_15#1&diff*close_EMA_15#close_EMA_25#1&diff*close#2#0&trend&HS*MACD#3#1&trend*MB#3#1&trend*K#40#1&thre&HS', 'close_EMA_7#close_EMA_15#0&diff*close#2#1&trend&HS*MACD#3#0&trend*MB#3#0&trend*K#40#0&thre&HS'],
#_Expression = ['close_EMA_25#2#1&trend*MACD#0#1&thre+close_EMA_25#2#1&trend*K#40#0&thre&HS',
 #'MACD#0#0&thre*K#40#0&thre&HS*MACD#0#0&thre+MACD#0#0&thre*K#40#0&thre&HS*close_EMA_25#2#1&trend+MACD#0#0&thre*K#40#0&thre&HS*K#40#0&thre&HS'],
#_Expression = ['close#2#0&trend&HS*MACD#2#1&trend*MB#2#1&trend','close#2#1&trend&HS*MACD#2#0&trend*MB#2#0&trend'],
#_Expression = ['close_EMA_12#close_EMA_26#1&cross*RSI_6#RSI_12#1&cross*J#D#1&cross','close_EMA_12#close_EMA_26#1&cross+RSI_6#RSI_12#1&cross+J#D#1&cross'],
#=['close_EMA_20#close_EMA_50#1&diff*close_EMA_20#close_EMA_50#1&cross*high#close_EMA_20#0&close_EMA_20#close_EMA_50#1&3&cross&cross&times+close_EMA_20#close_EMA_50#1&diff*close_EMA_20#close_EMA_50#1&cross*low#close_EMA_50#1&close_EMA_20#close_EMA_50#1&3&cross&cross&times',
                #'close_EMA_20#close_EMA_50#0&diff*close_EMA_20#close_EMA_50#0&cross*high#close_EMA_20#1&close_EMA_20#close_EMA_50#0&1&cross&cross&times'],
_Expression = ['K#90#1&HS&thre*close_MA_10#open#1&diff*close#close_MA_10_shift_1#1&diff+K#90#1&HS&thre*close_MA_10#open#1&diff*close_shift_1#close_MA_10_shift_1#1&diff+K#90#1&HS&thre*close_MA_10#open#1&diff*RSI_12#80#1&thre*RSI_12#100#0&thre+K#90#1&HS&thre*K#90#1&thre*close#close_MA_10_shift_1#1&diff+K#90#1&HS&thre*K#90#1&thre*close_shift_1#close_MA_10_shift_1#1&diff+K#90#1&HS&thre*K#90#1&thre*RSI_12#80#1&thre*RSI_12#100#0&thre+K_shift_1#10#0&HS&thre*close_MA_10#open#1&diff*close#close_MA_10_shift_1#1&diff+K_shift_1#10#0&HS&thre*close_MA_10#open#1&diff*close_shift_1#close_MA_10_shift_1#1&diff+K_shift_1#10#0&HS&thre*close_MA_10#open#1&diff*RSI_12#80#1&thre*RSI_12#100#0&thre+K_shift_1#10#0&HS&thre*K#90#1&thre*close#close_MA_10_shift_1#1&diff+K_shift_1#10#0&HS&thre*K#90#1&thre*close_shift_1#close_MA_10_shift_1#1&diff+K_shift_1#10#0&HS&thre*K#90#1&thre*RSI_12#80#1&thre*RSI_12#100#0&thre+D_shift_1#20#0&HS&thre*close_MA_10#open#1&diff*close#close_MA_10_shift_1#1&diff+D_shift_1#20#0&HS&thre*close_MA_10#open#1&diff*close_shift_1#close_MA_10_shift_1#1&diff+D_shift_1#20#0&HS&thre*close_MA_10#open#1&diff*RSI_12#80#1&thre*RSI_12#100#0&thre+D_shift_1#20#0&HS&thre*K#90#1&thre*close#close_MA_10_shift_1#1&diff+D_shift_1#20#0&HS&thre*K#90#1&thre*close_shift_1#close_MA_10_shift_1#1&diff+D_shift_1#20#0&HS&thre*K#90#1&thre*RSI_12#80#1&thre*RSI_12#100#0&thre', 'close_MA_10_shift_1#close_MA_10#1&HS&diff*open#close#1&diff*D#60#1&thre+close_MA_10_shift_1#close_MA_10#1&HS&diff*open#close#1&diff*D_shift_1#60#1&thre+close_MA_10_shift_1#close_MA_10#1&HS&diff*open#close#1&diff*RSI_12#0#1&thre*RSI_12#20#0&thre+close_MA_10_shift_1#close_MA_10#1&HS&diff*K_shift_1#90#1&thre*D#60#1&thre+close_MA_10_shift_1#close_MA_10#1&HS&diff*K_shift_1#90#1&thre*D_shift_1#60#1&thre+close_MA_10_shift_1#close_MA_10#1&HS&diff*K_shift_1#90#1&thre*RSI_12#0#1&thre*RSI_12#20#0&thre+close_MA_10_shift_1#close_MA_10#1&HS&diff*D_shift_1#10#0&thre*D#60#1&thre+close_MA_10_shift_1#close_MA_10#1&HS&diff*D_shift_1#10#0&thre*D_shift_1#60#1&thre+close_MA_10_shift_1#close_MA_10#1&HS&diff*D_shift_1#10#0&thre*RSI_12#0#1&thre*RSI_12#20#0&thre+DEA_shift_1#DEA#1&HS&diff*open#close#1&diff*D#60#1&thre+DEA_shift_1#DEA#1&HS&diff*open#close#1&diff*D_shift_1#60#1&thre+DEA_shift_1#DEA#1&HS&diff*open#close#1&diff*RSI_12#0#1&thre*RSI_12#20#0&thre+DEA_shift_1#DEA#1&HS&diff*K_shift_1#90#1&thre*D#60#1&thre+DEA_shift_1#DEA#1&HS&diff*K_shift_1#90#1&thre*D_shift_1#60#1&thre+DEA_shift_1#DEA#1&HS&diff*K_shift_1#90#1&thre*RSI_12#0#1&thre*RSI_12#20#0&thre+DEA_shift_1#DEA#1&HS&diff*D_shift_1#10#0&thre*D#60#1&thre+DEA_shift_1#DEA#1&HS&diff*D_shift_1#10#0&thre*D_shift_1#60#1&thre+DEA_shift_1#DEA#1&HS&diff*D_shift_1#10#0&thre*RSI_12#0#1&thre*RSI_12#20#0&thre+D_shift_1#20#0&HS&thre*open#close#1&diff*D#60#1&thre+D_shift_1#20#0&HS&thre*open#close#1&diff*D_shift_1#60#1&thre+D_shift_1#20#0&HS&thre*open#close#1&diff*RSI_12#0#1&thre*RSI_12#20#0&thre+D_shift_1#20#0&HS&thre*K_shift_1#90#1&thre*D#60#1&thre+D_shift_1#20#0&HS&thre*K_shift_1#90#1&thre*D_shift_1#60#1&thre+D_shift_1#20#0&HS&thre*K_shift_1#90#1&thre*RSI_12#0#1&thre*RSI_12#20#0&thre+D_shift_1#20#0&HS&thre*D_shift_1#10#0&thre*D#60#1&thre+D_shift_1#20#0&HS&thre*D_shift_1#10#0&thre*D_shift_1#60#1&thre+D_shift_1#20#0&HS&thre*D_shift_1#10#0&thre*RSI_12#0#1&thre*RSI_12#20#0&thre'],
#_Expression = ['K#90#1&HS&thre*CCI#-100#0&thre*close#open#1&diff+K_shift_1#10#0&HS&thre*CCI#-100#0&thre*close#open#1&diff+D#90#1&HS&thre*CCI#-100#0&thre*close#open#1&diff', 'MACD_shift_1#0#0&HS&thre*open#close#1&diff*K#10#0&thre+MACD_shift_1#0#0&HS&thre*open#close#1&diff*K_shift_1#90#1&thre+MACD_shift_1#0#0&HS&thre*open#close#1&diff*RSI_12_shift_1#RSI_12#1&diff+MACD_shift_1#0#0&HS&thre*K_shift_1#90#1&thre*K#10#0&thre+MACD_shift_1#0#0&HS&thre*K_shift_1#90#1&thre*K_shift_1#90#1&thre+MACD_shift_1#0#0&HS&thre*K_shift_1#90#1&thre*RSI_12_shift_1#RSI_12#1&diff+D_shift_1#20#0&HS&thre*open#close#1&diff*K#10#0&thre+D_shift_1#20#0&HS&thre*open#close#1&diff*K_shift_1#90#1&thre+D_shift_1#20#0&HS&thre*open#close#1&diff*RSI_12_shift_1#RSI_12#1&diff+D_shift_1#20#0&HS&thre*K_shift_1#90#1&thre*K#10#0&thre+D_shift_1#20#0&HS&thre*K_shift_1#90#1&thre*K_shift_1#90#1&thre+D_shift_1#20#0&HS&thre*K_shift_1#90#1&thre*RSI_12_shift_1#RSI_12#1&diff+D_shift_1#30#0&HS&thre*open#close#1&diff*K#10#0&thre+D_shift_1#30#0&HS&thre*open#close#1&diff*K_shift_1#90#1&thre+D_shift_1#30#0&HS&thre*open#close#1&diff*RSI_12_shift_1#RSI_12#1&diff+D_shift_1#30#0&HS&thre*K_shift_1#90#1&thre*K#10#0&thre+D_shift_1#30#0&HS&thre*K_shift_1#90#1&thre*K_shift_1#90#1&thre+D_shift_1#30#0&HS&thre*K_shift_1#90#1&thre*RSI_12_shift_1#RSI_12#1&diff'],
# 回测参数，目前设定是第二天开盘买入，当天收盘卖出，每次以资金的三分之一操作，默认
# 是下跌1%时候止损卖出
# 可以在strategy.py中更改
# 更多参数设置可以百度搜索rqalpha
_optimal = True,
_config = {
    "base":
    {
          "benchmark": "399300.XSHE", #基准
          "margin_multiplier": 1.4, #
          "start_date": "2015-01-03", #回测开始日期
          "end_date":   "2019-12-27", #回测结束日期
          "frequency": "1d", #回测频率
          "accounts":{
            "stock":  100000000, #回测本金
            #"future": "~",
          }
    },
    "extra":{
        #"log_level": "warning",
        "log_level": "error",
    },
    "mod":{
      "sys_analyser":{
        "enabled":             True,
        "report":              True,
        #"plot":                True,
        "plot":                False
      },
      "sys_simulation":{
        "enabled":               True,
        "signal":                True,
        "slippage":              0.0005, #滑点
        #"slippage":              0.0,
        "matching_type":         "current_bar",
        "price_limit":           False,
        "volume_limit":          False,
        "commission-multiplier": 0,
      },
    },
}
)