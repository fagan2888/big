# -*- coding:UTF-8 -*-
import numpy as np
#import matplotlib.pyplot as plt
import pymongo
from Http_Post import http_post

def ATS(x,step=0):
    #step=5 #默认是0
    n=len(x)
    #print(n)
    #print(n)
    chpts=np.mat([[0,x[0]]])
    if(step==0):
        step=np.max([1,int(np.round(n/10))])
    #print(step)
    sp=0 #本来是1，但是python是从0开始的，所以改成了0
    x0=sp
    #print(np.r_[0:step+1],x[np.r_[1:(step+1)]])
    b=6*(np.sum(np.r_[0:step+1]*(x[1:(step+2)]))-x[0]*step*(step+1)/2)/(step*(step+1)*(2*step+1))
    ep=sp+step
    diff=x[ep]-x[sp]
    while(np.sign(diff)!=np.sign(b)):
        ep=ep-1
        if(ep<=0):  #本来是1，但是python是从0开始的，所以改成了0
            print("data constant in first step")
            return
        diff=x[ep]-x[sp]
    while(diff==0):   #不希望斜率为0，宁愿往后再挪一个
        ep=ep+1
        if(ep>=(n-1)):
            print("slope=0 and data constant after first step")
            return
        diff=x[ep]-x[sp]
    slope=(x[ep]-x[sp])/step
    cs=np.sign(slope)
    while(ep<n-1):
        #print("ep:",ep)
        spstart=sp
        while(np.sign(slope)==cs):
            ep=np.min([sp+step,n-1])
            if(sp==ep):
                break
            diff=x[ep]-x[sp]
            while(diff==0 and ep==sp+1):
                ep=ep-1
                diff=x[ep]-x[sp]
            if(diff==0):
                ep=np.min([sp+step,n-1])
                while(diff==0 and ep<n):
                    ep=ep+1
                    diff=x[ep]-x[sp]
            slope=diff/(ep-sp)
            sp=ep
        #print(spstart,sp,int(cs),np.multiply(x[spstart:sp],int(cs)),np.argmax(np.multiply(int(cs),x[spstart:sp])))
        sp=spstart+(np.argmax(np.multiply(int(cs),x[spstart:sp])))#R语言和python的a:b可能不一样
        #print("sp:",sp)
        new_chpts=[sp,x[sp]]
        chpts=np.row_stack((chpts,new_chpts))
        x0=sp
        cs=-cs
    if(chpts[chpts.shape[0]-1,0]!=n):
        new_chpts=[n-1,x[n-1]]
        chpts=np.row_stack((chpts,new_chpts))
    return(chpts)

class dailyBar:
    def __init__(self):
        self.strtime = ''
        self.close = 0
        self.high = 0
        self.open = 0
        self.low = 0
        self.s0 = 0  # 是否是变化点
        self.s1 = 0  # 是否是高点
        self.s2 = 0  # 是否是低点


def get_close(daily_bar):
    close = []
    for i in daily_bar:
        close.append(i.close)
    return close

def get_k1day_data(code, start, end, key):
    db = http_post(code, start, end)
    close = []
    for i in db:
        close.append(i.close)
    return close

def linear_B(code, start, end, h=3):
    db = http_post(code, start, end)
    close = get_close(db)
    chpt = ATS(close, h)
    print(len(close), len(chpt))
    if (chpt[0, 1] > chpt[1, 1]):  # 先算出第一个和第二个是低点还是高点
        db[0].s1 = 1
        db[1].s2 = 1
    else:
        db[0].s2 = 1
        db[1].s1 = 1
    for j in np.arange(chpt.shape[0]):  # 判断j的奇偶性，如果是奇数，和第二个的高低性一致，如果是偶数，和第二个的高低性一致
        if (j % 2 == 0):
            # print(j)
            chx = int(chpt[j, 0])
            # print(chx)
            db[chx].s0 = 1
            db[chx].s1 = db[0].s1
            db[chx].s2 = db[0].s2
        else:
            chx = int(chpt[j, 0])
            # print(chx)
            db[chx].s0 = 1
            db[chx].s1 = db[1].s1
            db[chx].s2 = db[1].s2
    '''
    plt.plot(chpt[:, 0], chpt[:, 1])
    # plt.show()
    # plt.close()

    plt.plot(close)
    plt.show()
    plt.close()
    '''
    return db

def up_down_point(db):
    chpt_up = np.mat([[0, 0]])
    chpt_low = np.mat([[0, 0]])
    chpt = np.mat([[0, 0]])
    close = []
    for i in np.arange(len(db)):
        close.append(db[i].close)
        # print(db[i].s0)
        if (db[i].s0 == 1):
            chpt = np.row_stack((chpt, [i, db[i].close]))

        if (db[i].s1 == 1):
            chpt_up = np.row_stack((chpt_up, [i, db[i].close]))
        if (db[i].s2 == 1):
            chpt_low = np.row_stack((chpt_low, [i, db[i].close]))
    print(len(chpt))
    '''
    plt.plot(chpt[1:, 0], chpt[1:, 1])
    # plt.show()
    # plt.close()

    plt.plot(chpt_low[1:, 0], chpt_low[1:, 1])
    # plt.show()
    # plt.close()

    plt.plot(chpt_up[1:, 0], chpt_up[1:, 1])
    plt.show()
    plt.close()

    plt.plot(close)
    plt.show()
    plt.close()
    '''
    return chpt_up, chpt_low, chpt, close

def cal_kb_value(k, b, point):
    x = point[0]
    y = point[1]
    return y - k * x - b


