# -*- coding: utf-8 -*-
import sys,os
from collections import defaultdict

now_file = os.path.abspath(os.path.dirname(__file__))
up_file = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(up_file)

from factors.turnover_factor import TurnoverFactor
from factors.beta_factor import BetaFactor
from factors.return_factor import ReturnFactor
from factors.std_factor import StdFactor


from proportion.base_proportion import BaseProportion
from proportion.minvar_proportion import MinVarProportion
from proportion.minerr_proportion import MinErrProportion
from proportion.maxdiv_proportion import MaxDivProportion

PARAMS = defaultdict(
	lambda: None,
	# 选股的多因子
	factors = [
		# 每个list为一个因子 第一项为因子类XxxFactor  第二项为因子权重
		[TurnoverFactor(60) , 1], 
		[BetaFactor(242), 1],
		[ReturnFactor(60), 1],
		[StdFactor(60), 1],
	],
	# 板块权重配比【注意板块名称需与目录stocks内成分股文件名对应，即‘证券’对应‘证券.txt’】
	bk_weights={
		'银行' : 1,
		'证券' : 1,
		'保险' : 1,
		'互联网保险':1,
		'供应链金融':1,
		'互联网金融':1,
		'消费金融':1,
		'信托':1,
	},
	# 资金分配方法
	#asset_proportion = MinErrProportion(60),
	asset_proportion = BaseProportion(),
	# 输出股票的比例
	output_rate = 0.2,
)