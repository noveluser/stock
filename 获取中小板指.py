# coding=utf-8

'''
Created on 2019.11.18
筛选连续4个月下跌的名单
@author: wangle
'''

import baostock as bs
import pandas as pd
import logging
import time
import datetime

# 定义日志输出格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="E:\\historystock\\getostock.log",
                    filemode='a')


if __name__ == '__main__':
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    rs = bs.query_history_k_data_plus("sh.000015",
        "date,code,close,pctChg",
        start_date='2017-07-11', end_date='2020-04-30',
        frequency="m", adjustflag="2")
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####   
    result.to_csv("E:\\historystock\\zhongxiaoban.csv", index=False)
    print(result)

    #### 登出系统 ####
    bs.logout()
