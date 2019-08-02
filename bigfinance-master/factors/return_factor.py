# -*- coding: utf-8 -*-
from src.rqdata import get_1d_data
from factors.base_factor import BaseFactor
import numpy as np

class ReturnFactor(BaseFactor):
	def __init__(self, period):
		BaseFactor.__init__(self)
		self.period = period

	def __call__(self, code, date):
		# get_1d_data(code, date, limit=self.period)
		stock = get_1d_data(code, date, limit=self.period)
		closes = stock['close']
		return closes[len(closes)-1] / closes[0] - 1



