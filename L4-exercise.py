# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 20:18:05 2021

@author: LiaoBin
"""


import pandas as pd
from efficient_apriori import apriori


# 用pandas读取数据,存入dataset中
dataset = pd.read_csv('Market_Basket_Optimisation.csv', header=None)  # 不存入首行
# 遍历数据，去除NaN值
transactions = []
# 遍历数据列
for i in range(dataset.shape[0]):
    temp = []
    # 遍历数据行
    for j in range(20):
        if str(dataset[j][i]) != 'nan':  # type(dataset[j][i])发现是float
            temp.append(str(dataset[j][i]))
    transactions.append(temp)
# 挖掘频繁项集和频繁规则
itemsets, rules = apriori(transactions, min_support=0.04,  min_confidence=0.4)
print("频繁项集：", itemsets)
print("关联规则：", rules)

