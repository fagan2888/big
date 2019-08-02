# -*- coding: utf-8 -*-
import sys,os,time
#sys.path.append(os.path.abspath('../'))
#now_file = os.path.abspath(os.path.dirname(__file__))
#up_file = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#up_file = os.path.abspath(os.path.join(os.getcwd(), ".."))
from rqdata import up_file,now_file
sys.path.append(up_file)
import src.params
from rqdata import history_bars, get_1d_data

import argparse

def get_bk_codes(bkname):
    global tdate
    L = []
    f = open(up_file+'/stocks/'+bkname+'.txt','r',encoding='utf-8')
    for line in f.readlines():
        code = line.strip().split('\t')[0][-6:]
        if code[0] == '6':
            code += '.XSHG'
        else:
            code += '.XSHE'
        #print(get_1d_data(code, tdate).empty)
        if get_1d_data(code, tdate).empty:
            continue
        L.append(code)
    f.close()
    #print(bkname,L)
    return L

def get_code_list(date):
    global tdate
    tdate = date
    params = src.params.PARAMS
    stockcodes = {}
    totalnum = 0
    for bkname in params['bk_weights']:
        stockcodes[bkname] = get_bk_codes(bkname)
        totalnum += len(stockcodes[bkname])
    output_num = int(totalnum * params['output_rate'])
    bk_weights_sum = sum([ params['bk_weights'][bkname] for bkname in params['bk_weights'] ])
    
    ### 多因子评分 ###
    result_codes = []
    f = open('stock_score.csv','w',encoding='utf-8')
    for bkname in stockcodes:
        codes = stockcodes[bkname]
        target_num = int(output_num*params['bk_weights'][bkname] / bk_weights_sum)
        stock_score = {}
        for code in codes:
            stock_score[code] = []
        for factor in params['factors']:
            L = []
            for code in codes:
                L.append([factor[0](code, date) ,code])
            L = sorted(L, key=lambda x:x[0])
            for i in range(len(L)):
                code = L[i][1]
                score = (i+1)/len(L)
                stock_score[code].append(score)
        codes = sorted(codes,key=lambda code: sum(stock_score[code][i]*params['factors'][i][1]  for i in range(len(stock_score[code]))) ,reverse=True)
        
        f.write(bkname+'\n')
        result_codes += codes[:target_num]
        for code in codes[:target_num]:
            f.write('%s'%code)
            for i in range(len(stock_score[code])):
                f.write(',%.2f'%(100*stock_score[code][i]))
            f.write(',%.2f\n'%(100*sum(stock_score[code][i]*params['factors'][i][1] for i in range(len(stock_score[code]))) / sum(params['factors'][j][1]  for j in range(len(stock_score[code])))))
    f.close()

    ### 资金分配 ###
    result_codes = list(set(result_codes))
    result_codes = sorted(result_codes)
    proportion = params['asset_proportion'](result_codes, date)
    f = open('proportion.csv','w',encoding='utf-8')
    for i in range(len(result_codes)):
        f.write('%s,%.4f\n'%(result_codes[i], proportion[i]))
    f.close()


    return result_codes, proportion

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('--date','-d', required = True, type = str)
    args = parser.parse_args()
    args.date = '20170306'
    print(get_code_list(args.date))
