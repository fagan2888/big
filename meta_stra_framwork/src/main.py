import params
#from sig_meta_stratege import main
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
import os
import sharpe_2 as s2
import KB

single_expre_save_path = up_file+'/result/single/single.xlsx'
unit_save_path = up_file+'/result/single/unit.xlsx'

def get_year_result(writer,trade,unit_seris,ori_expre):
    summ = {}
    date = unit_seris.index.tolist()
    year_list = list(set([x.year for x in date]))
    summ['strategy_name'] = str(ori_expre)
    for year in year_list:
        one_unit = unit_seris.loc[str(year)+'0101':str(year)+'1231']
        one_trade_num = len(trade.loc[str(year)+'-01-01 15:00:00':str(year)+'-12-31 15:00:00','side'])
        one_list = one_unit.tolist()
        summ[str(year)+'max_draw_down'] = s2.Max_Draw_Down_List(one_list)
        summ[str(year)+'trade_num'] = one_trade_num 
        summ[str(year)+'Sharpe'] = s2.Sharpe_2(one_list)
        summ[str(year)+'Total_Return'] = s2.Total_Return(one_list)
    save_backtest_result(writer,summ,ori_expre,sheet_name = '分年')

def add_new_result(old,new):
    if(len(old)==0):
        for key in new.keys():
            old[key] = []

    for key in new.keys():
        old[key].append(new[key])
    return old

def save_backtest_result(writer,summ,ori_expre,sheet_name = ''):
    df = pd.read_excel(single_expre_save_path, None)
    sheet_names = df.keys()
    if (sheet_name not in sheet_names):
        all_re = pd.DataFrame(summ,index = [0])
    else:
        all_re = pd.read_excel(single_expre_save_path,index_col = 0,sheet_name=sheet_name).T
        all_re.loc[str(ori_expre)+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())] = summ
    all_re.T.to_excel(writer,sheet_name)

def save_unit_result(unit_seris,benchmark_unit,ori_expre):
    if os.path.exists(unit_save_path):
        unit_fra = pd.read_excel(unit_save_path,index_col = 0)
        if(len(unit_fra) == len(unit_seris)):
            unit_fra[str(ori_expre)+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())] = unit_seris.tolist()
        else:
            unit_dict = {}
            unit_dict[str(ori_expre)] = unit_seris.tolist()
            unit_dict['benchmark'] = benchmark_unit.tolist()
            unit_fra = pd.DataFrame(unit_dict,index = unit_seris.index.tolist())
    else:
        unit_dict = {}
        unit_dict[str(ori_expre)] = unit_seris.tolist()
        unit_dict['benchmark'] = benchmark_unit.tolist()
        unit_fra = pd.DataFrame(unit_dict,index = unit_seris.index.tolist())
    unit_fra.to_excel(unit_save_path)

def save_result(unit_seris,ori_expre,summ,trade,benchmark_unit):
    if not os.path.exists(single_expre_save_path):
        all_re = pd.DataFrame(summ,index = [0])
        all_re.T.to_excel(single_expre_save_path,sheet_name= '综合')
    writer = pd.ExcelWriter(single_expre_save_path)
    get_year_result(writer,trade,unit_seris,ori_expre)
    save_backtest_result(writer,summ,ori_expre,sheet_name = '综合')
    writer.save()
    save_unit_result(unit_seris,benchmark_unit,ori_expre)

def singel_expre_test(off_line = False):
    param =  params.PARAMS
    if(param['get_code_data']):
        #copydata.main(param['code_list'])
        KB.copy_day_data(param['code_list'])
        KB.copy_day_data([param['HS_code']])
    ori_expre,code_list = param['_Expression'],param['code_list']
    _code_list = copy.copy(code_list)
    if(not off_line):
        for code in code_list:
            if(sig_data.cal_index_data(code) == 0):
                _code_list.remove(code)
        HS_code = param['HS_code']
        sig_data.cal_index_data(HS_code)
    result = qs.get_signal(_code_list,ori_expre,param['begin_date'])
    result.to_csv(up_file+'/result/quick/quick_sig.csv')
    results = run_func(init=init, handle_bar=handle_bar, config=param['_config'])
    unit_seris = results["sys_analyser"]['portfolio']['unit_net_value']
    benchmark_unit = results["sys_analyser"]['benchmark_portfolio']['unit_net_value']
    summ = results['sys_analyser']['summary']
    _trade = results['sys_analyser']['trades']
    summ['strategy_name'] = str(ori_expre)
    summ['stock_num'] = len(code_list)
    save_result(unit_seris,ori_expre,summ,_trade,benchmark_unit)
    return results
def optimal_expre(off_line = False):
    param =  params.PARAMS
    if(param['get_code_data']):
        copydata.main(param['code_list'])
    ori_expre,code_list = param['_Expression'],param['code_list']
    new_expre_list = [ori_expre]
    new_expre_list += get_new_expre.get_new_expre_list(ori_expre)
    print(new_expre_list)
    expre_result,unit_seris = {},{}
    expre_result['expression'] = []
    _code_list = copy.copy(code_list)
    if(not off_line):
        for code in code_list:
            if(sig_data.cal_index_data(code) == 0):
                _code_list.remove(code)
        HS_code = param['HS_code']
        sig_data.cal_index_data(HS_code)
    for new_expre in new_expre_list: 
        try:
            start = time.clock()
            qs.get_signal(_code_list,new_expre,param['begin_date'])
            end = time.clock()
            print('sig',str(end-start))
            start = time.clock()
            results = run_func(init=init, handle_bar=handle_bar, config=param['_config'])
            unit_seris[str(new_expre)] = results["sys_analyser"]['portfolio']['unit_net_value'].tolist()
            expre_result['expression'].append(new_expre)
            expre_result = add_new_result(expre_result,results['sys_analyser']['summary'])
            end = time.clock()
            print('back',str(end-start))
        except Exception as e:
            print(e)
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
    return results["sys_analyser"][   'summary']['unit_net_value']



if __name__ == "__main__":
    #optimal_expre()
    singel_expre_test(True)