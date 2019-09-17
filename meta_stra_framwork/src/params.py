import sys,os
from collections import defaultdict

now_file = os.path.abspath(os.path.dirname(__file__))
up_file = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(up_file)


PARAMS = defaultdict(
begin_date = 20190101,#信号计算开始日期
code_list = ['000001.XSHE'],#信号计算的股票池
#code_list = get_all_code(up_file+'/wmdata'),
#code_list = get_code_list(),
get_code_data = True,#是否重新获得原始数据
HS_code = '999999.XSHG',#信号中的大盘信号代码
_signal_save_path = up_file+'/result/newzhongli/', #信号结果储存地址
#信号的表达式，第一个为做多买入信号，第二个为做多卖出信号
_Expression =['close_EMA_7#close_EMA_15#1&diff*close_EMA_15#close_EMA_25#1&diff*close_EMA_15#2#1&trend*close_EMA_25#2#1&trend*MACD#0#1&thre*close#close_shift_4#1&diff*K#40#1&thre&HS',
                'MACD#0#0&thre+K#40#0&thre&HS'],
#回测参数
_config = {
    "base":
    {
          "benchmark": "399300.XSHE",
          "margin_multiplier": 1.4,
          "start_date": "2015-01-01",
          "end_date":   "2019-02-01",
          "frequency": "1d",
          "accounts":{
            "stock":  100000000,
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
        "plot":                True,
      },
      "sys_simulation":{
        "enabled":               True,
        "signal":                True,
        "slippage":              0.0005,
        #"slippage":              0.0,
        "matching_type":         "current_bar",
        "price_limit":           False,
        "volume_limit":          False,
        "commission-multiplier": 0,
      },
    },
}
)