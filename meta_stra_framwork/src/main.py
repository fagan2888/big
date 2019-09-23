import params
from sig_meta_stratege import main
from strategy import init,handle_bar
from rqalpha import run_func
import copydata
import re
import copy
import get_new_expre
import pandas as pd
from rqdata import up_file,now_file

def singel_expre_test():
    param =  params.PARAMS
    if(param['get_code_data']):
        copydata.main(param['code_list'])
    main(_begin_date = param['begin_date'],
        code_list = param['code_list'],
        signal_save_path = param['_signal_save_path'],
        Expression = param['_Expression'])
    results = run_func(init=init, handle_bar=handle_bar, config=param['_config'])

def optimal_expre():
    param =  params.PARAMS
    if(param['get_code_data']):
        copydata.main(param['code_list'])
    ori_expre = param['_Expression']
    new_expre_list = [ori_expre]
    new_expre_list += get_new_expre.get_new_expre_list(ori_expre)
    expre_result = {}
    expre_result['expression'] = []
    expre_result['unit_net_value'] = []
    for new_expre in new_expre_list:
        try:
            main(_begin_date = param['begin_date'],
                code_list = param['code_list'],
                signal_save_path = param['_signal_save_path'],
                Expression = new_expre)
            results = run_func(init=init, handle_bar=handle_bar, config=param['_config'])
            expre_result['expression'].append(new_expre)
            expre_result['unit_net_value'].append(results["sys_analyser"]['summary']['unit_net_value'])
        except Exception as e:
            print(e)
        expre_result_fra = pd.DataFrame(expre_result)
        expre_result_fra.to_excel(param['_signal_save_path']+'expre.xlsx')
if __name__ == "__main__":
    #optimal_expre()
    singel_expre_test()