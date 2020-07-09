import re
import numpy as np
import pandas as pd
import main
import get_split_stra as gss
from rqdata import up_file,now_file
import get_zl_expre

def get_s(s):
    s_ = re.split('\[|\]|,|\'',s)
    s1 = s_[2]
    s2 = s_[5]
    s1_1 = re.split('\*',s1)
    s2_1 = re.split('\*',s2)
    s1_2 = []
    s2_2 = []

    for i in range(len(s1_1)):
        temp = re.split('\+',s1_1[i])
        s1_2.append(temp)

    for i in range(len(s2_1)):
        temp = re.split('\+',s2_1[i])
        s2_2.append(temp)
    return(s1_1,s1_2,s2_1,s2_2)

def get_result(s,s1_1,s1_2,s2_1,s2_2):
    result = []
    #去小项
    for i in range(len(s1_2)):
        for j in range(len(s1_2[i])):
            if j==0 and len(s1_2[i])==1:
                if i==0:
                    temp_str = s.replace(s1_2[i][j]+'*','')
                else:
                    temp_str = s.replace('*'+s1_2[i][j],'')
            elif j==0:
                temp_str = s.replace(s1_2[i][j]+'+','')
            else:
                temp_str = s.replace('+'+s1_2[i][j],'')
            result.append(temp_str)
    #去大项
    for i in range(len(s1_2)):
        if len(s1_2[i])!=1:
            if i==0:
                temp_str = s.replace(s1_1[i]+'*','')
            else:
                temp_str = s.replace('*'+s1_1[i],'')
            result.append(temp_str)

    #去小项
    for i in range(len(s2_2)):
        for j in range(len(s2_2[i])):
            if j==0 and len(s2_2[i])==1:
                if i==0:
                    temp_str = s.replace(s2_2[i][j]+'*','')
                else:
                    temp_str = s.replace('*'+s2_2[i][j],'')
            elif j==0:
                temp_str = s.replace(s2_2[i][j]+'+','')
            else:
                temp_str = s.replace('+'+s2_2[i][j],'')
            result.append(temp_str)
    #去大项
    for i in range(len(s2_2)):
        if len(s2_2[i])!=1:
            if i==0:
                temp_str = s.replace(s2_1[i]+'*','')
            else:
                temp_str = s.replace('*'+s2_1[i],'')
            result.append(temp_str)        

    return(result)

