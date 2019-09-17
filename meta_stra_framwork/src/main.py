import params
from sig_meta_stratege import main
from strategy import init,handle_bar
from rqalpha import run_func
import copydata

if __name__ == "__main__":
    param =  params.PARAMS
    if(param['get_code_data']):
        copydata.main(param['code_list'])
    main(_begin_date = param['begin_date'],
        code_list = param['code_list'],
        signal_save_path = param['_signal_save_path'],
        Expression = param['_Expression'])
    results = run_func(init=init, handle_bar=handle_bar, config=param['_config'])