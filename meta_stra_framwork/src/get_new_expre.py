import pandas
import numpy
import re
import copy

def split_expre(ori_list):
    new_list = []
    for meta in ori_list:
        index_list = meta.split('&')
        ri_list = index_list[0].split('#')
        new_ri_list = []
        for ri in ri_list:
            new_ri_list.append(ri.split('_'))
            #new_ri_list += ri.split('_')
        new_ri_list+=index_list[1:]
        #new_list.append(new_ri_list)
        new_list += new_ri_list
    return new_list

def compose_expre(meta_list):
    signal_type = ['diff','cross','thre','trend','HS']
    index_list = []
    for meta in meta_list:
        #print(meta)
        if(isinstance(meta,list)):
            index_list.append('_'.join(meta))
        else:
            index_list.append(meta)
    signal_list = []
    signal = ''
    for i in range(len(index_list)):
        if(i == (len(index_list)-1)):
            signal += index_list[i]
            signal_list.append(signal)
        elif(index_list[i] not in signal_type):
            if(index_list[i+1] not in signal_type):
                signal += index_list[i]+'#'
            else:
                signal += index_list[i]+'&'
        else:
            if(index_list[i+1] not in signal_type):
                signal += index_list[i]
                signal_list.append(signal)
                signal = ''
            else:
                signal += index_list[i]+'&'
    return signal_list

def get_str_list(expression):
    str_list = []
    for x in expression:
        if(x== '*' or x == '+'):
            str_list.append(x)
    return str_list

def get_new_expre(expression,max_k):
    signal_list  = re.split(r'[*+]',expression)
    str_list = get_str_list(expression)
    s_expre = split_expre(signal_list)
    new_s_expre = copy.copy(s_expre)
    new_expre_list = []
    for i in range(len(s_expre)):
        if(isinstance(s_expre[i],list) and len(s_expre[i])>1):
            for j in range(len(s_expre[i])):
                if(s_expre[i][j].isdigit()):
                    the_s = copy.copy(int(s_expre[i][j]))
                    #print(the_s)
                    for k in range(2,max_k):
                        new_s_expre[i][j] = copy.copy(str(the_s*k))
                        #print(new_s_expre)
                        new_expre_list.append(compose_expre(new_s_expre))
                    new_s_expre[i][j] = copy.copy(str(the_s))
    if(new_expre_list == []):
        new_expre_list.append(compose_expre(new_s_expre))
    result = []
    for expre_list in new_expre_list:
        expre_0 = copy.copy(expre_list[0])
        for i in range(len(str_list)):
            expre_0 += str_list[i] + expre_list[i+1]
        result.append(expre_0)
    return result

def lists_combination(lists, code=''):
    try:
        import reduce
    except:
        from functools import reduce
        
    def myfunc(list1, list2):
        return [[i,j] for i in list1 for j in list2]
    return reduce(myfunc, lists)

def get_new_expre_list(expression):
    new_expression_list = []
    for sub_expre in expression:
        new_sub_expre = get_new_expre(sub_expre,max_k = 3)
        new_expression_list.append(new_sub_expre)
    return lists_combination(new_expression_list)