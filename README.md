# POIFusion

#### 介绍
{这个是POI Fusion的代码，其中包含各个对比算法的代码(OSN-POI/MNN-POI/PRN-POI/NW-POI)以及实验数据。}


#### 安装教程

1.  jieba
2.  jaro_py3

#### 使用说明

1.  python nearestPM.py 测试OSN-POI方法
2.  python mutualNearest.py 测试MNN-POI方法
3.  python probability.py   测试PRN-POI方法
4.  python improbability.py 测试NW-POI方法
5.  python dbscanClustering.py  测试MHCM-POI方法
6.  python Cal_evaluation_index.py 计算MHCM-POI方法的评价指标
7.  测试数据在data文件夹下，distance_cluster_data是dbscan距离聚类后的结果，用于dbscanClustering.py程序。