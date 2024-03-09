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


def cash(stock, custom_year,custom_quarter):

    cash_flow_list = []
    rs_cash_flow = bs.query_cash_flow_data(code=stock, year=custom_year, quarter=custom_quarter)
    while (rs_cash_flow.error_code == '0') & rs_cash_flow.next():
        cash_flow_list.append(rs_cash_flow.get_row_data())
    if cash_flow_list:
        for item in cash_flow_list:
            try:
                cash_flow_ratio = item[7]
                ## item[7]=经营活动产生的现金流量净额除以营业收入
            except Exception as e:
                logging.info(e)
    else:
        cash_flow_ratio = 0
    return cash_flow_ratio

def profit(stock,custom_year,custom_quarter):
    stockinfo = []
    profit_list = []
    rs_profit = bs.query_profit_data(code=stock, year=custom_year, quarter=custom_quarter)
    while (rs_profit.error_code == '0') & rs_profit.next():
        profit_list.append(rs_profit.get_row_data())
    if len(profit_list) > 1:
        print("{}profit_list超过一条".format(stock))
    for item in  profit_list:
        # 6 净利润 8 营业收入 9 总股数   
        stockinfo = [item[6], item[8], item[9]]
    return stockinfo

def stockprice(stock, custom_year):
    custom_day = "{}-12-31".format(custom_year)
    custom_date = datetime.strptime(custom_day, '%Y-%m-%d')
    weeknumber = custom_date.weekday()
    if weeknumber == 5:
        custom_day = "{}-12-30".format(custom_year)
    elif weeknumber == 6:
        custom_day = "{}-12-29".format(custom_year)    
    result_list = []
    rs = bs.query_history_k_data_plus(stock, "date,close,pbMRQ", start_date=custom_day, end_date=custom_day,frequency="d", adjustflag="3")
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        result_list.append(rs.get_row_data())   
    for item in result_list:
        stockprice = item
    return stockprice

def calculatedividCash(code,currentyear,totalstockshare):
    # 查股息  rs_list[6]是除权除息日
    rs_list = []
    rs_dividend = bs.query_dividend_data(code=code, year=currentyear, yearType="report")
    while (rs_dividend.error_code == '0') & rs_dividend.next():
        rs_list.append(rs_dividend.get_row_data())
    # dividOperateDate = rs_list[0][9]
    result_dividend = pd.DataFrame(rs_list, columns=rs_dividend.fields)
    dividCash = 0
    if len(result_dividend) == 1:
        try:
            dividCash = float(result_dividend.iloc[0, result_dividend.columns.get_loc("dividCashPsBeforeTax")])
        except Exception as e:
            logging.info(e)
            logging.info("{}分红数据未获取".format(code))
    elif len(result_dividend) == 0:
        logging.info("{}分红数据有误或无分红,请手工计算".format(code))
    else:
        # dividCash = result_dividend.iloc[0, result_dividend.cloumns.get_loc("dividCashPsBeforeTax")] + result_dividend.iloc[1, result_dividend.cloumns.get_loc("dividCashPsBeforeTax")]
        logging.info("{}多次分红,需手工修订".format(code))
        for dividend in range(len(result_dividend)):
            try:
                onecash = float(result_dividend.iloc[dividend, result_dividend.columns.get_loc("dividCashPsBeforeTax")])
                dividCash += onecash
            except Exception as e:
                logging.info(e)
    totaldividCash = round(dividCash * totalstockshare)
    return totaldividCash



def main():
    #### 登陆系统 ####
    lg = bs.login()
    stock_list = ["sh.603515"]
    # stock_list = []
    # data = pd.read_csv("d:\\1\\testfilter.csv")
    # for index, row in data.iterrows():
    #     stock_list.append(row[0])
    # Fiveyearbefore = 2020
    # endyear = Fiveyearbefore + 3
    custom_year = 2020
    custom_quarter = 4
    for stock in stock_list:
        rs = bs.query_stock_basic(code=stock)
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        if data_list:
            ipodate = data_list[0][2]
        else:
            continue
        if datetime.strptime(ipodate, "%Y-%m-%d") > datetime.strptime("{}-12-31".format(custom_year), '%Y-%m-%d'):
            continue
        myfinance = profit(stock, custom_year,custom_quarter)
        mystockeprice = stockprice(stock,custom_year)
        mycash_flow_ratio = cash(stock,custom_year,custom_quarter)
        # 净资产 = 总股数*计算日股价/pb
        # print("{} {} {}".format(myprofit[2], mystockeprice[1], mystockeprice[2]))
        try:
            totalshare = float(myfinance[2])
        except Exception as e:
            logging.info(e)
            continue
        mycash = calculatedividCash(stock,custom_year+1,totalshare)
        mynetasset = round(totalshare * float(mystockeprice[1]) / float(mystockeprice[2]))
        if custom_quarter == 4:
            myprofit = round(float(myfinance[0]))
            myrevenue = round(float(myfinance[1]))
        else:
            myprofit = round(float(myfinance[0])*2)
            myrevenue = round(float(myfinance[1])*2)
        try:
            if custom_quarter == 4:
                myrevenue = round(float(myfinance[1]))
            else:
                myrevenue = round(float(myfinance[1])*2)           
        except Exception as e:
            logging.info(e)
            myrevenue = 0

        print("{} {} {} {} {} {} {} {}".format(custom_year,stock, mynetasset, myprofit, myrevenue, totalshare, mycash_flow_ratio, mycash))
        searchquery = "select * from profit where code = '{}' and year = {}".format(stock, custom_year)
        searchResult = cursor.run_query(searchquery)
        if not searchResult:
            query = "insert into stock.profit ( year, code, netasset ,profit, revenue, totalshares, cash_flow_ratio, cash) values ({}, '{}', {}, {}, {}, {}, {}, {});".format(custom_year,stock, mynetasset, myprofit, myrevenue, totalshare, mycash_flow_ratio, mycash)
            queryResult = cursor.run_query(query)
        else:
            logging.info("{}的{}数据已存在".format(stock, custom_year))
    #### 登出系统 ####
    bs.logout()


if __name__ == '__main__':
    main()            