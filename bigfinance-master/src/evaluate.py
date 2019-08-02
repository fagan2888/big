# -*- coding: utf-8 -*-
import sys,os
import numpy as np


def eval(jz_list):
    print('累计收益 %.2f'%((jz_list[-1]-1)*100))
    print('年化收益 %.2f'%((jz_list[-1]-1)*100*252/len(jz_list)))

    returns = np.array([jz_list[i]/jz_list[i-1]-1 for i in range(1,len(jz_list)) ])
    print('波动率   %.2f'%(returns.std()))
    print('夏普比   %.2f'%(np.sqrt(252)*returns.mean()/ returns.std()))
    dropback = 0
    for i in range(1,len(jz_list)):
        top = max(jz_list[:i])
        dropback = min(dropback, jz_list[i]/top-1)
    print('最大回撤 %.2f'%(-100*dropback))
 

def eval_model(trade_file='./tradeinfo.csv'):
    with open(trade_file,'r',encoding='utf-8') as f:
        jz = []
        start = -1
        for line in f.readlines():
            money = float(line.split(',')[1])
            if start == -1:
                jz.append(1.0)
                start = money
            else:
                jz.append(money / start)
        eval(jz)

if __name__ =='__main__':
    eval_model()
