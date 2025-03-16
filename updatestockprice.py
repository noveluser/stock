import pandas as pd
import baostock as bs

# Excel文件路径
excel_file = "d:\\1\\test.xlsx"  # 替换为您的Excel文件路径

# 读取Excel文件
df = pd.read_excel(excel_file)

# 获取正股代码列
stock_codes = df['正股代码'].tolist()

# 连接Baostock
lg = bs.login()
if lg.error_code != '0':
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    exit()

# 获取收盘价
close_prices = []
for code in stock_codes:
    code = str(code).zfill(6)
    code_str = f'sh.{code}' if str(code).startswith('6') else f'sz.{code}'
    print(code_str)
    rs = bs.query_history_k_data_plus(code_str,
                                      "close",
                                      start_date='2025-03-14',
                                      end_date='2025-03-14',
                                      frequency="d",
                                      adjustflag="3")
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    if data_list:
        close_prices.append(float(data_list[0][0]))
    else:
        close_prices.append(None)  # 如果没有数据，添加None
    # print(data_list)

# 登出Baostock
bs.logout()

# 更新Excel文件中的正股价格列
df['正股价格'] = close_prices

# 保存更新后的Excel文件
df.to_excel(excel_file, index=False)

print('正股价格已更新到Excel文件。')