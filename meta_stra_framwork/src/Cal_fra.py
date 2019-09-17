# -*- coding: utf-8 -*-
# __author__ = 'Li sz'

# 本脚本的功能是为信号框架提供运算符计算框架


import pandas as pd 
import numpy as np
import datetime
import os
import copy
import warnings
import re

def multiply_divide(s):#计算一个不含括号的最小乘除单元，用split分隔*或/然后计算
    ret = float(s.split('*')[0]) * float(s.split('*')[1]) if '*' in s else float(s.split('/')[0]) / float(
        s.split('/')[1])
    return ret
 
def remove_md(s):# 将不含括号的表达式里的乘除先递归计算完
    if '*' not in s and '/' not in s:
        return s# 没有乘除的话递归结束
    else:# 匹配一个最小乘除单元，调用multiply_divide计算，将结果拼接成一个新的表达式进行递归处理
        k = re.search(r'-?[\d\.]+[*/]-?[\d\.]+', s).group()
        s = s.replace(k, '+' + str(multiply_divide(k))) if len(re.findall(r'-', k)) == 2 else s.replace(k, str(
            multiply_divide(k)))
        return remove_md(s)
 
def add_sub(s):# 计算没有乘除的表达式，得出最后不包含括号表达式的运算结果
    l = re.findall(r'([\d\.]+|-|\+)',s)#将表达式转换成列表，
    if l[0] == '-':#如果第一个数是负数，对其进行处理
        l[0] = l[0] + l[1]
        del l[1]
    sum = float(l[0])
    for i in range(1, len(l), 2):# 循环计算结果
        if l[i] == '+' and l[i + 1] != '-':
            sum += float(l[i + 1])
        elif l[i] == '+' and l[i + 1] == '-':
            sum -= float(l[i + 2])
        elif l[i] == '-' and l[i + 1] == '-':
            sum += float(l[i + 2])
        elif l[i] == '-' and l[i + 1] != '-':
            sum -= float(l[i + 1])
    return sum
 
def basic_operation(s):# 计算一个基本的4则运算
    s = s.replace(' ', '')
    return add_sub(remove_md(s))# 调用前面定义的函数，先乘除，后加减
 
def calculate(expression):# 计算包含括号的表达式
    if not re.search(r'\([^()]+\)', expression):# 匹配最里面的括号，如果没有的话，直接进行运算，得出结果
        return basic_operation(expression)
    k = re.search(r'\([^()]+\)', expression).group()# 将匹配到的括号里面的表达式交给basic_operation处理后重新拼接成字符串递归处理
    expression = expression.replace(k, str(basic_operation(k[1:len(k) - 1])))
    return calculate(expression)

def replace_exp(expression,type_list,big_type_list,sig_list):
    for i in range(len(type_list)):
        #print(type_list[i],big_type_list)
        expression = expression.replace(type_list[i],str(sig_list[np.where(big_type_list == type_list[i])[0][0]]))
    return calculate(expression)

if __name__ == "__main__":
    expression='(MACD#0&thre+close_EMA_5#close_EMA_10&cross)*ADL#0&thre'
    #type_list = get_type_list(expression)
    #print(type_list)
    sig_list = [1,0,1]
    #print(replace_exp(expression,type_list,sig_list))
