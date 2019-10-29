# -*- coding: utf-8 -*-
__author__ = 'joy'
#  sample data from origin data
#  the rate is respectively 0.3 0.5 0.7

import random
import os
from glob import glob

def get_file_from_path(path):
    dirfiles = glob(path + "//" + "*.txt")
    return dirfiles

def make_sample_file_from_rate(file, rate):
    fr = open(file, 'r', encoding='utf-8')
    alllines = fr.readlines()
    lenth = len(alllines)
    read_count = (int)(lenth * rate)
    inx_list = sorted(random.sample(range(0,lenth), read_count))
    #  make new file
    new_file_dir = "C:/Users/Administrator/Desktop/Taks/1018_newFusion/data/sample_data/"
    new_file_name = os.path.basename(file).split(".")[0] + "_" + str(rate)
    new_file = new_file_dir + new_file_name + ".txt"
    fw = open(new_file, 'w', encoding='utf-8')
    for inx in inx_list:
        fw.write(alllines[inx])



if __name__ == "__main__":
    dirfiles = get_file_from_path("C:/Users/Administrator/Desktop/Taks/1018_newFusion/data/raw_origin_data")
    rate = [0.6]
    for df in dirfiles:
        for rval in rate:
            make_sample_file_from_rate(df, rval)
