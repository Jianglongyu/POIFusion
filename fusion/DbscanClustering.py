# -*- coding: utf-8 -*-

import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from glob import glob
import datetime


class DbscanClustering():
    def __init__(self, stopwords_path=None):
        self.stopwords = self.load_stopwords(stopwords_path)
        self.vectorizer = CountVectorizer(analyzer='word',token_pattern=u"(?u)\\b\\w+\\b")#字加词
        # self.vectorizer = CountVectorizer()#词
        self.transformer = TfidfTransformer()

    def load_stopwords(self, stopwords=None):
        """
        加载停用词
        :param stopwords:
        :return:
        """
        if stopwords:
            with open(stopwords, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f]
        else:
            return []

    def preprocess_data(self, corpus_path):
        """
        文本预处理，每行一个文本
        :param corpus_path:
        :return:
        """
        corpus = []
        with open(corpus_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split(",")[0]
                if line.find("time") != -1:
                    continue
                corpus.append(' '.join([word for word in jieba.lcut(line.strip()) if word not in self.stopwords]))
                # corpus.append(' '.join([word for word in jieba.lcut(line.strip())]))
        return corpus

    def get_text_tfidf_matrix(self, corpus):
        """
        获取tfidf矩阵
        :param corpus:
        :return:
        """

        # corpus2 = list(set(corpus))
        # tfidf = self.transformer.fit_transform(self.vectorizer.fit_transform(corpus2))
        tfidf = self.transformer.fit_transform(self.vectorizer.fit_transform(corpus))

        # 获取词袋中所有词语
        # words = self.vectorizer.get_feature_names()

        # 获取tfidf矩阵中权重
        weights = tfidf.toarray()

        # for i in range(len(corpus)):
        #     X_count_test = self.vectorizer.transform(corpus[i])
        # weights1 = X_count_test.toarray()

        return weights

    def pca(self, weights, n_components=2):
        """
        PCA对数据进行降维
        :param weights:
        :param n_components:
        :return:
        """
        pca = PCA(n_components=n_components)
        return pca.fit_transform(weights)

    def dbscan(self, corpus_path, eps=0.1, min_samples=3, fig=True):
        """
        DBSCAN：基于密度的文本聚类算法
        :param corpus_path: 语料路径，每行一个文本
        :param eps: DBSCA中半径参数
        :param min_samples: DBSCAN中半径eps内最小样本数目
        :param fig: 是否对降维后的样本进行画图显示
        :return:
        """
        corpus = self.preprocess_data(corpus_path)

        weights = self.get_text_tfidf_matrix(corpus)


        # pca_weights = self.pca(weights)

        clf = DBSCAN(eps=eps, min_samples=min_samples)

        y = clf.fit_predict(weights)

        # if fig:
        #     plt.scatter(weights[:, 0], weights[:, 1], c=y)
        #     plt.show()

        # 中心点
        # centers = clf.cluster_centers_

        # 用来评估簇的个数是否合适,距离约小说明簇分得越好,选取临界点的簇的个数
        # score = clf.inertia_

        # 每个样本所属的簇
        result = {}
        for text_idx, label_idx in enumerate(y):
            if label_idx not in result:
                result[label_idx] = [text_idx]
            else:
                result[label_idx].append(text_idx)
        return result


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    dbscan = DbscanClustering(stopwords_path='../data/stop_words.txt')

    rate_num = [0.2, 0.4, 0.6, 0.8, 1.0]
    import csv
    csv_path = ''
    with open(csv_path, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['重合度', 'precision', 'recall', 'f1', 'time'])
        for rate in rate_num:
            fw = open("\\\Mac\\Home\\Desktop\\0108_text_cluster\\data\\data0128_bw\\resultData\\resultInx.txt","w",encoding='utf-8')
            path = "\\\Mac\\Home\\Desktop\\0108_text_cluster\\fusion.txt" + "\\50_2\\*.txt"
            directory = glob(path)
            lastF = directory[len(directory) - 1]
            finalRes = []
            count = 0
            for f in directory:
              result = dbscan.dbscan(f, eps=1.0, min_samples=2)
              fr = open(f,'rb')
              alline = fr.readlines()

              for fInx in result:
                   if fInx != -1:

                       strPr = ""
                       res = result[fInx]
                       for rInx in res:
                           eachl = alline[rInx + 1]#有name行需加1
                           eachl = eachl.decode('utf-8')
                           lenth = len(eachl.split(","))
                           a = eachl.split(",")[lenth - 1].split("\r")[0]
                           if len(a) < 1:
                               print(res)
                           else:
                               strPr = strPr + "," + str(a)

                       strPr = strPr.split(",")
                       a = strPr[1] + "," + strPr[2].split("\r")[0]
                       fw.write(a + "\n")
                       finalRes.append(a)

            pos = []
            fp = open("\\\Mac\\Home\\Desktop\\0108_text_cluster\\data\\data0129\\"+ str(rate) + "positiveInx" +".txt",'rb')
            poslines = fp.readlines()
            for eachl in poslines:
                eachl = eachl.decode('utf-8')
                eachl = eachl.split(",")
                a = eachl[0] + "," + eachl[1].split("\r")[0]
                pos.append(a)

            pset = set(pos)
            rset = set(finalRes)
            final = pset & rset


            precison = len(final) * 1.0 / len(rset)
            recall = len(final) / (len(poslines)) * 1.0
            f1 = (2 * precison * recall) / (precison + recall)

            print(rate,len(final),len(rset),round(precison,4),round(recall,4),round(f1,4))

            endtime = datetime.datetime.now()
            print ((endtime - starttime).seconds())
            cost_time = (endtime - starttime).seconds()
            record_data = [rate, round(precison,4), round(recall,4), round(f1,4), cost_time]
            csv_writer.writerow(record_data)
