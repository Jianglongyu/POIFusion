# -*- coding: utf-8 -*-
"""
@Time    : 2019/10/06 21:17
@Author  : Joy
计算相邻距离 将单源数据中存在相似的数据删除  因为验证数据会修改经纬度 所以距离会有变化  在做删除时应将这些距离差值加上
"""
import sys
sys.path.append("C:/Users/Administrator/Desktop/Taks/1018_newFusion/mycode/POIFusion")
from fusion.TxCosine import Cosine
import math
import os
from glob import glob
import importlib,sys
importlib.reload(sys)
# sys.setdefaultencoding('utf8')

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

def cleanData(allines, tag, is_save_draft_data=False, is_same=True):  #  single file to clean
    lenth = len(allines)
    inxRec = []
    dataRecA = []
    dataRecB = []
    for inx in range(lenth):
        eachl = allines[inx]
        eachl = eachl.decode('utf-8')
        s1 = eachl.split(",")[0]
        x1 = float(eachl.split(",")[1])
        y1 = float(eachl.split(",")[2])

        for jinx in range(inx + 1,len(allines)):
            nextl = allines[jinx]
            nextl = nextl.decode('utf-8')
            s2 = nextl.split(",")[0]
            x2 = float(nextl.split(",")[1])
            y2 = float(nextl.split(",")[2])

            dis = round(calDistance(x1,y1,x2,y2), 2)

            if(dis <= 120):
                a = Cosine(s1,s2)
                val = a.calCosine()
                if( val > 0.4):
                    print (val,inx,jinx,dis,s1,s2)
                    inxRec.append(jinx)
                    if dis < 50 and val > 0.7:
                        dataRecA.append(eachl)
                        dataRecB.append(nextl)
    if is_save_draft_data:
        save_verify_draft_data(dataRecA, dataRecB, tag, is_same)
    return inxRec

def clean_two_type_data(lines1, lines2): # clean two type data
    lenth1 = len(lines1)
    lenth2 = len(lines2)
    inxRec = []
    for inx in range(1, lenth1): # the line 1 is "name, longitude,.."
        eachl = lines1[inx]
        eachl = eachl.decode('utf-8')
        s1 = eachl.split(",")[0]
        x1 = float(eachl.split(",")[1])
        y1 = float(eachl.split(",")[2])
        for jinx in range(1, lenth2):
            nextl = lines2[jinx]
            nextl = nextl.decode('utf-8')
            s2 = nextl.split(",")[0]
            x2 = float(nextl.split(",")[1])
            y2 = float(nextl.split(",")[2])

            dis = round(calDistance(x1, y1, x2, y2), 2)

            if(dis <= 120):
                a = Cosine(s1, s2)
                val = a.calCosine()
                if(val > 0.4):
                    print(val, inx, jinx, dis, s1, s2)
                    inxRec.append(jinx)
    return inxRec

def save_verify_draft_data(a,b,tag, is_same=True):
    #  tag is represent which flag data, eg:weibo/building/map
    savepath = '///Mac//Home//Desktop//DailyTask//1006_NewFusion//data//verify_draft_data'
    if is_same:
        savepath = savepath + "//" + str(tag) + ".txt"
        fw = open(savepath, 'w')
        for ad, bd in zip(a, b):
            fw.write(ad)
            fw.write(bd)
        fw.close()
    else:
        savepath_a = savepath + "//" + str(tag) + "_a"  + ".txt"
        savepath_b = savepath + "//" + str(tag) + "_b"  + ".txt"
        fw_a = open(savepath_a, 'w')
        fw_b = open(savepath_b, 'w')
        for ad, bd in zip(a, b):
            fw_a.write(ad)
            fw_b.write(bd)
        fw_a.close()
        fw_b.close()

#  just clean one type data
def save_new_file(inxRec, allines, newFile):
    fw = open(newFile, 'w', encoding='utf-8')
    #  delete surplus data inx from inxRec
    for inx in range(len(allines) - 1):
        if inx not in inxRec:
            eachl = allines[inx].decode('utf-8')
            a = eachl.split("/r")[0].split("/n")[0]
            fw.write(a + "/n")
    fw.close()

def save_new_two_type_file(inxRec, allines, newFile):
    fw = open(newFile, 'w', encoding='utf-8')
    for inx in range(len(allines) - 1):
        if inx not in inxRec:
            eachl = allines[inx].decode('utf-8')
            a = eachl.split("\r")[0].split("\n")[0]
            fw.write(a + "\n")
    fw.close()

if __name__ == '__main__':
    type_num = 2
    if type_num == 1: # clean single data 
        dirpath = '///Mac//Home//Desktop//DailyTask//1006_NewFusion//data//sample_data_remain//' + "*.txt"
        directory = glob(dirpath)
        savepath = '///Mac//Home//Desktop//DailyTask//1006_NewFusion//data//clean_sample_data//'
        for filepath in directory:
            tag_name = os.path.basename(filepath)
            new_savepath = savepath + "clean_" + tag_name
            f = open(filepath,'rb')
            allines = f.readlines()
            inxRec = cleanData(allines, tag_name.split(".txt")[0])
            save_new_file(inxRec, allines, new_savepath)
    else: # clean two type data
        file_path = "C:/Users/Administrator/Desktop/Taks/1018_newFusion/data/fusion_data/0.7/bw_map/dealData/"
        save_path = file_path
        file1 = file_path + "building_0.7.txt"
        file2 = file_path + "clean_mappoi_0.7.txt"
        lines1 = open(file1, 'rb').readlines()
        lines2 = open(file2, 'rb').readlines()
        tag_name = os.path.basename(file2)
        new_savepath = save_path + "new_clean_" + tag_name
        inxRec = clean_two_type_data(lines1, lines2)
        save_new_two_type_file(inxRec, lines2, new_savepath)
        


    









