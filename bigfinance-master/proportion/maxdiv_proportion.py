# -*- coding: utf-8 -*-
import sys,os,time
from proportion.base_proportion import BaseProportion
from src.rqdata import history_bars, get_1d_data

import pandas as pd
import numpy as np
from scipy.optimize import minimize


def fun(args):
	cov, std = args
	target = lambda w: -np.dot(w, std) / np.matmul(w, np.matmul(cov, w))**0.5
	return target

def con():
	cons = ({'type':'eq','fun': lambda w: sum(w) - 1})
	return cons

class MaxDivProportion(BaseProportion):
	def __init__(self, period):
		BaseProportion.__init__(self)
		self.period = period

	def __call__(self, codes, date):
		dic = {}
		std = []
		for code in codes:
			stock = get_1d_data(code, date, limit=self.period)
			dic[code] = stock['percent']
			std.append( np.std(stock['close']) )
		df = pd.DataFrame(dic)
		cov = df.cov().as_matrix()
		std = np.array(std)
		w0 = np.array([1.0/len(codes) for code in codes])

		res = minimize(fun((cov, std)), w0, method='SLSQP',constraints=con(), bounds=[(0,1) for code in codes])
		return res.x