def cal_dist(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    return np.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def cal_max_verdis(x, y, k, b):
    verdis = np.fabs((k * x - y + b) / np.sqrt((pow(k, 2) + 1)))
    return np.max(verdis)

#计算有效的支撑线压力线

def cal_kb_list(pre, chpt, updown):  # 高点为1，低点为-1
    kb_list = np.mat([[0, 0, 0, 0]])  # 第一行的元素只用来初始化，没有实际用处
    for i in np.arange(2, chpt.shape[0]):
        # print("i:",i)
        x1, y1 = float(chpt[i - 1, 0]), float(chpt[i - 1, 1])
        # print("x1,y1:",x1,y1)
        for t in np.arange(i, chpt.shape[0]):
            # print("t:",t)
            flag = 0
            x2, y2 = float(chpt[t, 0]), float(chpt[t, 1])
            # print("x2,y2:",x2,y2)
            k = (y1 - y2) / (x1 - x2)  # 如果k=0会怎么样
            b = (y1 * x2 - x1 * y2) / (x2 - x1)
            # print(k,b)
            # print("k,b:",k,b)
            # if(x2+1<len(pre)):
            for j in np.arange(x1 + 1, len(pre)):  # 这里起始点x1还是x2还有问题
                # print("j:",j)
                j = int(j)
                mid_ = updown * (pre[j] - k * j - b)
                # print("mid_:",mid_)
                if (mid_ > 0):  # 压力线是小于0，支撑线是大于0
                    flag = 1
                    break
            # print("k,b:",k,b)
            if (flag == 0):
                # print(x2)
                kb_list = np.row_stack((kb_list, [int(x1), int(x2), k, b]))
    return kb_list

#计算交点和统计指标

def cal_new_point(kb_list, all_close, np_start, updown):
    new_breakpoint = np.mat([[0, 0, 0, 0, 0]])
    kblist = kb_list
    print(len(kb_list), len(all_close), np_start)
    for i in np.arange(np_start, len(all_close)):
        for j in np.arange(1, len(kb_list)):
            k = kb_list[j, 2]
            b = kb_list[j, 3]
            yi = all_close[i]
            mid_ = updown * (yi - k * i - b)
            # print("mid_:",mid_)
            if (mid_ > 0):  # 压力线是小于0，支撑线是大于0
                x1 = int(kb_list[j, 0])
                y1 = all_close[x1]
                dist = cal_dist([x1, y1], [i, yi])
                # print("k,b:",k,b)
                # print("x1,y1:",x1,y1)
                x_list = np.arange(x1, i)
                y_list = all_close[x1:int(i)]
                max_verdis = cal_max_verdis(x_list, y_list, k, b)
                area = dist * max_verdis
                # print(i,yi,dist,max_verdis,area)
                new_breakpoint = np.row_stack((new_breakpoint, [i, yi, dist, max_verdis, area]))
                kb_list = np.delete(kb_list, j, axis=0)
                # print(kb_list)
                break  # 这里要不要把突破的kb去掉
    return new_breakpoint

#返回的交点五个值分别是横坐标，纵坐标，与起点的距离，中间点到连线的最大距离，面积

def chpt_plot(all_close, kb_list):
    # all_close=get_close(daily_bars)
    print(len(all_close), len(kb_list))
    plt.plot(all_close)
    for i in np.arange(len(kb_list)):
        x1 = kb_list[i, 0]
        k = kb_list[i, 2]
        b = kb_list[i, 3]
        # print(x1)
        x = np.arange(x1, len(all_close))
        # print(x)
        y = k * x + b
        # if(i==3):
        plt.plot(x, y, lw=0.5)
    plt.ylim(np.min(all_close), np.max(all_close))
    # plt.xlim(0, 339)
    plt.show()
    plt.close()

def point_inf_to_dict(point_inf):
    db_dict = []
    for i in np.arange(len(point_inf)):
        _dict = {}
        _dict['x'] = point_inf[i,0]
        _dict['y'] = point_inf[i,1]
        _dict['dis_to_start'] = point_inf[i,2]
        _dict['dis_to_mid_max'] = point_inf[i,3]
        _dict['area'] = point_inf[i,4]
        db_dict.append(_dict)
    return db_dict

def linear_C(code, start, mid, end):
    h = 3
    db = linear_B(code, start, mid, h)
    chpt_up, chpt_low, chpt, close = up_down_point(db)

    # daily_bars = md.get_dailybars(code,start,end)
    # all_close=get_close(daily_bars)
    all_close = get_k1day_data(code, start, end, 'close')

    kb_list_up = cal_kb_list(close, chpt_up, 1)
    #chpt_plot(all_close, kb_list_up)

    new_point_up = cal_new_point(kb_list_up, all_close, len(close), 1)

    kb_list_low = cal_kb_list(close, chpt_low, -1)

    #chpt_plot(all_close, kb_list_low)
    # daily_bars = md.get_dailybars(code,start,end)
    # all_close=get_close(daily_bars)
    new_point_low = cal_new_point(kb_list_low, all_close, len(close), -1)

    return point_inf_to_dict(new_point_up), point_inf_to_dict(new_point_low)

#返回的交点五个值分别是横坐标，纵坐标，与起点的距离，中间点到连线的最大距离，面积
#up表示高点。low表示低点
if __name__== "__main__":
    code = '601001.SH'
    start = '2016-01-03'
    mid = '2017-01-11'
    end = '2018-01-11'
    # new_point=cal_new_point(kb_list,all_close,len(close),1)
    new_pointup, new_point_low = linear_C(code, start, mid, end)

    print(new_pointup, new_point_low)
    #print(point_inf_to_dict(new_pointup))
