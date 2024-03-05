#!/usr/bin/python
# coding=utf-8

import pandas as pd

# 从CSV文件加载数据
data = pd.read_excel("d:\\1\\detail.xlsx")
# 获取列名列表
column_names = data.columns.tolist()
for item in column_names:
    if item == "code":
        continue
    pe = data.loc[24, item]*data.loc[25, item] / data.loc[9, item]
    cash = data.loc[24, item] 
    # # cash = row[24]/(row[25]*row[26])
    # cash = data.loc[23, item]/ (data.loc[24, item]**data.loc[25, item])
    # ROE = data.loc[9, item]/data.loc[4, item] 
    # # ROE = row[10] / row[5]
    # # netprofileratio = row[10] / row[15]
    # netprofileratio = data.loc[9, item]/data.loc[14, item] 
    # # cashflow = row[20]
    # cashflow = data.loc[19, item]
    # # netprofile = row[10]
    # netprofile = data.loc[9, item]
    print(pe)



  