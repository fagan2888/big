# big
    meta_strategy_framwork 共分为数据，信号，回测三部分，三部分均可以分开运行
# 参数
    params.py 参数设定
# 数据获取
    rqdata.py 
    copydata.py
    可以单独使用，在copydata中的main函数中给定股票列表即可
# 信号计算
    index_24.py 原始指标计算
    sig_data.py 数据处理
    sig_fra.py 原始信号计算
    sig_meta_strategy.py 策略信号计算 
    diff.py 分数阶差分
    Cal_fra.py 信号组合
# 回测
    strategy,py 策略回测
# 使用方法
    在params中设定好参数，运行main.py脚本即可
# 注意事项
    1.如果出现需要计算的指标没有在库里，需要检查sig_data.py中的cal_index_data函数中是否计算了此指标
    2.此框架可以生成做空信号，可以在sig_meta_strategy.py中调整，但是使用的回测框架无法对股票做空