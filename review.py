# coding=utf-8

# 暂定
# wangle
# v0.2

import tkinter as tk
import tkinter.font as tkFont

poem = ["床前明月光", "疑是地上霜", "举头望明月", "低头思故乡"]
current_line = 0  # 当前显示诗句的行数，从 0 开始

def display_line(event=None):
    """显示用户选择的诗句."""
    global current_line  # 使用全局变量 current_line
    
    # 获取输入框中的内容
    line_text = entry.get()

    if line_text:  # 如果输入框不为空
        try:
            line_num = int(line_text)
            if 1 <= line_num <= len(poem):
                current_line = line_num - 1  # 更新当前行数
                result_label.config(text=poem[current_line])
            else:
                result_label.config(text="输入错误，请输入 1-4 之间的数字。")
        except ValueError:
            result_label.config(text="输入错误，请输入数字。")
    else:  # 如果输入框为空
        current_line = (current_line + 1) % len(poem)  # 计算下一行，循环到第一行
        result_label.config(text=poem[current_line])

    entry.delete(0, tk.END)  # 清空输入框

# 创建主窗口
window = tk.Tk()
window.title("静夜思")
window.geometry("400x200")  # 设置窗口大小为 400x200

# 创建标签和输入框
label = tk.Label(window, text="请输入想要显示的诗句行数（1-4），回车显示下一句：")
label.pack()

entry = tk.Entry(window)
entry.pack()
entry.bind("<Return>", display_line)  # 绑定回车键

# 创建结果显示标签
result_label = tk.Label(window, text="", font=("Arial", 36))  # 设置字体为 Arial，大小为 36
result_label.pack()

# 初始化显示第一行诗句
result_label.config(text=poem[current_line])

# 进入消息循环
window.mainloop()