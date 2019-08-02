# -*- coding: utf-8 -*-

class BaseProportion:
	# 等权分配
	def __init__(self):
		pass
	def __call__(self, codes, date):
		return [1.0/len(codes) for code in codes]
