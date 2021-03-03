# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 08:47:18 2021

@author: LiaoBin
"""


# 使用KMeans进行聚类
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np

# 数据加载
data = pd.read_csv('car_data.csv', encoding='gbk')
# 建立训练集
train_x = data[["人均GDP","城镇人口比重","交通工具消费价格指数", "百户拥有汽车量"]]

# 规范化到 [0,1] 空间
min_max_scaler=preprocessing.MinMaxScaler()
train_x=min_max_scaler.fit_transform(train_x)
pd.DataFrame(train_x).to_csv('temp.csv', index=False)

# 使用KMeans聚类,分成4类
kmeans = KMeans(n_clusters=4)
kmeans.fit(train_x)  # 也可以直接fit+predict
predict_y = kmeans.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
# 将结果列重命名为'聚类结果'
result.rename({0:u'聚类结果'},axis=1,inplace=True)
# 将结果导出到CSV文件中
result.to_csv("car_data_cluster_result.csv",index=False)

