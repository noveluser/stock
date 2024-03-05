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
    query1 = "select netasset from profit where code = '{}' and year = {}".format(stockcode,startyear)
    startyear_netasset = cursor.run_query(query1)[0][0]
    try:
        query2 = "select netasset from profit where code = '{}' and year = {}".format(stockcode,endyear)
        endeyear_netasset = cursor.run_query(query2)[0][0]
    except Exception as e:
        print(stockcode)
        endeyear_netasset = 0
    # 1.75是4年15%增长率，2.24是4年25%的增长率
    if  endeyear_netasset > startyear_netasset * 1.75 and  endeyear_netasset < startyear_netasset * 2.44:
        return True
    else:
        return False
    
def compare_everyyearnetassets(stockcode,startyear, endyear):
    premit_flag = True
    for i in range(startyear, endyear):
        try:
            query1 = "select netasset from profit where code = '{}' and year = {}".format(stockcode,i)
            startyear_netasset = cursor.run_query(query1)[0][0]
            query2 = "select netasset from profit where code = '{}' and year = {}".format(stockcode,i+1)
            endeyear_netasset = cursor.run_query(query2)[0][0]
        except Exception as e:
            logging.info("{}异常数据.{}".format(stockcode,e))
            endeyear_netasset = 0
        # 假定某年净资产是上年的1.3以上，可以判断为非正常增长
        if  endeyear_netasset > startyear_netasset * 1.3:
            premit_flag = False
    return premit_flag            





def main():
    startyear = 2019
    endyear = 2022
    stock_list = []
    second_stock_list = []
    query = "select code from profit where year = {}".format(startyear)
    result = cursor.run_query(query)
    for item in result:
        stockcode = item[0]
        filter_flag = compare_netassets(stockcode,startyear, endyear)
        if filter_flag:
            stock_list.append(stockcode)
    # 二次筛选，剔除不正常增长的企业
    for stockcode in stock_list:
        second_filter_flag = compare_everyyearnetassets(stockcode,startyear, endyear)
        if second_filter_flag:
            second_stock_list.append(stockcode)       
    custom_columns = ["code"]
    df = pd.DataFrame(second_stock_list,columns = custom_columns )
    df.to_csv("D:\\1\\firstfliter.csv", encoding="gbk",index=False)


if __name__ == '__main__':
    main()            