def get_result2(result,s,s1_1,s1_2,s2_1,s2_2):
    result2 = []
    for num in range(len(result)):
        s = result[num]
        s_ = re.split('\[|\]|,|\'',s)
        s1 = s_[2]
        s2 = s_[5]
        s1_1 = re.split('\*',s1)
        s2_1 = re.split('\*',s2)
        s1_2 = []
        s2_2 = []

        for i in range(len(s1_1)):
            temp = re.split('\+',s1_1[i])
            s1_2.append(temp)

        for i in range(len(s2_1)):
            temp = re.split('\+',s2_1[i])
            s2_2.append(temp)


        a_result = ''
        b_result = ''
        #a
        if len(s1_2)==1:
            for i in range(len(s1_2[0])):
                a_result = a_result+ '+'+s1_2[0][i]
            a_result=a_result[1:]
        elif len(s1_2)==2:
            for i in range(len(s1_2[0])):
                for j in range(len(s1_2[1])):
                    a_result = a_result+ '+'+s1_2[0][i]+'*'+s1_2[1][j]
            a_result=a_result[1:]
        elif len(s1_2)==3:
            for i in range(len(s1_2[0])):
                for j in range(len(s1_2[1])):
                    for k in range(len(s1_2[2])):
                        a_result = a_result+ '+'+s1_2[0][i]+'*'+s1_2[1][j]+'*'+s1_2[2][k]
            a_result=a_result[1:]
        elif len(s1_2)==4:
            for i in range(len(s1_2[0])):
                for j in range(len(s1_2[1])):
                    for k in range(len(s1_2[2])):
                        for h in range(len(s1_2[2])):
                            a_result = a_result+ '+'+s1_2[0][i]+'*'+s1_2[1][j]+'*'+s1_2[2][k]+'*'+s1_2[3][h]
            a_result=a_result[1:]


        #b
        if len(s2_2)==1:
            for i in range(len(s2_2[0])):
                b_result = b_result+ '+'+s2_2[0][i]
            b_result=b_result[1:]
        elif len(s2_2)==2:
            for i in range(len(s2_2[0])):
                for j in range(len(s2_2[1])):
                    b_result = b_result+ '+'+s2_2[0][i]+'*'+s2_2[1][j]
            b_result=b_result[1:]
        elif len(s2_2)==3:
            for i in range(len(s2_2[0])):
                for j in range(len(s2_2[1])):
                    for k in range(len(s2_2[2])):
                        b_result = b_result+ '+'+s2_2[0][i]+'*'+s2_2[1][j]+'*'+s2_2[2][k]
            b_result=b_result[1:]
        elif len(s2_2)==4:
            for i in range(len(s2_2[0])):
                for j in range(len(s2_2[1])):
                    for k in range(len(s2_2[2])):
                        for h in range(len(s2_2[2])):
                            b_result = b_result+ '+'+s2_2[0][i]+'*'+s2_2[1][j]+'*'+s2_2[2][k]+'*'+s2_2[3][h]
            b_result=b_result[1:]   

        temp = '[\''+a_result+'\',\''+b_result+'\']'
        temp = temp.replace('%','*')
        result2.append(temp)
    return result2

def get_split_expre(s):
    s1_1,s1_2,s2_1,s2_2 = get_s(s)
    result = get_sort_norep(get_result(s,s1_1,s1_2,s2_1,s2_2))
    result2 = get_sort_norep(get_result2(result,s,s1_1,s1_2,s2_1,s2_2))
    expre_split= {}
    expre_split['expre'] = result2
    expre_fra = pd.DataFrame(expre_split)
    expre_fra.to_excel(up_file+'/result/split'+'/expre_2.xlsx')
    return result,result2

def get_split_expre_list(ori_result):
    result_list,result2_list,mother_expre,mother_expre_list = [],[],[],[]
    for _s in ori_result:
        result,result2 = get_split_expre(_s)
        result_list += result
        result2_list += result2
        mother_expre += [_s]*len(result)
    output_result_list = np.array(get_sort_norep(result_list))
    for _r in np.array(list(set(result_list))):
        mother_expre_list.append(mother_expre[result_list.index(_r)])
    '''
    expre_split= {}
    expre_split['expre_long'] = list(set(result2_list))
    expre_split['expre_short'] = list(set(result_list))
    expre_fra = pd.DataFrame(expre_split)
    expre_fra.to_excel('/Users/wode/Desktop/expre_2.xlsx')
    '''
    return output_result_list,np.array(get_sort_norep(result2_list)),mother_expre_list


####有问题######
def get_remain_stra(result,_s_long,com_thre = 0.99):
    unit = pd.read_excel(up_file+'/result/split'+'/unit.xlsx')
    unit_columns = unit.columns.values
    ori_expre_list = get_zl_expre.get_expression_list_split()
    #ori_expre_list.append(_s_long)
    expre_list = [str(x) for x in ori_expre_list]
    if(str(_s_long) in expre_list):
        expre_list.remove(str(_s_long))
    expre_list.append(str(_s_long))
    pure_uc = [x[:-19] for x in unit_columns]
    uc_index = []
    for r in expre_list:
        uc_index.append(pure_uc.index(r))
    use_uc =  get_sort_norep(unit_columns[uc_index]) 
    use_unit = unit.loc[:,use_uc]
    remain_stra = use_unit.corr()[(use_unit.corr().loc[:,use_uc[-1]])>com_thre]
    remain_stra_name = remain_stra.index.values[:-1]
    remain_stra_name_pure =[x[:-19] for x in remain_stra_name]
    remain_stra_name_short = []
    for _r in remain_stra_name_pure:
        remain_stra_name_short.append(result[expre_list.index(_r)])
    return get_sort_norep(remain_stra_name_short),get_sort_norep(remain_stra_name_pure)

