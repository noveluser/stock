# coding=utf-8

'''
Created on 2024.1.15
将候选股票的相关数据展示
@author: wangle
'''

import baostock as bs
import pandas as pd
import logging
from my_mysql import Database
import datetime
from decimal import Decimal


# 定义日志输出格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="d:\\1\\getostock.log",
                    filemode='a')


# enviroments
cursor = Database(dbname="stock", username="wangxp01", password="111111", host="192.168.217.100", port="3306")


def main():
    df = pd.DataFrame()
    stock_list = []
    data = pd.read_csv("d:\\1\\firstfliter.csv")
    for index, row in data.iterrows():
        stock_list.append(row[0])
    for item in stock_list:
        netasset_list = []
        profit_list = []
        revenue_list = []
        cash_list = []
        cashflowratio_list = []
        ROE_list = []
        result_list = []
        currentDay = "2024-03-01"
        startyear = 2019
        endyear = startyear + 4
        circle_flag = False
        # 取5年内净资产,净利润,总营收,现金流比率, ROE情况
        for i in range(startyear, endyear+1):
            query1 = "select netasset,profit, revenue, cash_flow_ratio from profit where code = '{}' and year = {}".format(item, i)
            result = cursor.run_query(query1)
            if not result:
                logging.info("{} {}result is blank".format(i, item))
                circle_flag = True
                continue
            current_netasset = result[0][0]
            netasset_list.append(current_netasset)
            current_profit = result[0][1]
            profit_list.append(current_profit)
            current_revenue = result[0][2]
            revenue_list.append(current_revenue)
            current_cashflowratio = result[0][3]
            cashflowratio_list.append(current_cashflowratio)
            ROE_list.append(current_profit/current_netasset)
        if circle_flag:
            continue   # 跳出循环，不写入这个股票

        # 取动态PE值，current_profit是最新预测盈利
        lg = bs.login()
        rs = bs.query_history_k_data_plus(item, "date,code,close", start_date=currentDay, frequency="d", adjustflag="3")
        while (rs.error_code == '0') & rs.next():
            result_list.append(rs.get_row_data())
        stock_result = pd.DataFrame(result_list, columns=rs.fields)
        close = float(stock_result.tail(1)["close"])
        bs.logout()
        # 取当前股数及预测盈利
        query2 = "select profit,totalshares from profit where code = '{}' and year = {}".format(item, endyear)
        result2 = cursor.run_query(query2)
        current_profit = result2[0][0]
        current_totalshares = result2[0][1]
        pe = current_totalshares * close / current_profit

        # 取分红额
        for i in range(startyear, endyear):
            query3 = "select cash from profit where code = '{}' and year = {}".format(item, i)
            current_cache = cursor.run_query(query3)[0][0]
            cash_list.append(current_cache)       

        stock = [item, netasset_list[0], netasset_list[1], netasset_list[2], netasset_list[3], netasset_list[4], profit_list[0], profit_list[1], profit_list[2], profit_list[3], profit_list[4], revenue_list[0], revenue_list[1], revenue_list[2], revenue_list[3], revenue_list[4], cashflowratio_list[0], cashflowratio_list[1], cashflowratio_list[2], cashflowratio_list[3], cashflowratio_list[4], cash_list[0], cash_list[1], cash_list[2], cash_list[3] , close, current_totalshares]
        custom_columns =["code", "2019净资产", "2020净资产", "2021净资产", "2022净资产", "2023净资产", "2019净利润", "2020净利润", "2021净利润", "2022净利润", "2023净利润", "2019总营收", "2020总营收", "2021总营收", "2022总营收", "2023总营收", "2019现金流比率", "2020现金流比率", "2021现金流比率", "2022现金流比率", "2023现金流比率", "2019分红", "2020分红", "2021分红", "2022分红", "当前股价", "总股数"]
        ori_df = pd.DataFrame([stock], columns=custom_columns)
        df = pd.concat([df, ori_df])
    # finallydata = pd.DataFrame(df, columns=custom_columns)
    # df.transpose().to_csv("D:\\1\\detail.csv", encoding="gbk", index=False)
    df.transpose().to_excel("D:\\1\\detail.xlsx", index=True)


if __name__ == '__main__':
    main()