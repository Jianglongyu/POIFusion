# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/1 10:34
@Author  : Joy
概率法
"""

from numpy import *
import numpy as np
import math
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
def delFusionRecrd(delW,ws):
    for dw in delW:
     if dw in ws.values():
        keyT = list(ws.keys())[list(ws.values()).index(dw)]
        ws.pop(keyT)
    return ws
def getIndexByValue(delW,ws):
    keyT = list(ws.keys())[list(ws.values()).index(delW)]
    return keyT
def delSingleRecrd(delW,ws):#从集合中删除一条数据
    for dw in list(ws.values()):
     if dw == delW:
        keyT = list(ws.keys())[list(ws.values()).index(dw)]
        ws.pop(keyT)
        break
    return ws
def calProbability(bD,wD):
    lon1 = bD.lon
    lat1 = bD.lat
    lon2 = wD.lon
    lat2 = wD.lat
    dis = calDistance(lon1,lat1,lon2,lat2)
    finDis = 0
    if dis <= 100:#如果超过距离值 则概率值为0
        finDis = math.pow(dis, -2) #这里参数是为2
    return finDis


def calMatrixProbability(bkList,chkList):#返回计算后的概率矩阵
    bkLen = len(bkList)
    chkLen = len(chkList)
    count = 0
    bkMatrix = np.zeros(shape=(bkLen,chkLen))

    for inx in range(bkLen):
        disSum = 0
        for jinx in range(chkLen):
             disSum = disSum + calProbability(bkList[inx],chkList[jinx])

        for kinx in range(chkLen):
            disAB = calProbability(bkList[inx],chkList[kinx])
            prbVal = disAB * 1.0 / (disSum)
            bkMatrix[inx][kinx] = prbVal
            if prbVal > 0:
                count = count + 1
    # print(count)
    return bkMatrix
def calFinalRCMatrix(bkList,chkList,row,col,tmpMatrix):
    bkLen = len(bkList)
    chkLen = len(chkList)

    rcAdd = np.zeros(shape=(row,col))
    disMultiple = 1
    for inx in range(bkLen):
         for jinx in range(chkLen):
             pab = tmpMatrix[jinx][inx]
             disMultiple =  disMultiple * (1 - pab)

         val = disMultiple

         r = 0
         c = 0
         if row == 1:
             r = 0
             c = inx
         else:
             r = inx
             c = 0

         rcAdd[r][c] = val

    return rcAdd


INDEX_TAG = 14
locationVal = 0.5
thresVal1 = 0.3
thresVal2 = 0.9

rateT = [0.2, 0.4, 0.6, 0.8, 1.0]

import csv
csv_path = 'C:/Users/Administrator/Desktop/Taks/1018_newFusion/data/fusion_data/0.7/bw_map/data_excel/' + 'pnn_data.csv'
with open(csv_path, 'w') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['重合度', 'precision', 'recall', 'f1', 'time'])
    
    for rate in rateT:
        starttime = datetime.datetime.now()
        #先读取数据
        path = "C:/Users/Administrator/Desktop/Taks/1018_newFusion/data/fusion_data/0.7/bw_map/dealData/"
        bwDataPath = path + "ve_" + str(rate) + "building_0.7" + ".txt"
        mapDataPath = path + "ve_" + str(rate) + "mappoi_0.7" + ".txt"

        fbw = open(bwDataPath,'r')
        fmap = open(chkDataPath,'r')


        fp = open(path + "posinx_" + str(rate) + ".txt",'rb')
        poslines = fp.readlines()

        bwLines = fbw.readlines()
        chklines = fmap.readlines()

        bList = []
        chkList = []

        ws = {}
        bs = {}
        oriWs = {}
        oriBs = {}
        fusionResultOri = [] #最近邻融合结果集
        fs = []
        #读入单集

        for bwl in bwLines:
            # bwl = bwl.decode('utf-8')
            a = bwl.split(",")
            aname = a[0]
            alon = float(a[1])
            alat = float(a[2])
            index = a[INDEX_TAG].split("\n")[0]
            bs[index] = aname
            oriBs[index] = aname

            a = Cosine(name1,name2)
            aObj = ChkData(aname,alon,alat,index)
            bList.append(aObj)

        for mapl in chklines:
            # mapl = mapl.decode('utf-8')
            b = mapl.split(",")
            bname = b[0]
            blon = float(b[1])
            blat = float(b[2])
            indexb = b[INDEX_TAG].split("\n")[0]
            ws[indexb] = bname
            oriWs[indexb] = bname

            bObj = ChkData(bname,blon,blat,indexb)
            chkList.append(bObj)

        #创建单集概率矩阵
        bkMatrix = calMatrixProbability(bList,chkList)
        chkMatrix = calMatrixProbability(chkList,bList)

        # print(bkMatrix.shape)
        #开始计算匹配矩阵M
        rowVal = bkMatrix.shape[0]
        colVal = bkMatrix.shape[1]

        #二维矩阵行列遍历计算
        for row in range(rowVal):
            for col in range(colVal):
                bkMatrix[row][col] = math.sqrt(bkMatrix[row][col] * chkMatrix[col][row])

        #给矩阵先添加最后一行和最后一列 初始赋0值 之后再修改值
        rowAdd = calFinalRCMatrix(chkList,bList,1,len(chkList),bkMatrix)#最后一行添加  传入bkMatrix
        colAdd = calFinalRCMatrix(bList,chkList,len(bList) + 1,1,chkMatrix)#最后一列添加  传入chkMatrix
        #将矩阵连接
        bkMatrix = np.row_stack((bkMatrix,rowAdd))
        bkMatrix = np.column_stack((bkMatrix,colAdd))

        rowValNew = bkMatrix.shape[0]
        colValNew = bkMatrix.shape[1]

        #根据矩阵的结果得到融合结果集
        for inx in range(rowValNew - 1):
            for jinx in range(colValNew - 1):
                if(bkMatrix[inx][jinx] > locationVal):#论文中所给阈值
                    aname = bList[inx].name
                    bname = chkList[jinx].name
                    ab = (aname, bname)
                    fusionResultOri.append(ab)


        #接下来进行名称相似性计算
        #初次过滤函数  对融合结果集进行计算余弦相似度 并获得不同数据的单集
        delW = []
        delB = []
        for eachab in fusionResultOri:
            name1 = eachab[0]
            name2 = eachab[1]

            val = (name1,name2)
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
                val1 = jaro_my.metric_jaro_winkler(db,dw)
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
            # strT = inx2 + "," + inx1 #在两种数据源中 数字下标是反过来的
            finalRes.append(strT)

        pos = []
        for eachl in poslines:
            eachl = eachl.decode('utf-8')
            eachl = eachl.split(",")
            a = eachl[0] + "," + eachl[1].split("\r")[0]
            pos.append(a)

        pset = set(pos)
        rset = set(finalRes)
        final = pset & rset

        precison = len(final) / len(rset) * 1.0
        recall = len(final) * 1.0 / (len(poslines) - 1) * 1.0
        f1 = (2 * precison * recall) / (precison + recall)

        print((endtime - starttime).seconds)
        cost_time = (endtime - starttime).seconds
        record_data = [rate, round(precison,4), round(recall,4), round(f1,4), cost_time]
        csv_writer.writerow(record_data)

