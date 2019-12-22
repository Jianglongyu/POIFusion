# -*- coding: utf-8 -*-
"""
@Time    : 2019/1/16 21:03
@Author  : Joy
测试余弦相似度

"""
import jieba
import math

class Cosine(object):
    def __init__(self,s1,s2):
        self.s1 = s1
        self.s2 = s2

    def calCosine(self):
        s1_cut = [i for i in jieba.cut(self.s1, cut_all=True) if i != '']
        s2_cut = [i for i in jieba.cut(self.s2, cut_all=True) if i != '']
        word_set = set(s1_cut).union(set(s2_cut))
        word_dict = dict()
        i = 0
        for word in word_set:
            word_dict[word] = i
            i += 1
        # print(word_dict)

        s1_cut_code = [word_dict[word] for word in s1_cut]
        # print(s1_cut_code)
        s1_cut_code = [0]*len(word_dict)

        for word in s1_cut:
            s1_cut_code[word_dict[word]]+=1
        # print(s1_cut_code)

        s2_cut_code = [word_dict[word] for word in s2_cut]
        # print(s2_cut_code)
        s2_cut_code = [0]*len(word_dict)
        for word in s2_cut:
            s2_cut_code[word_dict[word]]+=1
        # print(s2_cut_code)

        # 计算余弦相似度
        sum = 0
        sq1 = 0
        sq2 = 0
        for i in range(len(s1_cut_code)):
            sum += s1_cut_code[i] * s2_cut_code[i]
            sq1 += pow(s1_cut_code[i], 2)
            sq2 += pow(s2_cut_code[i], 2)

        try:
            result = round(float(sum) / (math.sqrt(sq1) * math.sqrt(sq2)), 2)
        except ZeroDivisionError:
            result = 0.0

        # print(result)
        return result