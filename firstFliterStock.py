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
    Fiveyearbefore = 2019
    currentyear = 2023
    stock_list = []
    firstfilter_stocklist = []
    estimated_value = 4/3
    data = pd.read_csv("d:\\1\\stocklist.csv")       
    for index, row in data.iterrows():
        stock_list.append(row[0])
    for item in stock_list:
        # 查询季频估值指标盈利能力
        profit_list = []
        Fiveyearbefore = 2019
        currentyear = 2023
        currentDay = '2024-01-16'
        # 取5年前的总营收入
        rs_profit = bs.query_profit_data(code=item, year=Fiveyearbefore, quarter=4)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())

        result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
        try:
            MBRevenue_fiveyearbefore = int(float(result_profit["MBRevenue"]))
        except Exception as e:
            print(e)
            print(item)
            print(result_profit)

        # 查询当年三季度的营收，再4/3估算出全年的营收
        rs_profit = bs.query_profit_data(code=item, year=currentyear, quarter=3)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())

        result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
        statDate = result_profit["statDate"]
        netprofit = int(float(result_profit.tail(1)["netProfit"]))
        totalShare = int(float(result_profit.tail(1)["totalShare"]))

        # 查询杜邦指数
        dupont_list = []
        rs_dupont = bs.query_dupont_data(code=item, year=currentyear, quarter=3)
        while (rs_dupont.error_code == '0') & rs_dupont.next():
            dupont_list.append(rs_dupont.get_row_data())
        result_dupont = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
        dupontNitogr = float(result_dupont.tail(1)["dupontNitogr"])
        MBRevenue = estimated_value * netprofit / dupontNitogr

        if (MBRevenue > MBRevenue_fiveyearbefore * 2 and MBRevenue < MBRevenue_fiveyearbefore * 3 ):
            firstfilter_stocklist.append(item)
            print(item)
    custom_columns = ["code"]
    df = pd.DataFrame(firstfilter_stocklist,columns = custom_columns )
    df.to_csv("D:\\1\\firstfliter.csv", encoding="gbk",index=False)
    # #### 获取沪深A股估值指标(日频)数据 ####
    # # peTTM    滚动市盈率
    # # psTTM    滚动市销率
    # # pcfNcfTTM    滚动市现率
    # # pbMRQ    市净率
    # rs = bs.query_history_k_data_plus("sz.300285",
    #     "date,code,close,peTTM,pbMRQ",
    #     start_date= currentDay, 
    #     frequency="d", adjustflag="3")
    # print('query_history_k_data_plus respond error_code:'+rs.error_code)
    # print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

    # #### 打印结果集 ####
    # result_list = []
    # while (rs.error_code == '0') & rs.next():
    #     # 获取一条记录，将记录合并在一起
    #     result_list.append(rs.get_row_data())
    # stock_result = pd.DataFrame(result_list, columns=rs.fields)
    # close = float(stock_result.tail(1)["close"])
    # pb = float(stock_result.tail(1)["pbMRQ"])
    # fix_value = 4/3
    # pe = totalShare*close/ (netprofit * fix_value)
    # MBRevenue = netprofit / dupontNitogr
    # Netassets = close * totalShare / pb

    # # 查股息
    # rs_list = []
    # rs_dividend_2017 = bs.query_dividend_data(code="sz.300285", year="2023", yearType="report")
    # while (rs_dividend_2017.error_code == '0') & rs_dividend_2017.next():
    #     rs_list.append(rs_dividend_2017.get_row_data())

    # result_dividend = pd.DataFrame(rs_list, columns=rs_dividend_2017.fields)
    # if len(result_dividend) > 1:
    #     dividCash = result_dividend.tail(1)["dividCashPsBeforeTax"]
    #     print("超过1次分红")
    # else:
    #     dividCash = result_dividend["dividCashPsBeforeTax"]
    # dividendYield = float(dividCash) / close
    # stock = [MBRevenue_fiveyearbefore, MBRevenue, Netassets, netprofit, totalShare,  close, pb, pe, dividendYield]
    # print(stock)
    # custom_columns = ["5年前总营收", "当前总营收", "当前净资产", "净利润", "总股数", "当前价", "PB", "PE", "股息率"]
    # df = pd.DataFrame([stock],columns = custom_columns )


    # # 结果集输出到csv文件 ####   
    # df.to_csv("D:\\1\\history_Dividend_data.csv", encoding="gbk",index=False)

    #### 登出系统 ####
    bs.logout()

if __name__ == '__main__':
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)
    main()
    # df = pd.DataFrame([[1, 2], [3, 4]], columns=['column1', 'column2'])