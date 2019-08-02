# -*- coding:UTF-8 -*-
import numpy as np
import pandas as pd
import math


def read_file(filename):
	'''
    读取文件
    '''
	localpath = "/Users/wode/Desktop/"  # 文件地址
	file = localpath + "/" + filename
	f = open(file)
	lines = f.readlines()
	line = [float(line.strip("\n")) for line in lines]
	return line


def read_csv(filename, zs_name):
	localpath = "/Users/wode/Desktop/"  # 文件地址

	# filename = "sharp_1.csv"

	file = localpath + "/" + filename

	data = pd.read_csv(file)
	return list(data[zs_name])


def Total_Return(line):
	# 计算累计收益率
	PVend = line[-1]
	PVstart = line[0]
	p = (PVend - PVstart) / PVstart
	return p


def Total_Return_2(line):
	# line = np.log(line)
	# print line
	day_ret = [0]
	for i in range(1, len(line)):
		re_i = line[i] - line[i - 1]
		# print re_i
		day_ret.append(re_i)
	day_ret = np.array(day_ret)
	daily_mean = np.mean(day_ret)
	return daily_mean


def Total_Annualized_Return(line, all_day=245):
	# 计算年化收益率
	# p=Total_Return(line)
	p = Total_Return(line)
	n = len(line)
	# print p,n
	total_annualized_return = (pow((1 + p), all_day / n) - 1)
	# print total_annualized_return
	return total_annualized_return


def Total_Annualized_Return_2(line):
	# 计算年化收益率
	# p=Total_Return(line)
	p = Total_Return_2(line)
	# print p
	n = len(line)
	# print n
	# total_annualized_return=(pow((1+p),244/n)-1)
	total_annualized_return = p
	return total_annualized_return


def Daily_Volatility(line):
	# 策略日收益标准
	day_ret = [0]
	for i in range(1, len(line)):
		re_i = line[i] - line[(i - 1)]

		day_ret.append(re_i)
	# print re_i
	day_ret = np.array(day_ret)
	# print day_ret
	daily_volatility = np.std(day_ret)
	# print daily_volatility
	return daily_volatility


def Annual_Volatility(line, n=244):
	# 年度波动率
	annual_volatility = math.sqrt(n) * Daily_Volatility(line)
	return annual_volatility


def Sharpe(line, Rf=0.03, n=244):
	# 夏普率
	total_annualized_return = Total_Annualized_Return(line)
	sharpe_ratio = (total_annualized_return - Rf) / Annual_Volatility(line)
	# sharpe_ratio = (total_annualized_return - Rf/n) / (Annual_Volatility(line)*np.sqrt(n))
	return sharpe_ratio


def Sharpe_2(line, Rf=0.03, n=244):
	# 夏普率
	total_annualized_return = Total_Annualized_Return_2(line)
	# sharpe_ratio=(total_annualized_return-Rf)/Annual_Volatility(line)
	# sharpe_ratio = (total_annualized_return - Rf/n) / (Annual_Volatility(line)/np.sqrt(n))
	#print(Annual_Volatility(line))
	sharpe_ratio = (total_annualized_return - Rf / n) / (Annual_Volatility(line) / n)
	return sharpe_ratio


def Max_Draw_Down_List(line):
	'''
    计算最大回撤，其中ret是累计收益率的变化值
    '''
	max_drow_down = 0
	temp_max_value = 0
	for i in range(1, len(line)):
		temp_max_value = max(temp_max_value, line[i - 1])
		max_drow_down = min(max_drow_down, line[i] / temp_max_value - 1)
	return max_drow_down


def main():
	# line=read_file("return.txt")
	zs_name_list = ['wn', 'szzz', 'sz50', 'hs300', 'cybz']
	for zs_name in zs_name_list:
		line = read_csv("sharp_3.csv", zs_name)
		total_annualized_return = Total_Annualized_Return(line)
		sharpe_ratio = Sharpe(line)
		max_draw_down = Max_Draw_Down_List(line)
		print(zs_name + "年化收益率是%s,夏普率是%s,最大回撤是%s" % (total_annualized_return, sharpe_ratio, max_draw_down))


# return (total_annualized_return,sharpe_ratio,max_draw_down)

def main_2():
	# line=read_file("return.txt")
	zs_name_list = ['wn', 'szzz', 'sz50', 'hs300', 'cybz']
	for zs_name in zs_name_list:
		line = read_csv("sharp_3.csv", zs_name)
		# line = line[1:]
		# print line
		max_draw_down = Max_Draw_Down_List(line)
		line = np.log(line)
		# print line
		total_annualized_return = Total_Annualized_Return_2(line)
		sharpe_ratio = Sharpe_2(line)
		# max_draw_down=Max_Draw_Down_List(line)
		print(zs_name + "年化收益率是%s,夏普率是%s,最大回撤是%s" % (total_annualized_return * len(line), sharpe_ratio, max_draw_down))


# return (total_annualized_return,sharpe_ratio,max_draw_down)

if __name__ == '__main__':
	main()
	main_2()
# line=read_file("return.txt")
# max_draw_down=Max_Draw_Down_List(line)
# print("最大回撤是%s"%max_draw_down)
