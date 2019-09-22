import sys,os
from collections import defaultdict

now_file = os.path.abspath(os.path.dirname(__file__))
up_file = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(up_file)


PARAMS = defaultdict(
begin_date = 20190101,#信号计算开始日期
code_list = ['000001.XSHE'],#信号计算的股票池
get_code_data = True,#是否重新获得原始数据
HS_code = '999999.XSHG',#信号中的大盘信号代码
_signal_save_path = up_file+'/result/newzhongli/', #信号结果储存地址
# 信号的表达式，第一个为做多买入信号，第二个为做多卖出信号
# 信号的构建方法为 
# 阈值型信号 指标名+#+方向(1为大于,0为小于)+&thre,如果为大盘信号，则在最后加上&HS
# 交叉型信号 指标1名+#+指标2名+#+方向(1为金叉,0为死叉)+&cross,如果为大盘信号，则在最后加上&HS
# 趋势型信号 指标1名+#+指标2名+#+方向(1为上涨,0为下跌)+&trend,如果为大盘信号，则在最后加上&HS
# 比较型信号 指标1名+#+指标2名+#+方向(1为指标1大于指标2,0为指标1小于指标2)+&diff,如果为大盘信号，则在最后加上&HS
# 信号组合可以使用+和*进行或和且逻辑运算,指标名称可在index_24中查询
_Expression =['close_EMA_20#close_EMA_50#1&cross&times',
                'close_EMA_20#close_EMA_50#1&cross'],
# 回测参数，目前设定是第二天开盘买入，当天收盘卖出，每次以资金的三分之一操作，默认
# 是下跌1%时候止损卖出
# 可以在strategy.py中更改
# 更多参数设置可以百度搜索rqalpha
_config = {
    "base":
    {
          "benchmark": "399300.XSHE", #基准
          "margin_multiplier": 1.4, #
          "start_date": "2015-01-01", #回测开始日期
          "end_date":   "2019-02-01", #回测结束日期
          "frequency": "1d", #回测频率
          "accounts":{
            "stock":  100000000, #回测本金
            #"future": "~",
          }
    },
    "extra":{
        "log_level": "warning",
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