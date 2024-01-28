#!/usr/bin/python
# coding=utf-8

from my_mysql import Database
import datetime
import pandas as pd
import logging
import json
import requests


logging.basicConfig(
                    level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='d://1//3//dump.log',
                    filemode='a')


# enviroments
cursor = Database(dbname="stock", username="wangxp01", password="111111", host="192.168.217.100", port="3306")

def main():
    url = 'http://api.biyingapi.com/hicw/yl/2022/1/4519d46752654bda3e'
    # url = 'http://api.biyingapi.com/hslt'
    # 假设这是API需要的参数
    params = {
        'param1': 'value1',
        'param2': 'value2'
    }

    # 假设这是需要的身份验证信息
    headers = {
        'Authorization': 'Bearer your_access_token'
    }
    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
    df = pd.DataFrame()

    # # 打印API的响应
    parsed_data = response.json()
    for item in parsed_data:
        dm = item["dm"]
        query ="insert into stock.hicw (dm, mc, jzcsy ,jlr, mgsy, yysr, y, q) values ('{}', '{}', {}, {}, {}, {}, {}, {});".format(item["dm"], item["mc"], item["jzcsy"], item["jlr"], item["mgsy"], item["yysr"], item["y"], item["q"])
        # print(query)
        queryResult = cursor.run_query(query)


    # # # 打印API的响应
    # parsed_data = response.json()
    # for item in parsed_data:
    #     ori_df = pd.json_normalize(item)
    #     df_index = ["dm", "mc", "jzcsy", "jlr", "mgsy", "yysr", "y", "q"]
    #     df = pd.concat([df, ori_df[df_index]])

    # # 将DataFrame导出到Excel并保存列名
    # excel_filename = 'd://1//3//json_data_to_excel.xlsx'
    # df.to_excel(excel_filename, index=False, header=True)



if __name__ == '__main__':
    main()        