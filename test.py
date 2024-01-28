# coding=utf-8

import baostock as bs
import pandas as pd


def main():
    #### 登陆系统 ####
    lg = bs.login()

    profit_list = []
    rs_profit = bs.query_profit_data(code="sz.300888", year=2020, quarter=4)
    while (rs_profit.error_code == '0') & rs_profit.next():
        profit_list.append(rs_profit.get_row_data())
    result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
    row_index = result_profit.index
    print(row_index)
    print(result_profit.loc[0,"totalShare"])

    # #### 结果集输出到csv文件 ####   
    # result_profit.to_csv("D:\\1\\history_Dividend_data.csv", encoding="gbk",index=False)

    #### 登出系统 ####
    bs.logout()
            
if __name__ == '__main__':
    main()            