# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 22:19:20 2021
# Action1：汽车投诉信息采集
@author: LiaoBin
"""

# 加载模块
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy
import time
# from sklearn.feature_extraction import DictVectorizer
# from sklearn.linear_model import LogisticRegression

# 获取网址内容
def get_page_content(request_url):
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url, headers=headers, timeout=10)
    time.sleep(1)
    content = html.text
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

# 解析页面内容
def analysis(soup):
    # 定义空的df
    df = pd.DataFrame(columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem',\
                               'datetime', 'status'])
    # 找出完整的投诉信息框
    temp = soup.find('div', class_='tslb_b')
    # 找出tr
    tr_list = temp.find_all('tr')
    for tr in tr_list:
        # 找出所有的td
        td_list = tr.find_all('td')
        # 如果长度为0，那么就是表头
        if len(td_list) >0:
            # 投诉编号，投诉品牌，投诉车系，投诉车型，问题简述，典型问题，投诉时间，投诉状态
            # 数据放入字典
            temp = {}
            temp['id'] = td_list[0].text
            temp['brand'] = td_list[1].text
            temp['car_model'] = td_list[2].text
            temp['type'] = td_list[3].text
            temp['desc'] = td_list[4].text
            temp['problem'] = td_list[5].text
            temp['datatime'] = td_list[6].text
            temp['status'] = td_list[7].text
            # 数据传入df
            # print(temp)
            df = df.append(temp, ignore_index=True)
    result = df
    return result

# 清洗数据，分析type
def analyze(type):
    year, engine, transmission, other = '', '', '', ''
    engine_list = ['1.2T', '1.4T', '1.5T', '1.5L', '2.0L', '2.4L', '200TSI', '330TSI',\
                   '2.5G', '1.6L', '1.5', '1.5TD', '2.0T', '2.5L', '280TGDi', '230TSI',\
                       '280TSI', '380TSI', '285', '20T']
    transmission_list = ['自动', '手动', 'DVT', 'CVT', 'AMT', 'DCT']
    for i in type:
        if type.index(i) == 0 and i[-1:] == '款':
            year = i[:-1]
            continue
        if i in transmission_list:
            transmission = i
            continue
        if i in engine_list:
            engine = i
            continue
        other = other + ' ' + i
    return year, engine, transmission, other

url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml'
# 获取网址内容
soup = get_page_content(url)
# 解析获得数据
result = analysis(soup)

# 对type列进行数据清洗
# 年份 type_year
result['type_year'] =''
result['type_engine'] = ''
result['type_transmission'] = ''
result['type_other'] = ''

# 分析type字段，拆分成多个字段
for i, row in result.iterrows():
    year, engine, transmission, other = analyze(row['type'].split(' '))
    result.loc[i,'type_year'] = year
    result.loc[i,'type_engine'] = engine
    result.loc[i,'type_transmission'] = transmission
    result.loc[i,'type_other'] = other

# 识别变速箱情况，发现空值不是nan值，无法自动填充
print(result['type_transmission'].value_counts())
# 使用数量最多自动变速箱的来填充nan值
result['type_transmission'] = result['type_transmission'].replace('','自动')
# 数据存入excel表格
result.to_excel('car_complain_exercise.xlsx',index=False)
