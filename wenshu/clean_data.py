#!/usr/bin/python
#-*- coding:utf-8 -*-
"""wish no bug"""
############################
#File Name: test_0.py
#Author: zhangyang
#Mail: ass7798@qq.com
#Created Time: 2019-03-02 00:57:54
############################
import sys
import os
# 清洗旧的数据
for line in sys.stdin:
    path = line.split(' ')[-1].strip()
    if "-" in path:
        path_0 = 'data/20190228/' + path
        if not os.path.exists(path_0):
            continue
        f = open(path_0)
        data  = f.read()
        f.close()
        if "failed" in data:
            continue
        list_0 = data.split('\n')
        length = len(list_0)
        if length >= 3:
            tmp_0 = list_0[0]
            time_0 = tmp_0.split(' ')[0][:4]
            list_tmp = data.split(time_0)
            data_new = time_0 + list_tmp[1]
            data = data_new.strip()
        #n = path[0].lower()
        if len(data) < 100:
            continue
        n = 'last_data'
        w = open("old_data/" + n + "/" +  path ,'w')
        w.write(data)
        w.close()
        os.remove(path_0)
        #print(path,data_new)
