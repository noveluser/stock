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
    """ MBRevenue_fiveyearbefore=5年前总营收  netprofit=净利润 totalShare=总股数 dupontNitogr=净利润/营业总收入 Netassets=净资产
    """
    df = pd.DataFrame()
    potential_growing = 0
    potential_cash = 0
    potential_pe = 0
    potentail_netprofileratio = 0
    potential_roe = 0
    potentail_cashflow = 0
    data = pd.read_csv("d:\\1\\4\\secondfliter.csv", encoding="GBK")
    for index, row in data.iterrows():
        code = row[0]
        MBRevenue_fiveyearbefore = row[1]
        MBRevenue = row[2]
        pe = row[7]
        cache = row[8]
        ROE = row[9]
        netprofileratio = row[10]
        cacheflow = row[11]
        netprofile = row[4]
        if MBRevenue / MBRevenue_fiveyearbefore < 1.05:
            potential_growing = 0
        elif MBRevenue / MBRevenue_fiveyearbefore < 1.28:
            potential_growing = 20
        elif MBRevenue / MBRevenue_fiveyearbefore < 1.61:
            potential_growing = 30
        elif MBRevenue / MBRevenue_fiveyearbefore < 2:
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
        if cache == 0:
            potential_cash = 0
        elif cache < 0.02:
            potential_cash = 5
        elif cache < 0.04:
            potential_cash = 10
        elif cache < 0.06:
            potential_cash = 15
        else:
            potential_cash = 20
        GDP = potential_growing + potential_cash + potential_pe
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
        if cacheflow < 0 and netprofile < 0:
            potentail_cashflow = 0
        elif netprofile < 0 and cacheflow > 0: 
            potentail_cashflow = 20
        elif netprofile > 0 and cacheflow < 0: 
            potentail_cashflow = 30
        else:
            potentail_cashflow = 40
        PRC = potentail_netprofileratio + potential_roe + potentail_cashflow
        stock_info = [code, potential_growing, potential_cash, potential_pe, GDP, potentail_netprofileratio, potential_roe, potentail_cashflow, PRC]
        custom_columns = ["code", "G", "D", "P", "GDP", "P", "R", "C", "PRC"]
        ori_df = pd.DataFrame([stock_info], columns=custom_columns)
        df = pd.concat([df, ori_df])

    # finallydata = pd.DataFrame(df, columns=custom_columns)
    df.to_csv("D:\\1\\4\\thirdfliter.csv", encoding="gbk", index=False)


if __name__ == '__main__':
    main()