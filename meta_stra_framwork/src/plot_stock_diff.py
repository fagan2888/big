from rqalpha.api import *
from rqalpha import run_func
from strategy import init,handle_bar
import os
#import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import quick_sig as qs
import params
import tushare as ts
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import sklearn
from rqdata import up_file,now_file
import get_zl_expre
import pandas as pd

def main():
    param =  params.PARAMS
    code_list = params.get_code_list()
    expre_list = get_zl_expre.get_expression_list_3()

    score = {}
    a_r = {}
    vol = {}
    use_expre = []
    k = 0
    for ori_expre in expre_list[0:2]:
        if('xxx' in ori_expre[0] or 'xxx' in ori_expre[1]):
            continue
        else:
            try:
                X = {}
                X['annual_return'] = []
                X['volitility'] = []
                a_r[str(ori_expre)] = []
                vol[str(ori_expre)] = []
                for code in code_list[0:4]:
                    try:
                        _code_list = [code]
                        result = qs.get_signal(_code_list ,ori_expre,param['begin_date'])
                        result.to_csv(up_file+'/result/diff/quick_sig.csv')
                        results = run_func(init=init, handle_bar=handle_bar, config=param['_config'])
                        X['annual_return'].append(results['sys_analyser']['summary']['annualized_returns'])
                        X['volitility'].append(results['sys_analyser']['summary']['volatility'])
                        a_r[str(ori_expre)].append(results['sys_analyser']['summary']['annualized_returns'])
                        vol[str(ori_expre)].append(results['sys_analyser']['summary']['volatility'])
                    except:
                        a_r[str(ori_expre)].append(0)
                        vol[str(ori_expre)].append(0)
                _X = pd.DataFrame(X,index = code_list[0:4])
                #print(len(_X))
                kmeans_model = KMeans(n_clusters=2, random_state=1).fit(_X)
                labels = kmeans_model.labels_
                #print(labels)
                score[str(ori_expre)] =  sklearn.metrics.silhouette_score(_X, labels, metric='euclidean')
                use_expre.append(str(ori_expre))
                k = k + 1
            except Exception as e:
                print(e)
    a_r_fra = pd.DataFrame(a_r,index = code_list[0:4])
    vol_fra = pd.DataFrame(vol,index = code_list[0:4])
    score_fra = pd.DataFrame(score,index = code_list[0:2])
    a_r_fra.to_excel(up_file+'/result/diff/ar.xlsx')
    vol_fra.to_excel(up_file+'/result/diff/vol.xlsx')
    score_fra.to_excel(up_file+'/result/diff/score.xlsx')

if __name__ == "__main__":
    main()