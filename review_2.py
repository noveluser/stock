# coding=utf-8

# 暂定
# wangle
# v0.2

import tkinter as tk
from my_mysql import Database

def main():
    """程序主函数"""

    # 数据库连接
    cursor = Database(dbname="stock", username="wangxp01", password="111111", host="192.168.217.100", port="3306")

    current_line = 0

    def display_line(event=None):
        """显示用户选择的诗句."""
        global current_line, poem_name

        # 获取输入框中的内容
        line_text = entry.get()

        if line_text:
            try:
                line_num = int(line_text)
                if 1 <= line_num <= 4:
                    current_line = line_num - 1
                    # 使用参数化查询防止 SQL 注入
                    query = "select content FROM poem WHERE name = %s and serialnumber = %s"
                    params = (poem_name, current_line + 1)
                    result = cursor.run_query(query, params)
                    result_label.config(text=result[0])
                else:
                    result_label.config(text="输入错误，请输入 1-4 之间的数字。")
            except ValueError:
                result_label.config(text="输入错误，请输入数字。")
        else:
            current_line = (current_line + 1) % 4
            # 使用参数化查询防止 SQL 注入
            query = "select content FROM poem WHERE name = %s and serialnumber = %s"
            params = (poem_name, current_line + 1)
            result = cursor.run_query(query, params)
            result_label.config(text=result[0])

        entry.delete(0, tk.END)

    def get_poem_name():
        """获取诗歌名称"""
        global poem_name
        poem_name = poem_entry.get()
        if poem_name:
            # 初始化显示第一行诗句
            query = "select content FROM poem WHERE name = %s and serialnumber = %s"
            params = (poem_name, 1)
            result = cursor.run_query(query, params)
            if result:
                result_label.config(text=result[0])
            else:
                result_label.config(text="该诗歌不存在或数据错误。")
        else:
            result_label.config(text="请输入诗歌名称。")
        poem_entry.delete(0, tk.END)  # 清空诗歌名称输入框

    # 创建主窗口
    window = tk.Tk()
    window.title("古文背诵")
    window.geometry("800x400")

    # 创建诗歌名称输入框
    poem_label = tk.Label(window, text="请输入诗歌名称：")
    poem_label.pack()
    poem_entry = tk.Entry(window)
    poem_entry.pack()
    poem_entry.bind("<Return>", get_poem_name)  # 绑定回车键

    # 创建标签和输入框
    label = tk.Label(window, text="请输入想要显示的诗句行数（1-4），回车显示下一句：")
    label.pack()

    entry = tk.Entry(window)
    entry.pack()
    entry.bind("<Return>", display_line)

    # 创建结果显示标签
    result_label = tk.Label(window, text="", font=("Arial", 36))
    result_label.pack()

    # 进入消息循环
    window.mainloop()

    # 关闭数据库连接
    # cursor.close()

# 如果是直接运行文件，则调用 main() 函数
if __name__ == "__main__":
    main()