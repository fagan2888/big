import params_1
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
import KB

import smtplib
from email.mime.multipart import MIMEMultipart    
from email.mime.text import MIMEText    
from email.mime.image import MIMEImage 
from email.header import Header 

def email(estr,subject):
    username = 'lsz17801016296@163.com'
    password = 'MKJQHGVZYYHTEEDP'
    now_time = time.strftime("%Y%m%d", time.localtime())

    msg = MIMEMultipart('mixed') 
    msg['Subject'] = now_time+' '+subject
    msg['From'] = 'lsz17801016296@163.com <lsz17801016296@163.com>'
    msg['To'] = '495506796@qq.com'
    #收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
    #msg['To'] = ";".join(receiver) 
    msg['Date'] = now_time

    #构造文字内容      
    text_plain = MIMEText(estr,'plain', 'utf-8')    
    msg.attach(text_plain)    

    smtp = smtplib.SMTP() 
    smtp.connect('smtp.163.com') 
    smtp.login(username, password) 
    smtp.sendmail('lsz17801016296@163.com','495506796@qq.com', msg.as_string()) 
    smtp.quit()


def get_day_code():
    param =  params_1.PARAMS
    KB.copy_day_data(param['code_list'])
    KB.copy_day_data([param['HS_code']])
    ori_expre,code_list = param['_Expression'],param['code_list']
    _code_list = copy.copy(code_list)
    for code in code_list:
        if(sig_data.cal_index_data(code) == 0):
            _code_list.remove(code)
    HS_code = param['HS_code']
    sig_data.cal_index_data(HS_code)
    result = qs.get_signal(_code_list,ori_expre,param['begin_date'])
    result.to_csv(up_file+'/result/quick/quick_sig_1.csv')
    new_signal = pd.read_csv(up_file+'/result/quick/quick_sig_1.csv')
    now_time = time.strftime("%Y%m%d", time.localtime())
    new_code = new_signal[new_signal['time'] == int(now_time)]
    #print(new_signal['time'].values[-1],type(new_signal['time'].values[-1]),new_code)
    new_buy = new_code[new_code['operation'] == 'long']['code']
    new_sell = new_code[new_code['operation'] == 'long_sell']['code']
    print('buy',new_buy.values)
    print('sell',new_sell.values)
    email(str(new_buy.values),'buy')
    email(str(new_sell.values),'sell')


if __name__ == "__main__":
    get_day_code()