def clear_result(result,result2):
    
    new_result = []
    new_result2 = []
    unit = pd.read_excel(up_file+'/result/split'+'/unit.xlsx')
    unit_columns = unit.columns.values
    pure_uc = [x[:-19] for x in unit_columns]
    for i in range(len(result2)):
        com_e = [result2[i].split(',')[0].strip("[]''"),result2[i].split(',')[1].strip("[]''")]
        if(str(com_e) not in pure_uc):
            new_result.append(result[i])
            new_result2.append(result2[i])
    return new_result,new_result2

def save_expre(result,result2,save_name = 'expre_2'):
    expre_split= {}
    expre_split['expre_long'] = result2
    expre_split['expre_short'] = result
    expre_fra = pd.DataFrame(expre_split)
    expre_fra.to_excel(up_file+'/result/split/'+save_name+'.xlsx')

def all_result_init():
    re = {}
    re['long'] = []
    re['short'] = []
    re['mother'] = []
    return re

def all_result_add(re,result,result2,mother_list):
    re['long'] += result2.tolist()
    re['short'] += result.tolist()
    re['mother'] += mother_list
    return re

#得到不改变顺序的不重复元素列表
def get_sort_norep(l1):
    l2 = [] 
    [l2.append(i) for i in l1 if not i in l2] 
    return(l2)


if __name__ == "__main__":
    s = "['K#90#1&HS&thre+D_shift_1#10#0&HS&thre', 'close_MA_10_shift_1#close_MA_10#1&HS&diff+K_shift_1#20#0&HS&thre+D_shift_1#10#0&HS&thre*D_shift_1#80#1&HS&thre+K_shift_1#90#1&thre]"
    _s_long = "['K#90#1&HS&thre+D_shift_1#10#0&HS&thre', 'close_MA_10_shift_1#close_MA_10#1&HS&diff*D_shift_1#80#1&HS&thre+close_MA_10_shift_1#close_MA_10#1&HS&diff*K_shift_1#90#1&thre+K_shift_1#20#0&HS&thre*D_shift_1#80#1&HS&thre+K_shift_1#20#0&HS&thre*K_shift_1#90#1&thre+D_shift_1#10#0&HS&thre*D_shift_1#80#1&HS&thre+D_shift_1#10#0&HS&thre*K_shift_1#90#1&thre']"
    result,result2 = gss.get_split_expre(s)
    main.singel_expre_test(off_line = True,result_path = up_file+'/result/split')
    main.circle_expre(off_line = True,result_path = up_file+'/result/split')
    remain_stra_name_short,remain_stra_name_pure = get_remain_stra(result,_s_long)
    all_result = all_result_init()
    flag = 0
    while(len(remain_stra_name_short)>0):
    #while(flag<1):
        save_expre(remain_stra_name_short,remain_stra_name_pure,'remain_expre')
        #result,result2,mother_list = gss.get_split_expre_list(remain_stra_name_short)
        result,result2,mother_list = get_split_expre_list(remain_stra_name_short)
        all_result = all_result_add(all_result,result,result2,mother_list)
        result,result2 = clear_result(result,result2)
        save_expre(result,result2)
        main.circle_expre(off_line = True,result_path = up_file+'/result/split')
        remain_stra_name_short,remain_stra_name_pure = get_remain_stra(result,_s_long)
        flag+=1
    all_fra = pd.DataFrame(all_result)
    all_fra.to_excel(up_file+'/result/split/'+'all_result.xlsx')