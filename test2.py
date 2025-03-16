#!/usr/bin/python
# coding=utf-8

current_line = 0
query = "SELECT content FROM poem WHERE name = '静夜思' and serialnumber={}".format(current_line + 1)
print(query)

  