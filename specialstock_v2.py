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
import sys

# 定义日志输出格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="d:\\1\\getostock.log",
                    filemode='a')


def calculatedividCash(code,currentyear,totalstockshare):
    # 查股息  rs_list[6]是除权除息日
    rs_list = []
    rs_dividend = bs.query_dividend_data(code=code, year=currentyear, yearType="report")
    while (rs_dividend.error_code == '0') & rs_dividend.next():
        rs_list.append(rs_dividend.get_row_data())
    # dividOperateDate = rs_list[0][9]
    result_dividend = pd.DataFrame(rs_list, columns=rs_dividend.fields)
    if len(result_dividend) == 1:
        dividCash = float(result_dividend.iloc[0, result_dividend.columns.get_loc("dividCashPsBeforeTax")])
    elif len(result_dividend) == 0:
        dividCash = 0
        logging.info("{}分红数据有误或无分红,请手工计算".format(code))
    else:
        # dividCash = result_dividend.iloc[0, result_dividend.cloumns.get_loc("dividCashPsBeforeTax")] + result_dividend.iloc[1, result_dividend.cloumns.get_loc("dividCashPsBeforeTax")]
        # print(result_dividend)
        # print("{}多次分红".format(code))
        dividCash = 0
        # for dividend in range(len(result_dividend)):
        #     dividCash += float(result_dividend.iloc[dividend, result_dividend.cloumns.get_loc("dividCashPsBeforeTax")])
    totaldividCash = dividCash * totalstockshare

    return totaldividCash


