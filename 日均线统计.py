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
    print(datetime.datetime.now())
    lg = bs.login()
    # 显示登陆返回信息
    logging.info('login respond error_code:'+lg.error_code)
    logging.info('login respond  error_msg:'+lg.error_msg)

    rs = bs.query_trade_dates(start_date="2019-01-01", end_date="2020-01-01")
    print('query_trade_dates respond error_code:'+rs.error_code)
    print('query_trade_dates respond  error_msg:'+rs.error_msg)

    tradeDate_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        tradeDate = rs.get_row_data()
        if tradeDate[1] == '1':
            tradeDate_list.append(tradeDate[0])
    for k in range(len(tradeDate_list)):
        strEndTime = tradeDate_list[k+59]
        strStartTime = tradeDate_list[k]
        # print(strStartTime, strEndTime)
        rs = bs.query_all_stock(day=strStartTime)
        logging.info('query_all_stock respond error_code:'+rs.error_code)
        logging.info('query_all_stock respond  error_msg:'+rs.error_msg)
        stock_list = []
        closePrice_list = []
        data = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            stock_list.append(rs.get_row_data()[0])
        for row in range(len(stock_list)):
            rs2 = bs.query_stock_basic(code=stock_list[row])
            b = rs2.get_row_data()
            if int(b[4]) == 1:
                data.append(stock_list[row])
        # print(data)
        # data = pd.read_csv("E:\\historystock\\stocklist.csv")
        lowPriceCount = 0
        filterDate_list = filterDate = []
        for i in range(len(data)):
            # print(data.iat[i, 0])
            sumClose = 0
            closePrice_list = []
            rs2 = bs.query_history_k_data_plus(data[i],
                                                "date,code,close,volume",
                                                start_date=strStartTime,
                                                end_date=strEndTime,
                                                frequency="d",
                                                adjustflag="2")
            while (rs2.error_code == '0') & rs2.next():
                # 获取一条记录，将记录合并在一起
                a = rs2.get_row_data()
                if a[3]:
                    closePrice_list.append(a[2])

            for j in range(len(closePrice_list)):
                sumClose += float(closePrice_list[j])
            try:
                averageClose = sumClose/j
            except Exception as e:
                print(e)
                print(data[i])
            # print(averageClose, float(a[2]))
            if float(a[2]) - averageClose < 0:
                lowPriceCount += 1
        stockPercent = lowPriceCount / len(data)
        filterData = [strStartTime, len(data), lowPriceCount, lowPriceCount/float(len(data))]
        filterDate_list.append(filterData)
        logging.info(filterDate_list)
        time.sleep(60)
        print(k)
    result = pd.DataFrame(filterDate_list)
    # 结果集输出到csv文件
    result.to_csv("E:\\historystock\\staticstock.csv", encoding="gbk", index=False)
    print(result)
    bs.logout()
