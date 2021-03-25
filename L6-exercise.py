# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 14:43:31 2021

@author: LiaoBin
"""


import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARMA
from itertools import product
import numpy as np
import pandas as pd

# 用ARMA进行时间序列预测
# 导入数据
train = pd.read_csv('train.csv')
# datatime转化为pandas中格式
train['Datetime'] = pd.to_datetime(train['Datetime'], format='%d-%m-%Y %H:%M')
# 将Datetime作为新索引
train.index = train['Datetime']
# 去掉ID,Datetime字段
train.drop(['ID', 'Datetime'], axis=1, inplace=True)
# 按照天进行采样
daily_train = train.resample('D').sum()
# daily_train作图
plt.figure(figsize=(30, 8))
# 显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.plot(daily_train['Count'], '-', label='按天')
plt.legend()
plt.show()

# 设置参数范围
ps = range(0, 3)
qs = range(0, 3)
parameters = product(ps, qs)
parameters_list = list(parameters)
# 寻找最优ARMA模型参数，即best_aic最小
result = []
best_aic = float('inf')  # 正无穷
for param in parameters_list:
    try:
        model = ARMA(daily_train.Count, order=(param[0], param[1])).fit()
    except ValueError:
        print('参数错误：', param)
        continue
    aic = model.aic
    if aic < best_aic:
        best_model = model
        best_aic = aic
        best_param = param
    result.append([param, model.aic])
# 输出最佳模型
print('最优模型：', best_model.summary())

# 设置futrue_day，需要预测的时间date_list
daily_train2 = daily_train['Count']
future_day = 213
last_day = pd.to_datetime(daily_train2.index[len(daily_train2)-1])
date_list = pd.date_range('2014-09-26', periods=future_day, freq='D')
# 添加未来要预测的7个月即213天
future = pd.DataFrame(index=date_list, columns=daily_train.columns)
print(len(daily_train2))
daily_train2 = pd.concat([daily_train2, future])
# 历史所有时间+未来七月预测，赋值到forecast字段
daily_train2['forecast'] = best_model.predict(start=0, end=len(daily_train2))
daily_train2['forecast'][0] = np.NaN
# 交通流量预测结果显示
plt.figure(figsize=(30, 8))
daily_train2.forecast.plot(color='r',ls='--',label='预测流量')
plt.legend()
plt.title('交通流量预测')
plt.xlabel('日期')
plt.ylabel('流量')
plt.show()

