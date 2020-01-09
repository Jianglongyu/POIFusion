
import time
import datetime
import csv

# Calculate the evaluation index of MHCM-POI method

rate_num = [0.2, 0.4, 0.6, 0.8, 1.0] # overlapping degree
sample_rateT = 1.0
for rate in rate_num:
    pos = []
    fp = open("data/fusion_data/"+ str(sample_rateT) + "/bw_map/dealData/" + "posinx_" +  str(rate) + ".txt",'rb') #read true positive data
    poslines = fp.readlines()
    for eachl in poslines:
        eachl = eachl.decode('utf-8')
        eachl = eachl.split(",")
        a = eachl[0] + "," + eachl[1].split("\r")[0]
        pos.append(a)
    
    finalRes = []
    fp1 = open("data/res_data/" + str(sample_rateT) + "/result_data/" + "resultInx_0.4_" +  str(rate) + ".txt",'rb') #read true positive data
    poslines1 = fp1.readlines()
    for eachl in poslines1:
        eachl = eachl.decode('utf-8')
        eachl = eachl.split(",")
        a = eachl[0] + "," + eachl[1].split("\r")[0]
        finalRes.append(a)
    
    pset = set(pos)
    rset = set(finalRes)
    final = pset & rset


    precison = len(final) * 1.0 / len(rset)
    recall = len(final) / (len(poslines)) * 1.0
    f1 = (2 * precison * recall) / (precison + recall)

    print(rate,len(final),len(rset),round(precison,4),round(recall,4),round(f1,4))
