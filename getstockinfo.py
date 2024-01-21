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
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)



    # # 查询季频估值指标盈利能力
    # profit_list = []
    # # for custom_year in [2021,2022,2023]:
    # #     for item in [1,2,3]:
    # # rs_profit = bs.query_profit_data(code="sz.300285", year=custom_year, quarter=item)
    # rs_profit = bs.query_profit_data(code="sz.300285", year=2023, quarter=3)
    # while (rs_profit.error_code == '0') & rs_profit.next():
    #     profit_list.append(rs_profit.get_row_data())

    # result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
    # statDate = result_profit["statDate"]
    # netprofit = int(float(result_profit.tail(1)["netProfit"]))
    # totalShare = int(float(result_profit.tail(1)["totalShare"]))

    # # 查询杜邦指数
    # dupont_list = []
    # rs_dupont = bs.query_dupont_data(code="sz.300285", year=2023, quarter=3)
    # while (rs_dupont.error_code == '0') & rs_dupont.next():
    #     dupont_list.append(rs_dupont.get_row_data())
    # result_dupont = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
    # dupontNitogr = float(result_dupont.tail(1)["dupontNitogr"])

    # #### 获取沪深A股估值指标(日频)数据 ####
    # # peTTM    滚动市盈率
    # # psTTM    滚动市销率
    # # pcfNcfTTM    滚动市现率
    # # pbMRQ    市净率
    # rs = bs.query_history_k_data_plus("sz.300285",
    #     "date,code,close,peTTM,pbMRQ",
    #     start_date='2024-01-15', 
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
    # stock = [netprofit, MBRevenue, totalShare, Netassets, close, pb, pe]
    # print(stock)


    # 查股息
    rs_list = []
    rs_dividend_2017 = bs.query_dividend_data(code="sz.300285", year="2023", yearType="report")
    while (rs_dividend_2017.error_code == '0') & rs_dividend_2017.next():
        rs_list.append(rs_dividend_2017.get_row_data())

    result_dividend = pd.DataFrame(rs_list, columns=rs_dividend_2017.fields)
    
    # 打印输出
    print(result_dividend)

    ## 结果集输出到csv文件 ####   
    result_dividend.to_csv("D:\\1\\history_Dividend_data.csv", encoding="gbk",index=False)

    #### 登出系统 ####
    bs.logout()

if __name__ == '__main__':
    main()

