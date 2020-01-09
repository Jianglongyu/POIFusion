# POIFusion

#### Description
{**This is the code of POI Fusion, which contains the code of each comparison algorithm (OSN-POI/MNN-POI/PRN-POI/NW-POI) and the experimental data.**}

#### Installation

1.  jieba
2.  jaro_py3

#### Instructions
1.  python nearestPM.py   #Test OSN-POI method
2.  python mutualNearest.py  #Test MNN-POI method
3.  python probability.py    #Test PRN-POI method
4.  python improbability.py   #Test NW-POI method
5.  python dbscanClustering.py  #Test MHCM-POI method
6.  python Cal_evaluation_index.py #Calculate the evaluation index of MHCM-POI method
7.  The test data is in "data\". "data\distance_cluster_data" is the result of DBSCAN distance clustering, which is used in dbscanclustering.py program.