def main():
    """ MBRevenue_fiveyearbefore=5年前总营收  netprofit=净利润 totalShare=总股数 dupontNitogr=净利润/营业总收入 Netassets=净资产
    """
    df = pd.DataFrame()
    stock_list = []
    result_list = []
    estimated_value = 1.25   # 3季度估算全年的比例，保守些

    data = pd.read_csv("d:\\1\\4\\testfliter.csv")
    for index, row in data.iterrows():
        stock_list.append(row[0])
    Fiveyearbefore = 2020
    endyear = Fiveyearbefore + 3
    should_skip = False
    for item in stock_list:

        # 获取证券基本资料
        rs = bs.query_stock_basic(code=item)
        # 打印结果集
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        ipoDate_result = result.iloc[0,result.columns.get_loc("ipoDate")]
        ipodate = datetime.datetime.strptime(ipoDate_result, '%Y-%m-%d')
        startday =  datetime.datetime.strptime("{}-12-31".format(Fiveyearbefore), '%Y-%m-%d')
        if ipodate > startday:
            print("{} skip".format(item))
            continue
        else:
            # 查询季频估值指标盈利能力
            MBRevenue_list = []
            totalShare_list = []
            netprofit_list = []
            Netassets_list = []
            dupontNitogr_list = []
            dividCash_list = []
            ROE_list = []
            cash_flow_ratio_list = []
            for currentyear in range(Fiveyearbefore,endyear+1):  
                if currentyear != endyear:
                    custom_quarter = 4
                    currentDay = "{}-12-31".format(currentyear)  
                else:
                    custom_quarter = 3
                    currentDay = "{}-01-19".format(currentyear+1)  
                profit_list = []
                print("{}--{}  start".format(currentyear, item))

                # 取5年前的总营收入
                rs_profit = bs.query_profit_data(code=item, year=currentyear, quarter=custom_quarter)
                while (rs_profit.error_code == '0') & rs_profit.next():
                    profit_list.append(rs_profit.get_row_data())
                result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
                try:
                    MBRevenue_list.append(int(float(result_profit["MBRevenue"])))
                except ValueError as e:
                    MBRevenue_list.append(0)
                    logging.info("{}-{}-{}".format(item,currentyear,e))
                except TypeError as e:
                    logging.info("{}-{}-{}".format(item,currentyear,e))
                    should_skip = True
                    break
                totalShare = int(float(result_profit["totalShare"]))
                totalShare_list.append(totalShare)
                netprofit_list.append(int(float(result_profit["netProfit"])))

                # ## 获取沪深A股估值指标(日频)数据 ####
                # peTTM    滚动市盈率
                # psTTM    滚动市销率
                # pcfNcfTTM    滚动市现率
                # pbMRQ    市净率
                rs = bs.query_history_k_data_plus(item, "date,code,close,peTTM,pbMRQ", start_date=currentDay, frequency="d", adjustflag="3")
                while (rs.error_code == '0') & rs.next():
                    # 获取一条记录，将记录合并在一起
                    result_list.append(rs.get_row_data())
                stock_result = pd.DataFrame(result_list, columns=rs.fields)
                close = float(stock_result.tail(1)["close"])
                pb = float(stock_result.tail(1)["pbMRQ"])
                Netassets_list.append(close*totalShare/pb)

                # 查询杜邦指数
                dupont_list = []
                rs_dupont = bs.query_dupont_data(code=item, year=currentyear, quarter=custom_quarter)
                while (rs_dupont.error_code == '0') & rs_dupont.next():
                    dupont_list.append(rs_dupont.get_row_data())
                result_dupont = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
                dupontNitogr_list.append(float(result_dupont.tail(1)["dupontNitogr"]))
                ROE_list.append(float(result_dupont["dupontROE"]))

                # 查股息
                dividCash = calculatedividCash(item, currentyear,totalShare)
                dividCash_list.append(dividCash)

                # 季频现金流量
                cash_flow_list = []
                rs_cash_flow = bs.query_cash_flow_data(code=item, year=currentyear, quarter=custom_quarter)
                while (rs_cash_flow.error_code == '0') & rs_cash_flow.next():
                    cash_flow_list.append(rs_cash_flow.get_row_data())
                result_cash_flow = pd.DataFrame(cash_flow_list, columns=rs_cash_flow.fields)
                cash_flow_ratio_list.append(float(result_cash_flow["CFOToOR"]))

        if not should_skip:
            stock = [item, MBRevenue_list[0], MBRevenue_list[1], MBRevenue_list[2], MBRevenue_list[3], Netassets_list[0], Netassets_list[1], Netassets_list[2], Netassets_list[3], netprofit_list[0], netprofit_list[1], netprofit_list[2], netprofit_list[3], dividCash_list[0], dividCash_list[1], dividCash_list[2], dividCash_list[3], ROE_list[0], ROE_list[1], ROE_list[2], ROE_list[3],dupontNitogr_list[0],dupontNitogr_list[1],dupontNitogr_list[2],dupontNitogr_list[3], cash_flow_ratio_list[0], cash_flow_ratio_list[1], cash_flow_ratio_list[2], cash_flow_ratio_list[3] ]
            custom_columns = ["code", "总营收_3Y", "总营收_2Y", "总营收_1Y", "总营收", "净资产_3Y", "净资产_2Y", "净资产_1Y", "净资产", "净利润_3Y", "净利润_2Y", "净利润_1Y", "净利润", "分红_3Y", "分红_2Y", "分红_1Y", "分红","ROE_3Y","ROE_2Y","ROE_1Y","ROE",  "净利润率_3Y", "净利润率_2Y", "净利润率_1Y", "净利润率", "现金流_3Y", "现金流_2Y", "现金流_1Y", "现金流"]
            ori_df = pd.DataFrame([stock], columns=custom_columns)
            df = pd.concat([df, ori_df])
            print(stock)
        else:
            pass
        print("{}--{}  end".format(currentyear, item))       
    # finallydata = pd.DataFrame(df, columns=custom_columns)
    df.to_csv("D:\\1\\4\\customstock.csv", encoding="gbk", index=False)


if __name__ == '__main__':
    # ## 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    main()
    # ### 登出系统 ####
    bs.logout()