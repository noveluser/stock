# coding=utf-8

import baostock as bs
import pandas as pd
import logging
from datetime import datetime
from my_mysql import Database


# 定义日志输出格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="d:\\1\\getostock.log",
                    filemode='a')

# enviroments
cursor = Database(dbname="stock", username="wangxp01", password="111111", host="192.168.217.100", port="3306")


def compare_netassets(stockcode,startyear, endyear):
    for i in range(startyear, endyear):
        query1 = "select netasset from profit where code = '{}' and year = {}".format(stockcode,i)
        startyear_netasset = cursor.run_query(query1)[0][0]
        try:
            query2 = "select netasset from profit where code = '{}' and year = {}".format(stockcode,i+1)
            endeyear_netasset = cursor.run_query(query2)[0][0]
        except Exception as e:
            print(stockcode)
            endeyear_netasset = 0
    # 1.75是4年15%增长率，2.24是4年25%的增长率
    if startyear_netasset * 1.75 > endeyear_netasset and startyear_netasset * 2.44 < endeyear_netasset:
        return True
    else:
        return False





def main():
    startyear = 2019
    endyear = 2022
    stock_list = []
    second_stock_list = []
    data = pd.read_csv("d:\\1\\firstfliter.csv")
    for index, row in data.iterrows():
        stock_list.append(row[0])
    for stockcode in stock_list:
        filter_flag = compare_netassets(stockcode,startyear, endyear)
        if filter_flag:
            second_stock_list.append(stockcode)
    custom_columns = ["code"]
    df = pd.DataFrame(second_stock_list,columns = custom_columns )
    df.to_csv("D:\\1\\firstfliter.csv", encoding="gbk",index=False)


if __name__ == '__main__':
    main()            