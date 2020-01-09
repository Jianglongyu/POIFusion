# -*- coding: utf-8 -*-
"""
@Time    : 2019/2/22 14:36
@Author  : Joy
片面最近邻算法
"""

import math
from TxCosine import Cosine
import datetime

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

def delFusionRecrd(delW,ws):#从集合中删除一个集合的数据
    for dw in delW:
     if dw in ws.values():
        keyT = list(ws.keys())[list(ws.values()).index(dw)]
        ws.pop(keyT)
    return ws

def delSingleRecrd(delW,ws):#从集合中删除一条数据
    for dw in list(ws.values()):
     if dw == delW:
        keyT = list(ws.keys())[list(ws.values()).index(dw)]
        ws.pop(keyT)
        break
    return ws

def getIndexByValue(delW,ws):
    keyT = list(ws.keys())[list(ws.values()).index(delW)]
    return keyT

thresVal1 = 0.4
thresVal2 = 0.8

rateT = [0.2, 0.4, 0.6, 0.8, 1.0]
sample_rate = 0.7

import csv
csv_path = 'data/fusion_data/' + str(sample_rate) + '/bw_map/data_excel/' + 'pnn_data.csv'

with open(csv_path , 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['overlapping degree', 'precision', 'recall', 'f1', 'time'])
    for rate in rateT:
        #首先读取各自数据集
        path = 'data/fusion_data/'+ str(sample_rate) + '/bw_map/dealData/'
        bwDataPath = path + "ve_" + str(rate) + "bw_" + str(sample_rate) + ".txt"
        mapDataPath = path + "ve_" + str(rate) + "mappoi_" + str(sample_rate) + ".txt"
        
        starttime = datetime.datetime.now()
        fp = open(path + "posinx_" + str(rate) + ".txt",'rb')
        poslines = fp.readlines()

        fbw = open(bwDataPath,'r')
        fmap = open(mapDataPath,'r')

        bwLines = fbw.readlines()
        maplines = fmap.readlines()



        ws = {}
        bs = {}
        oriWs = {}
        oriBs = {}
        fs = []

        fusionResultOri = []

        addFlag = 0
        #记录各自数据集 并得到片面最近邻融合结果集
        for bwl in bwLines:
            # bwl = bwl.decode('utf-8')
            a = bwl.split(",")
            aname = a[0]
            alon = float(a[1])
            alat = float(a[2])
            index = a[14].split("\n")[0]
            bs[index] = aname
            oriBs[index] = aname

            disT = 10000000
            ab = (aname,"error")
            for mapl in maplines:
                # mapl = mapl.decode('utf-8')
                b = mapl.split(",")
                bname = b[0]
                blon = float(b[1])
                blat = float(b[2])

                if addFlag == 0:
                    indexb = b[14].split("\n")[0]
                    ws[indexb] = bname
                    oriWs[indexb] = bname

                dis = calDistance(alon,alat,blon,blat)

                if dis < disT:
                    disT = dis
                    minName = bname
                    ab = (aname, bname)

            fusionResultOri.append(ab)
            addFlag = 1


        #初次过滤函数  对融合结果集进行计算余弦相似度 并获得不同数据的单集
        delW = []
        delB = []
        for eachab in fusionResultOri:
            name1 = eachab[0]
            name2 = eachab[1]

            a = Cosine(name1,name2)
            val = a.calCosine()
            if (val > thresVal1):#如果大于阈值  则从单集中删除此条记录 并将该条记录加入融合结果集中
                delB.append(name1)
                delW.append(name2)

                ab = (name1,name2)
                fs.append(ab)

        #得到删除记录的单集
        ws = delFusionRecrd(delW,ws)
        bs = delFusionRecrd(delB,bs)

        #第二次过滤删除函数
        for db in list(bs.values()):
            for dw in list(ws.values()):
                b = Cosine(db,dw)
                val1 = b.calCosine()
                if(val1 > thresVal2):#if val bigger than high threshold, then add in fusion record
                    tMap = (db,dw)
                    fs.append(tMap)
                    #从单集中删除
                    ws = delSingleRecrd(dw,ws)
                    bs = delSingleRecrd(db,bs)
                    break

        finalRes = []
        #根据融合数据集得到index数据 并进行精确率 召回率 F1计算
        for items in fs:
            it1 = items[0]
            it2 = items[1]
            inx1 = getIndexByValue(it1,oriBs).split("\r")[0]
            inx2 = getIndexByValue(it2,oriWs).split("\r")[0]
            strT = inx1 + "," + inx2
            finalRes.append(strT)

        pos = []
        # fp = open("\\\Mac\\Home\\Desktop\\0108_text_cluster\\data\\data0129\\"+ str(rate) + "positiveInx" +".txt",'r')
        # poslines = fp.readlines()
        for eachl in poslines:
            eachl = eachl.decode('utf-8')
            eachl = eachl.split(",")
            a = eachl[0] + "," + eachl[1].split("\r")[0]
            pos.append(a)

        pset = set(pos)
        rset = set(finalRes)
        final = pset & rset

        precison = len(final) / len(rset) * 1.0
        recall = len(final) * 1.0 / (len(poslines) - 1)
        f1 = (2 * precison * recall) / (precison + recall)

        print(str(rate),len(final),len(finalRes),round(precison,4),round(recall,4),round(f1,4))
        endtime = datetime.datetime.now()
        print((endtime - starttime).seconds)
        cost_time = (endtime - starttime).seconds
        record_data = [rate, round(precison,4), round(recall,4), round(f1,4), cost_time]
        csv_writer.writerow(record_data)

