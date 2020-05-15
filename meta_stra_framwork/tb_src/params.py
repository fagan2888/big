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

def get_st_code():
    st = pd.read_excel('/Users/wode/Desktop/学校/系统方案备份/sig_inter.xlsx',index_col = 0)
    return st[st['5day_fre']>0.5].index.tolist()

now_file = os.path.abspath(os.path.dirname(__file__))
up_file = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(up_file)


PARAMS = defaultdict(
begin_date = 20150101,#信号计算开始日期
#code_list = ['600000.XSHG','002422.XSHE'],
#code_list = get_st_code(),#
code_list = get_code_list(),#信号计算的股票池
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
#=['close_EMA_20#close_EMA_50#1&diff*close_EMA_20#close_EMA_50#1&cross*high#close_EMA_20#0&close_EMA_20#close_EMA_50#1&3&cross&cross&times+close_EMA_20#close_EMA_50#1&diff*close_EMA_20#close_EMA_50#1&cross*low#close_EMA_50#1&close_EMA_20#close_EMA_50#1&3&cross&cross&times',
                #'close_EMA_20#close_EMA_50#0&diff*close_EMA_20#close_EMA_50#0&cross*high#close_EMA_20#1&close_EMA_20#close_EMA_50#0&1&cross&cross&times'],
#_Expression = ['SAR#3#0&trend+ROC_14#-10#0&thre+STOCHRSI_fastd_7#STOCHRSI_fastk_12#0&diff+SIN#DIV#0&diff&HS+NATR_5#3#1&trend+LINEARREG_ANGLE_40#2#0&trend+NATR_14#3#0&thre&HS+ATR_60#1#1&thre&HS+ATR_14#0#0&thre&HS+close_TRIMA_30#42#0&thre+CDLEVENINGDOJISTAR#0#0&thre&HS+close_MAMA#close_EMA_2#1&diff&HS+RSI_30#ROCR100_40#0&cross+CEIL#3#0&trend+OBV#4571203#1&thre&HS+CDLLONGLINE#3#0&trend&HS+CDLMATCHINGLOW#1#0&thre&HS+VAR_30#1#1&thre+SINH#2#0&trend+TSF_7#LINEARREG_14#0&cross&HS+CMO_12#33#0&thre+LINEARREG_12#43#1&thre+L_line_26#3#1&trend+TRIX_26#3#1&trend+CDLPIERCING#0#0&thre+ROCP_26#0#0&thre&HS+L_line_60#28#0&thre+close_TRIMA_40#close_KAMA_60#0&cross+ROCR_14#1#0&thre&HS+STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&diff+RSI_60#60#1&thre&HS+CDLHIKKAKEMOD#3#1&trend&HS+STDDEV_14#1#1&trend&HS+close_TEMA_30#close_TRIMA_40#0&cross&HS+CDLBREAKAWAY#2#0&trend+TRANGE#ATR_26#0&cross+L_line_30#AVGPRICE#1&diff&HS+CDLGAPSIDESIDEWHITE#2#0&trend&HS+TSF_5#32#1&thre+TYPPRICE#1#1&trend+ATAN#2#1&trend&HS+CDLDOJISTAR#1#0&trend&HS+RSI_14#65#0&thre+MOM_40#3#0&trend&HS+STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross+close_KAMA_2#2#0&trend&HS+MAVP_40#42#1&thre&HS+CDLRISEFALL3METHODS#1#1&trend&HS+L_line_26#2#1&trend&HS+close_DEMA_14#close_TEMA_26#0&cross+NATR_12#5#0&thre&HS+CMO_60#-24#1&thre+COS#FLOOR#1&cross+LINEARREG_26#3#1&trend+STOCHRSI_fastk_5#25#1&thre&HS+MOM_14#1#1&trend+CDLMATCHINGLOW#1#1&trend+CMO_30#3#1&trend&HS+close_WMA_14#close_DEMA_26#0&cross&HS+LINEARREG_ANGLE_2#39#0&thre+ROCR100_2#1#0&trend+CDLRICKSHAWMAN#3#1&trend+CMO_14#STOCHRSI_fastd_14#0&cross+STOCHRSI_fastd_30#75#1&thre&HS+CEIL#26#1&thre+ACOS#1#0&trend&HS+MOM_40#8#1&thre&HS+TRIX_2#3#1&trend&HS+RSI_5#ROCR100_7#1&diff+close_EMA_7#close_MA_14#0&diff+M_line_7#L_line_14#0&diff&HS+MOM_12#CMO_14#1&diff+close_KAMA_7#1#1&trend&HS+TRIX_30#0#0&thre&HS+CDLABANDONEDBABY#1#1&trend+ROC_60#35#0&thre+CDLLADDERBOTTOM#1#0&trend+ROCR100_40#1#1&trend&HS+close_EMA_2#close_MA_7#0&cross+VAR_60#3#1&trend+close_MA_40#32#1&thre+RSI_5#ROCR100_7#1&cross+NATR_7#ATR_40#1&cross&HS+close_DEMA_12#close_TEMA_14#0&cross&HS+LINEARREG_SLOPE_14#3#1&trend+CDLSHOOTINGSTAR#3#1&trend+close_TEMA_60#MAVP_2#0&cross&HS+VAR_2#LINEARREG_ANGLE_7#0&cross&HS+CDLCONCEALBABYSWALL#0#0&thre+STDDEV_12#VAR_14#1&cross+TSF_2#25#1&thre+TRIX_40#3#0&trend&HS+VAR_12#1#1&trend+LINEARREG_26#LINEARREG_INTERCEPT_30#1&cross+ATR_7#1#0&trend&HS+close_TRIMA_14#43#0&thre&HS+RSI_30#1#1&trend+LINEARREG_14#1#0&trend+quadrature#-8#0&thre&HS+close_TEMA_14#32#0&thre&HS+ATR_26#2#0&thre&HS+VAR_26#3#0&trend&HS+L_line_26#MAVP_60#1&diff&HS+CDLLONGLINE#2#0&trend&HS+TRIX_30#0#1&thre&HS+TRIX_12#0#1&thre&HS+TRIX_60#APO#0&diff&HS+ROCR100_14#1#1&trend&HS+NATR_30#STDDEV_2#1&cross+close_TEMA_5#3#1&trend&HS+STOCHRSI_fastd_60#51#1&thre+CDLLONGLINE#49#1&thre&HS+H_line_12#1#0&trend&HS+ROC_60#1#1&trend+ROC_14#18#0&thre&HS+STOCHRSI_fastk_5#2#0&trend+NATR_12#5#1&thre&HS+ROCR100_12#ROCR_14#1&cross&HS+H_line_7#1#1&trend&HS+VAR_60#1#0&trend&HS+close_TRIMA_60#2#1&trend&HS+CMO_2#STOCHRSI_fastd_2#1&cross+MOM_40#CMO_60#0&diff+CDLCLOSINGMARUBOZU#-2#1&thre&HS+close_MA_7#2#1&trend&HS+L_line_5#2#0&trend+MACD#1#0&thre&HS+CDLMORNINGSTAR#1#0&trend+L_line_2#2#1&trend&HS+STOCHRSI_fastk_26#TRIX_30#1&diff+LINEARREG_SLOPE_12#TSF_14#0&cross+RSI_12#1#0&trend&HS+close_WMA_5#3#1&trend+ROCR100_2#2#1&trend+LINEARREG_7#1#0&trend+CDLGAPSIDESIDEWHITE#1#1&trend+close_MA_60#32#1&thre&HS+STDDEV_26#2#0&thre&HS+MAVP_26#26#1&thre&HS+CDLKICKING#1#0&trend+FLOOR#25#1&thre&HS+close_KAMA_30#1#1&trend+LINEARREG_INTERCEPT_60#1#0&trend&HS+LINEARREG_INTERCEPT_26#3#0&trend+LINEARREG_INTERCEPT_60#ACOS#0&cross+ROCR100_30#99#0&thre+close_DEMA_60#3#0&trend+ROCR100_60#3#0&trend&HS+NATR_12#2#1&trend+CDLSHOOTINGSTAR#2#1&trend&HS+LINEARREG_30#1#0&trend&HS+close_WMA_7#26#1&thre+CDLINVERTEDHAMMER#1#0&thre&HS+VAR_14#1#1&thre+CDLABANDONEDBABY#0#1&thre+M_line_2#L_line_7#0&diff+MAVP_2#3#1&trend+MACD#3#1&trend+H_line_30#35#1&thre&HS+CEIL#47#1&thre+ROCR_5#0#0&thre&HS+CDLSHOOTINGSTAR#2#1&trend+PPO#3#0&trend&HS+ATR_7#NATR_30#0&cross&HS+close_KAMA_2#2#1&trend&HS+STDDEV_5#0#0&thre+H_line_5#3#0&trend&HS+close_EMA_12#26#1&thre&HS+L_line_14#24#1&thre&HS+ROC_40#-16#1&thre+close_DEMA_2#46#0&thre+ADOSC#2#1&trend&HS+STDDEV_14#3#0&trend&HS+CMO_7#2#0&trend&HS+ROCR_40#ROCP_60#1&cross+ROCR100_30#ROCR_40#1&diff&HS+STOCHRSI_fastd_5#50#1&thre+ROCR100_5#89#1&thre+close_KAMA_7#1#1&trend+NATR_40#3#1&thre&HS+ATR_60#LINEARREG_5#1&diff+close_SMA_40#2#1&trend+STOCHRSI_fastk_7#TRIX_12#0&diff+RSI_26#ROCR100_30#0&cross&HS+APO#1#1&thre+CDLONNECK#3#0&trend&HS+CDLHIKKAKEMOD#2#0&trend+TRANGE#1#0&thre&HS+close_WMA_5#32#1&thre+COS#1#0&trend&HS+EXP#2#0&trend&HS+TAN#-296#0&thre+CDLHANGINGMAN#0#1&thre+close_EMA_14#26#1&thre&HS+inhpase#NATR_2#0&cross&HS+CDLKICKINGBYLENGTH#1#0&trend+RSI_12#28#1&thre+close_DEMA_14#32#1&thre&HS+close_EMA_26#32#1&thre&HS+LINEARREG_SLOPE_5#TSF_7#1&diff','close_EMA_26#32#1&thre&HS'],
#_Expression = ['ROCR100_30#99#0&thre*L_line_30#AVGPRICE#1&diff&HS*ROCP_26#0#0&thre&HS+ROCR100_30#99#0&thre*L_line_30#AVGPRICE#1&diff&HS*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross+ROCR100_30#99#0&thre*L_line_30#AVGPRICE#1&diff&HS*CMO_14#STOCHRSI_fastd_14#0&cross+ROCR100_30#99#0&thre*close_TRIMA_60#2#1&trend&HS*ROCP_26#0#0&thre&HS+ROCR100_30#99#0&thre*close_TRIMA_60#2#1&trend&HS*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross+ROCR100_30#99#0&thre*close_TRIMA_60#2#1&trend&HS*CMO_14#STOCHRSI_fastd_14#0&cross+ROCR100_30#99#0&thre*CDLSHOOTINGSTAR#2#1&trend&HS*ROCP_26#0#0&thre&HS+ROCR100_30#99#0&thre*CDLSHOOTINGSTAR#2#1&trend&HS*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross+ROCR100_30#99#0&thre*CDLSHOOTINGSTAR#2#1&trend&HS*CMO_14#STOCHRSI_fastd_14#0&cross','CDLMORNINGSTAR#1#0&trend*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross*MOM_40#CMO_60#0&diff+CDLMORNINGSTAR#1#0&trend*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross*L_line_26#2#1&trend&HS+CDLMORNINGSTAR#1#0&trend*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross*STDDEV_14#1#1&trend&HS+CDLMORNINGSTAR#1#0&trend*VAR_26#3#0&trend&HS*MOM_40#CMO_60#0&diff+CDLMORNINGSTAR#1#0&trend*VAR_26#3#0&trend&HS*L_line_26#2#1&trend&HS+CDLMORNINGSTAR#1#0&trend*VAR_26#3#0&trend&HS*STDDEV_14#1#1&trend&HS+CDLMORNINGSTAR#1#0&trend*ROC_14#-10#0&thre*MOM_40#CMO_60#0&diff+CDLMORNINGSTAR#1#0&trend*ROC_14#-10#0&thre*L_line_26#2#1&trend&HS+CDLMORNINGSTAR#1#0&trend*ROC_14#-10#0&thre*STDDEV_14#1#1&trend&HS'],
#_Expression = ['ROCR100_30#99#0&thre*L_line_30#AVGPRICE#1&diff&HS*CEIL#26#1&thre+ROCR100_30#99#0&thre*L_line_30#AVGPRICE#1&diff&HS*MOM_40#CMO_60#0&diff+ROCR100_30#99#0&thre*L_line_30#AVGPRICE#1&diff&HS*COS#FLOOR#1&cross+ROCR100_30#99#0&thre*TRANGE#ATR_26#0&cross*CEIL#26#1&thre+ROCR100_30#99#0&thre*TRANGE#ATR_26#0&cross*MOM_40#CMO_60#0&diff+ROCR100_30#99#0&thre*TRANGE#ATR_26#0&cross*COS#FLOOR#1&cross+ROCR100_30#99#0&thre*MOM_14#1#1&trend*CEIL#26#1&thre+ROCR100_30#99#0&thre*MOM_14#1#1&trend*MOM_40#CMO_60#0&diff+ROCR100_30#99#0&thre*MOM_14#1#1&trend*COS#FLOOR#1&cross','CDLMORNINGSTAR#1#0&trend*VAR_26#3#0&trend&HS*STDDEV_14#1#1&trend&HS+CDLMORNINGSTAR#1#0&trend*VAR_26#3#0&trend&HS*CDLLONGLINE#2#0&trend&HS+CDLMORNINGSTAR#1#0&trend*VAR_26#3#0&trend&HS*ROC_14#-10#0&thre+CDLMORNINGSTAR#1#0&trend*STDDEV_26#2#0&thre&HS*STDDEV_14#1#1&trend&HS+CDLMORNINGSTAR#1#0&trend*STDDEV_26#2#0&thre&HS*CDLLONGLINE#2#0&trend&HS+CDLMORNINGSTAR#1#0&trend*STDDEV_26#2#0&thre&HS*ROC_14#-10#0&thre+CDLMORNINGSTAR#1#0&trend*ROC_14#-10#0&thre*STDDEV_14#1#1&trend&HS+CDLMORNINGSTAR#1#0&trend*ROC_14#-10#0&thre*CDLLONGLINE#2#0&trend&HS+CDLMORNINGSTAR#1#0&trend*ROC_14#-10#0&thre*ROC_14#-10#0&thre'],
_Expression = ['L_line_5#2#0&trend*TAN#-296#0&thre*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross*CDLABANDONEDBABY#0#1&thre+L_line_5#2#0&trend*TAN#-296#0&thre*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross*close_DEMA_60#3#0&trend+L_line_5#2#0&trend*TAN#-296#0&thre*close_TRIMA_60#2#1&trend&HS*CDLABANDONEDBABY#0#1&thre+L_line_5#2#0&trend*TAN#-296#0&thre*close_TRIMA_60#2#1&trend&HS*close_DEMA_60#3#0&trend+L_line_5#2#0&trend*TAN#-296#0&thre*COS#FLOOR#1&cross*CDLABANDONEDBABY#0#1&thre+L_line_5#2#0&trend*TAN#-296#0&thre*COS#FLOOR#1&cross*close_DEMA_60#3#0&trend+L_line_5#2#0&trend*L_line_30#AVGPRICE#1&diff&HS*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross*CDLABANDONEDBABY#0#1&thre+L_line_5#2#0&trend*L_line_30#AVGPRICE#1&diff&HS*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross*close_DEMA_60#3#0&trend+L_line_5#2#0&trend*L_line_30#AVGPRICE#1&diff&HS*close_TRIMA_60#2#1&trend&HS*CDLABANDONEDBABY#0#1&thre+L_line_5#2#0&trend*L_line_30#AVGPRICE#1&diff&HS*close_TRIMA_60#2#1&trend&HS*close_DEMA_60#3#0&trend+L_line_5#2#0&trend*L_line_30#AVGPRICE#1&diff&HS*COS#FLOOR#1&cross*CDLABANDONEDBABY#0#1&thre+L_line_5#2#0&trend*L_line_30#AVGPRICE#1&diff&HS*COS#FLOOR#1&cross*close_DEMA_60#3#0&trend+L_line_5#2#0&trend*MOM_14#1#1&trend*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross*CDLABANDONEDBABY#0#1&thre+L_line_5#2#0&trend*MOM_14#1#1&trend*STOCHRSI_fastd_5#STOCHRSI_fastk_7#0&cross*close_DEMA_60#3#0&trend+L_line_5#2#0&trend*MOM_14#1#1&trend*close_TRIMA_60#2#1&trend&HS*CDLABANDONEDBABY#0#1&thre+L_line_5#2#0&trend*MOM_14#1#1&trend*close_TRIMA_60#2#1&trend&HS*close_DEMA_60#3#0&trend+L_line_5#2#0&trend*MOM_14#1#1&trend*COS#FLOOR#1&cross*CDLABANDONEDBABY#0#1&thre+L_line_5#2#0&trend*MOM_14#1#1&trend*COS#FLOOR#1&cross*close_DEMA_60#3#0&trend','MOM_12#CMO_14#1&diff*VAR_26#3#0&trend&HS*close_DEMA_14#32#1&thre&HS+MOM_12#CMO_14#1&diff*VAR_26#3#0&trend&HS*L_line_26#MAVP_60#1&diff&HS+MOM_12#CMO_14#1&diff*VAR_26#3#0&trend&HS*ROCR_14#1#0&thre&HS+MOM_12#CMO_14#1&diff*STDDEV_26#2#0&thre&HS*close_DEMA_14#32#1&thre&HS+MOM_12#CMO_14#1&diff*STDDEV_26#2#0&thre&HS*L_line_26#MAVP_60#1&diff&HS+MOM_12#CMO_14#1&diff*STDDEV_26#2#0&thre&HS*ROCR_14#1#0&thre&HS+MOM_12#CMO_14#1&diff*ROC_14#-10#0&thre*close_DEMA_14#32#1&thre&HS+MOM_12#CMO_14#1&diff*ROC_14#-10#0&thre*L_line_26#MAVP_60#1&diff&HS+MOM_12#CMO_14#1&diff*ROC_14#-10#0&thre*ROCR_14#1#0&thre&HS'],
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