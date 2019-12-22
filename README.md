# POIFusion

#### 介绍
{这个是POI Fusion的代码，其中包含各个对比算法的代码(OSN-POI/MNN-POI/PRN-POI/NW-POI)以及实验数据。}


#### 安装教程

1.  jieba
2.  jaro_py3

#### 使用说明

1.  python nearestPM.py
2.  python mutualNearest.py
3.  python probability.py
4.  python improbability.py
5.  python dbscanClustering.py
6.  测试数据在data文件夹下，distance_cluster_data是dbscan距离聚类后的结果，用于dbscanClustering.py程序，fusion_data用于剩下的算法。
7.  输出文件在data\fusion_data\1.0\bw_map\data_excel下。