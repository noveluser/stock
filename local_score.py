# coding=utf-8

'''
Created on 2024.1.15
获取特定股票的财务数据
@author: wangle
'''

import baostock as bs
import pandas as pd
import logging
import time
import datetime
from decimal import Decimal

# 定义日志输出格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="d:\\1\\getostock.log",
                    filemode='a')


def main():
    """ netasset_2019=5年前总营收  netprofit=净利润 totalShare=总股数 dupontNitogr=净利润/营业总收入 Netassets=净资产
    """
    df = pd.DataFrame()
    potential_growing = 0
    potential_cash = 0
    potential_pe = 0
    potentail_netprofileratio = 0
    potential_roe = 0
    potentail_cashflow = 0
    data = pd.read_excel("d:\\1\\detail.xlsx")
    # 获取列名列表
    column_names = data.columns.tolist()
    for item in column_names:
        if item == "code":
            continue
        code = item
        # pe = row[25]*row[26]/row[10]
        pe = data.loc[24, item]*data.loc[25, item] / data.loc[9, item]

        # cash = row[24]/(row[25]*row[26])
        cash = data.loc[23, item]/ (data.loc[24, item]*data.loc[25, item])
        ROE = data.loc[9, item]/data.loc[4, item] 
        # ROE = row[10] / row[5]
        # netprofileratio = row[10] / row[15]
        netprofileratio = data.loc[9, item]/data.loc[14, item] 
        # cashflow = row[20]
        cashflow = data.loc[19, item]
        # netprofile = row[10]
        netprofile = data.loc[9, item]

        # 计算净资产增长率，减去一个最高值，降低预期
        selected_data = data[code].iloc[0:5]
        growth_rate = selected_data.pct_change() * 100
        print(growth_rate)
        # 找到最高值
        max_value = growth_rate.max()
        # 去掉最高值
        filtered_growth_rate = growth_rate[growth_rate < max_value]
        # 计算剩余值的平均值
        potential_growing = filtered_growth_rate.mean()
        if potential_growing < 1:
             potential_growing = 0
        elif potential_growing < 5:
            potential_growing = 20
        elif potential_growing < 10:
            potential_growing = 30
        elif potential_growing < 15:
            potential_growing = 40
        else:
            potential_growing = 50           
        if pe < 0:
            potential_pe = 0
        elif pe < 10:
            potential_pe = 30
        elif pe < 15:
            potential_pe = 20
        elif pe < 25:
            potential_pe = 10
        else:
            potential_pe = 5
        if cash == 0:
            potential_cash = 0
        elif cash < 0.02:
            potential_cash = 5
        elif cash < 0.04:
            potential_cash = 10
        elif cash < 0.06:
            potential_cash = 15
        else:
            potential_cash = 20
        GDP = potential_growing + potential_cash + potential_pe

        # 计算利润率，5年内所有利润除以5年内营收
        # 计算1到5项的总和
        sum_1_to_5 = data[code].iloc[5:10].sum()
        # 计算6到10项的总和
        sum_6_to_10 = data[code].iloc[10:15].sum()
        # 计算总和的比值
        netprofileratio = sum_1_to_5 / sum_6_to_10
        if netprofileratio < 0.01:
            potentail_netprofileratio = 0
        elif netprofileratio < 0.05:
            potentail_netprofileratio = 5
        elif netprofileratio < 0.1:
            potentail_netprofileratio = 10
        elif netprofileratio < 0.15:
            potentail_netprofileratio = 15
        else:
            potentail_netprofileratio = 20
        if ROE < 0.05:
            potential_roe = 10
        elif ROE < 0.1:
            potential_roe = 20
        elif ROE < 0.15:
            potential_roe = 30
        else:
            potential_roe = 40
        if cashflow < 0 and netprofile < 0:
            potentail_cashflow = 0
        elif netprofile < 0 and cashflow > 0: 
            potentail_cashflow = 20
        elif netprofile > 0 and cashflow < 0: 
            potentail_cashflow = 30
        else:
            potentail_cashflow = 40
        PRC = potentail_netprofileratio + potential_roe + potentail_cashflow
        stock_info = [code, potential_growing, potential_cash, potential_pe, GDP, potentail_netprofileratio, potential_roe, potentail_cashflow, PRC]
        custom_columns = ["code", "G", "D", "P", "GDP", "P", "R", "C", "PRC"]
        ori_df = pd.DataFrame([stock_info], columns=custom_columns)
        df = pd.concat([df, ori_df])

    # finallydata = pd.DataFrame(df, columns=custom_columns)
    df.to_csv("D:\\1\\final.csv", encoding="gbk", index=False)


if __name__ == '__main__':
    main()