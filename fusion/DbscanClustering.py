# -*- coding: utf-8 -*-
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from glob import glob
import time
import csv
import datetime

import sys
sys.path.append('../')

class DbscanClustering():
    def __init__(self, stopwords_path=None):
        self.stopwords = self.load_stopwords(stopwords_path)
        self.vectorizer = CountVectorizer(analyzer='word',token_pattern=u"(?u)\\b\\w+\\b")
        self.transformer = TfidfTransformer()

    def load_stopwords(self, stopwords=None):
        """
        load stopwords
        :param stopwords:
        """
        if stopwords:
            with open(stopwords, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f]
        else:
            return []

    def preprocess_data(self, corpus_path):
        """
        preprocess text data
        """
        corpus = []
        with open(corpus_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split(",")[0]
                if line.find("name") != -1:
                    continue
                # corpus.append(line)
                corpus.append(' '.join([word for word in jieba.lcut(line.strip()) if word not in self.stopwords]))
        return corpus

    def get_text_tfidf_matrix(self, corpus):
        tfidf = self.transformer.fit_transform(self.vectorizer.fit_transform(corpus))
        weights = tfidf.toarray()
        return weights

    def pca(self, weights, n_components=2):
        pca = PCA(n_components=n_components)
        return pca.fit_transform(weights)

    def dbscan(self, corpus_path, eps=0.1, min_samples=3, fig=True):
        """
        text cluster algorithm
        """
        corpus = self.preprocess_data(corpus_path)

        weights = self.get_text_tfidf_matrix(corpus)

        clf = DBSCAN(eps=eps, min_samples=min_samples)

        y = clf.fit_predict(weights)

        # to get the final result cluster
        result = {}
        for text_idx, label_idx in enumerate(y):
            if label_idx not in result:
                result[label_idx] = [text_idx]
            else:
                result[label_idx].append(text_idx)
        return result


if __name__ == '__main__':
    rate_num = [0.2, 0.4, 0.6, 0.8, 1.0] # overlapping degree
    sample_rateT = 1.0
    csv_path = "data/fusion_data/" + str(sample_rateT) + "/bw_map/data_excel_ws/" + "mhcm.csv"

    dbscan = DbscanClustering(stopwords_path='tfidf_data/stop_words.txt')
    with open(csv_path, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['overlapping degree', 'precision', 'recall', 'f1', 'time'])
        for rate in rate_num:
            fw = open("data/res_data/" + str(sample_rateT) + "/result_data/" + "resultInx_" + str(rate) + ".txt","w",encoding='utf-8')
            start = datetime.datetime.now()
            path = "data/distance_cluster_data/"  + str(sample_rateT) + "/dis_fusion_" + str(rate) + "/100_2/" + "*.txt"
            directory = glob(path)
            lastF = directory[len(directory) - 1]
            finalRes = []
            count = 0
            for f in directory:
              result = dbscan.dbscan(f, eps=0.4, min_samples=2)
              fr = open(f,'rb')
              alline = fr.readlines()
              for fInx in result:
                if fInx != -1:
                    strPr = ""
                    res = result[fInx]
                    for rInx in res:
                        eachl = alline[rInx + 1]
                        eachl = eachl.decode('utf-8')
                        lenth = len(eachl.split(","))
                        a = eachl.split(",")[lenth - 1].split("\r")[0]
                        if len(a) < 1:
                            print(res)
                        else:
                            strPr = strPr + "," + str(a)

                    strPr = strPr.split(",")
                    a = strPr[1] + "," + strPr[2].split("\r")[0]
                    finalRes.append(a)  # get cluster positive data
                    fw.write(a + "\n")
    
    
