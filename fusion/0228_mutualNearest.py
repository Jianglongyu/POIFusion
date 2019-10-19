# -*- coding: utf-8 -*-
"""
@Time    : 2019/2/22 14:36
@Author  : Joy
相互最近邻算法
"""
import tqdm
import math
from TxCosine import Cosine
import datetime
import numpy as np
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

def getDistanceByInx(inxb,inxw,bwlines,maplines):
    bwl = bwlines[inxb]
    bwl = bwl.decode('utf-8')
    a = bwl.split(",")
    alon = float(a[1])
    alat = float(a[2])

    mapl = maplines[inxw]
    mapl = mapl.decode('utf-8')
    b = mapl.split(",")
    blon = float(b[1])
    blat = float(b[2])

    dis = calDistance(alon,alat,blon,blat)
    return dis

def getNameByInx(inxb,inxw,bwlines,maplines):
    bwl = bwlines[inxb]
    bwl = bwl.decode('utf-8')
    a = bwl.split(",")
    aname = a[0]

    mapl = maplines[inxw]
    mapl = mapl.decode('utf-8')
    b = mapl.split(",")
    bname = b[0]
    name = (aname,bname)
    return name




thresVal1 = 0.4
thresVal2 = 0.8
INDEXTAG = 14

rateT = [0.2, 0.4, 0.6, 0.8, 1.0]

import csv
csv_path = 'C:/Users/Administrator/Desktop/Taks/1018_newFusion/data/fusion_data/0.7/bw_map/data_excel/' + 'mnn_data.csv'
with open(csv_path, 'w') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['重合度', 'precision', 'recall', 'f1', 'time'])
    
    for rate in rateT:
        #首先读取各自数据集
        path = "C:/Users/Administrator/Desktop/Taks/1018_newFusion/data/fusion_data/0.7/bw_map/dealData/"
        bwDataPath = path + "ve_" + str(rate) + "building_0.7" + ".txt"
        mapDataPath = path + "ve_" + str(rate) + "mappoi_0.7" + ".txt"

        starttime = datetime.datetime.now()
        # fp = open(path + str(rate) + "positiveInx" + ".txt",'rb')
        fp = open(path+ "posinx_" + str(rate)  + ".txt",'rb')
        poslines = fp.readlines()

        fbw = open(bwDataPath,'r')
        fmap = open(mapDataPath,'r')

        bwLines = fbw.readlines()
        maplines = fmap.readlines()
        blen = len(bwLines)
        wlen = len(maplines)


        ws = {}
        bs = {}
        oriWs = {}
        oriBs = {}
        fs = []

        fusionResultOri = []

        bMatrix = np.zeros(shape=(blen,2))
        wMatrix = np.zeros(shape=(wlen,2))

        addFlag = 0
        #记录各自数据集 并得到片面最近邻融合结果集
        # for bwl in bwLines:
        for bwinx in range(len(bwLines)):
            bwl = bwLines[bwinx]
            # bwl = bwl.decode('utf-8')
            a = bwl.split(",")
            aname = a[0]
            alon = float(a[1])
            alat = float(a[2])
            index = a[INDEXTAG].split("\n")[0]
            bs[index] = aname
            oriBs[index] = aname

            bMatrix[bwinx][0] = -1
            bMatrix[bwinx][1] = -1

            disT = 10000000

            for mapinx in range(len(maplines)):
                dis = getDistanceByInx(bwinx,mapinx,bwLines,maplines)

                if dis < disT:
                    disT = dis
                    bMatrix[bwinx][1] = bMatrix[bwinx][0]
                    bMatrix[bwinx][0] = mapinx

        for mapinx in range(len(maplines)):
            mapl = maplines[mapinx]
            # mapl = mapl.decode('utf-8')
            b = mapl.split(",")
            bname = b[0]
            blon = float(b[1])
            blat = float(b[2])
            indexb = b[INDEXTAG].split("\n")[0]
            ws[indexb] = bname
            oriWs[indexb] = bname

            wMatrix[mapinx][0] = -1
            wMatrix[mapinx][1] = -1

            disT = 10000000

            for bwinx in range(len(bwLines)):
                dis = getDistanceByInx(mapinx,bwinx,maplines,bwLines)

                if dis < disT:
                    disT = dis
                    wMatrix[mapinx][1] = wMatrix[mapinx][0]
                    wMatrix[mapinx][0] = bwinx


        #根据得到的矩阵计算置信度 得到最后fusuionResult集合
        for bwinx in range(len(bwLines)):
            mapinx0 = int(bMatrix[bwinx][0])
            mapinx1 = int(bMatrix[bwinx][1])

            if(int(wMatrix[mapinx0][0]) == bwinx):
                bwinx1 = int(wMatrix[mapinx0][1])
                disAB = getDistanceByInx(bwinx,mapinx0,bwLines,maplines)
                disMin2 = getDistanceByInx(bwinx1,mapinx0,bwLines,maplines)
                disMin1 = getDistanceByInx(bwinx,mapinx1,bwLines,maplines)
                disMin = disMin1
                if disMin1 > disMin2:
                    disMin = disMin2

                confidenceV = 1 - ((disAB * 1.0) / disMin)
                if(confidenceV > 0):
                    name = getNameByInx(bwinx,mapinx0,bwLines,maplines)
                    fusionResultOri.append(name)


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
            # strT = inx2 + "," + inx1
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

        precison = len(final) / (len(rset)) * 1.0
        recall = len(final) * 1.0 / len(poslines)
        f1 = (2 * precison * recall) / (precison + recall)


        print(str(rate),len(final),len(finalRes),round(precison,4),round(recall,4),round(f1,4))
        endtime = datetime.datetime.now()
        print((endtime - starttime).seconds)
        cost_time = (endtime - starttime).seconds
        record_data = [rate, round(precison,4), round(recall,4), round(f1,4), cost_time]
        csv_writer.writerow(record_data)
