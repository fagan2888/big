# -*- coding: utf-8 -*-
import sys,os,time
from proportion.base_proportion import BaseProportion
from src.rqdata import history_bars, get_1d_data

import pandas as pd
import numpy as np
from scipy.optimize import minimize


def fun(args):
	cov = args
	target = lambda w: np.matmul(w, np.matmul(cov, w))
	return target

def con():
	cons = ({'type':'eq','fun': lambda w: sum(w) - 1})
	return cons

class MinVarProportion(BaseProportion):
	def __init__(self, period):
		BaseProportion.__init__(self)
		self.period = period

	def __call__(self, codes, date):
		dic = {}
		for code in codes:
			stock = get_1d_data(code, date, limit=self.period)
			dic[code] = stock['percent']
		df = pd.DataFrame(dic)
		### Method 1 ###
		cov = np.mat(df.cov().as_matrix())
		vec1 = np.mat(np.ones((len(codes),1)))
		up = cov.I*vec1
		down = (vec1.T*cov.I*vec1)
		weights = (up / down).T.getA()[0]
		
		### Method 2 ###
		cov = df.cov().as_matrix()
		w0 = np.array([1.0/len(codes) for code in codes])
		res = minimize(fun(cov), w0, method='SLSQP', constraints=con(), bounds=[(0,1) for code in codes])
		
		return res.x



