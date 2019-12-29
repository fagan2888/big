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
import quick_sig as qs
import time
import sig_data
def singel_expre_test():
    param =  params.PARAMS
    if(param['get_code_data']):
        copydata.main(param['code_list'])
    main(_begin_date = param['begin_date'],
        code_list = param['code_list'],
        signal_save_path = param['_signal_save_path'],
        Expression = param['_Expression'],
        HS_code = param['HS_code'])
    results = run_func(init=init, handle_bar=handle_bar, config=param['_config'])

def optimal_expre(off_line = False):
    param =  params.PARAMS
    if(param['get_code_data']):
        copydata.main(param['code_list'])
    ori_expre,code_list = param['_Expression'],param['code_list']
    new_expre_list = [ori_expre]
    new_expre_list += get_new_expre.get_new_expre_list(ori_expre)
    expre_result,unit_seris = {},{}
    expre_result['expression'],expre_result['unit_net_value'] = [],[]
    _code_list = copy.copy(code_list)
    if(not off_line):
        for code in code_list:
            if(sig_data.cal_index_data(code) == 0):
                _code_list.remove(code)
        #sig_data.cal_index_data(HS_code)
    for new_expre in new_expre_list: 
        #try:
        start = time.clock()
        qs.get_signal(_code_list,new_expre)
        end = time.clock()
        print('sig',str(end-start))
        start = time.clock()
        results = run_func(init=init, handle_bar=handle_bar, config=param['_config'])
        expre_result['expression'].append(new_expre)
        unit_seris[str(new_expre)] = results["sys_analyser"]['portfolio']['unit_net_value'].tolist()
        expre_result['unit_net_value'].append(results["sys_analyser"]['summary']['unit_net_value'])
        end = time.clock()
        print('back',str(end-start))
        #except Exception as e:
            #print(e)
    unit_seris['benchmark'] = results["sys_analyser"]['benchmark_portfolio']['unit_net_value'].tolist()
    unit_seris['date'] = results["sys_analyser"]['portfolio']['unit_net_value'].index.tolist()
    expre_result_fra = pd.DataFrame(expre_result)
    expre_result_fra.to_excel(param['_signal_save_path']+'expre.xlsx')
    unit_seris_fra = pd.DataFrame(unit_seris)
    unit_seris_fra.to_excel(param['_signal_save_path']+'unit.xlsx')
def bayesian_opt(expression):
    param =  params.PARAMS
    if(param['get_code_data']):
        copydata.main(param['code_list'])
    main(_begin_date = param['begin_date'],
                code_list = param['code_list'],
                signal_save_path = param['_signal_save_path'],
                Expression = expression,
                HS_code = param['HS_code'])
    results = run_func(init=init, handle_bar=handle_bar, config=param['_config'])
    return results["sys_analyser"]['summary']['unit_net_value']
if __name__ == "__main__":
    optimal_expre(off_line = False)
    #singel_expre_test()