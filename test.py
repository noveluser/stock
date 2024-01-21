# coding=utf-8

import baostock as bs
import pandas as pd


def main():
    #### 登陆系统 ####
    lg = bs.login()

    rs_list = []
    rs_dividend = bs.query_dividend_data(code="sz.300888", year=2022, yearType="report")
    while (rs_dividend.error_code == '0') & rs_dividend.next():
        rs_list.append(rs_dividend.get_row_data())
    print(rs_list)
    dividOperateDate = rs_list[0][9]
    print(dividOperateDate)

    # #### 结果集输出到csv文件 ####   
    # result_profit.to_csv("D:\\1\\history_Dividend_data.csv", encoding="gbk",index=False)

    #### 登出系统 ####
    bs.logout()
            
if __name__ == '__main__':
    main()            