#!/usr/bin/python
# coding=utf-8

import pandas as pd

# 从CSV文件加载数据
data = pd.read_excel("d:\\1\\detail.xlsx")

# 用for循环逐行计算
for index, row in df.iterrows():
    selected_data = row[1:5]  # 选择第二列至第五列的数据
    selected_data = selected_data.drop(selected_data.idxmax())  # 剔除最高值
    average = selected_data.mean()  # 计算平均值
    print(f"第{index+1}行剔除最高值后的平均值：{average}")



  