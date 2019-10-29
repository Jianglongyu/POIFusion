# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 15:03:27 2019

@author: Administrator
对两个清洗后的数据集加入彼此的验证数据后形成最终的融合数据集
"""
import sys
sys.path.append("C:/Users/Administrator/Desktop/Taks/1018_newFusion/mycode/POIFusion")
from fusion.TxCosine import Cosine
import os
import pandas as pd
import math


def calDistance(x,y,x1,y1):
    radLat1 = (x * math.pi) / 180.0
    radLat2 = (x1 * math.pi) / 180.0
    aR = radLat1 - radLat2

    disY1 = (y * math.pi) / 180.0
    disY2 = (y1 * math.pi) / 180.0
    bR = disY1 - disY2

    s = 2 * math.asin((math.sqrt(pow(math.sin(aR / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * pow(math.sin(bR / 2), 2))))
    s = s * 6378137

    return s

def read_data(fst_dt, snd_dt, rate, save_path):
    table_1 = pd.read_csv(fst_dt)
    table_2 = pd.read_csv(snd_dt)
    rows_1 = table_1.shape[0]
    rows_2 = table_2.shape[0]
    ve = round((rows_1 + rows_2) * rate / (2 - rate))
    v_1 = round(ve / (rows_1 / rows_2 + 1))
    v_2 = ve - v_1

    #在经度小数点第五位加2
    table_4 = pd.DataFrame()
    table_4 = table_4.drop(table_4.index)
    table_4 = table_4.append(table_1,ignore_index=True)
    table_5 = pd.DataFrame()
    table_5 = table_5.drop(table_5.index)
    table_5 = table_5.append(table_2,ignore_index=True)
    table_4['latitude'] = table_4['latitude'] + 0.0002#微博
    table_5['latitude'] = table_5['latitude'] + 0.0002#楼盘
    # 加入验证数据
    ve_fst = pd.DataFrame()
    ve_fst = ve_fst.drop(ve_fst.index)
    ve_fst = ve_fst.append(table_1, ignore_index=True)
    ve_fst = ve_fst.append(table_5[0:v_1], ignore_index=True)
    ve_snd = pd.DataFrame()
    ve_snd = ve_snd.drop(ve_snd.index)
    ve_snd = ve_snd.append(table_2, ignore_index=True)
    ve_snd = ve_snd.append(table_4[0:v_2], ignore_index=True)

    save_file_1 = save_path + "ve_" + str(rate) + os.path.basename(fst_dt)
    save_file_2 = save_path + "ve_" + str(rate) + os.path.basename(snd_dt)
    
    columns = ['name','longitude','latitude','phone','address','district','city','area','zipcode','type','datatype','date','creator','source', 'index']
    ve_fst = ve_fst.reindex(columns=columns)
    ve_snd = ve_snd.reindex(columns=columns)

    ve_fst.to_csv(save_file_1, index=False)
    ve_snd.to_csv(save_file_2, index=False)
    print(v_1, v_2)
    return save_file_1, save_file_2, v_1, v_2

# generate fusion data and posinx data
def generate_fusion_data(dt1, dt2, v1, v2, rate):
    save_path = os.path.dirname(dt1)

    save_file = save_path + "/" + "fusion_" + str(rate) + ".txt"
    
    fw = open(save_file, 'w')

    inx = 1
    lines1 = open(dt1, 'rb').readlines()
    lines2 = open(dt2, 'rb').readlines()
    
    f1_new = open(dt1, 'w')
    f2_new = open(dt2, 'w')
    for eachl_1 in lines1:
        eachl_1 = eachl_1.decode('utf-8')
        if eachl_1.find("name") != -1:
            continue
        else:
            a = eachl_1.split(",")
            a[len(a) - 1] = str(inx)
            inx += 1
            new_line1 = ','.join(a)
        f1_new.write(new_line1 + "\n")
        fw.write(new_line1 + "\n")
    fst_lst_inx = inx - 1
    for eachl_2 in lines2:
        eachl_2 = eachl_2.decode('utf-8')
        if eachl_2.find("name") != -1:
            continue
        else:
            b = eachl_2.split(",")
            b[len(b) - 1] = str(inx)
            inx += 1
            new_line2 = ','.join(b)
        f2_new.write(new_line2 + "\n")
        fw.write(new_line2 + "\n")
    snd_lst_inx = inx - 1
    generate_posinx_data(v1, v2, fst_lst_inx, snd_lst_inx, rate, save_path)

#  generate posinx data from fusion data
def generate_posinx_data(v1, v2, fst_lst_inx, snd_lst_inx, rate, save_path):
    save_posinx = save_path + "/" + "posinx_" + str(rate) + ".txt"
    fpos = open(save_posinx, 'w')
    for i in range(1, v2 + 1):
        pos_str = str(i) + "," + str(snd_lst_inx - v2 + i)
        fpos.write(pos_str + "\n")
    for i in range(1, v1 + 1):
        pos_str = str(fst_lst_inx - v1 + i) + "," + str(fst_lst_inx + i)
        fpos.write(pos_str + "\n")

if __name__ == '__main__':
    file_path = 'C:/Users/Administrator/Desktop/Taks/1018_newFusion/data/fusion_data/0.6/b_w/dealData/'
    fst_dt = file_path + 'building_0.6.txt'
    snd_dt = file_path + 'weibo_0.6.txt'
    save_path = file_path
    rate_num = [0.2, 0.4, 0.6, 0.8, 1.0]
    for rate in rate_num:
        print(rate)
        f1, f2, v1, v2 = read_data(fst_dt, snd_dt, rate, save_path)
        generate_fusion_data(f1, f2, v1, v2, rate)
