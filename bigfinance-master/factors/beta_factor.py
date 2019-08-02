# -*- coding: utf-8 -*-
from src.rqdata import get_1d_data
from factors.base_factor import BaseFactor
import numpy as np

class BetaFactor(BaseFactor):
	def __init__(self, period, benchmark='999999.XSHG'):
		BaseFactor.__init__(self)
		self.period = period
		self.benchmark = benchmark

	def __call__(self, code, date):
		# get_1d_data(code, date, limit=self.period)
		df = get_1d_data(self.benchmark, date, limit=self.period)
		stock = get_1d_data(code, date, limit=self.period)
		if len(df) > 0 and len(stock) > 0:
			beta = stock['percent'].cov(df['percent'])/np.var(df['percent'])
		else:
			beta = None
		return beta


