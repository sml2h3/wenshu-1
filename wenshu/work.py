#!/usr/bin/python
#-*- coding:utf-8 -*-
"""wish no bug"""
############################
#File Name: work.py
#Author: zhangyang
#Mail: ass7798@qq.com
#Created Time: 2019-02-28 00:29:46
############################
import os
import sys
import time
def sep_data(list_all,n):
    count = 0
    w_list = []
    for i in range(n):
        file_tmp = "id_sep/" + str(i)
        w = open(file_tmp,'w')
        w.close()
        w = open(file_tmp,'a+')
        w_list.append(w)
    for tmp in list_all:
        count += 1
        count = count % n
        w_list[count ].write(tmp + '\n')

    for i in range(n):
        w_list[i].close()

#for line in sys.stdin:
#    pass
list_new =[]
file_all = sys.argv[1]
date_now = file_all.split('_')[-1][:-4]
#dirs = '/root/work/other/wenshu/get_data/get_doc_id/data/' + date_now
#if not os.path.exists(dirs):
#    os.makedirs(dirs)
#    for i in range(24):
#        os.makedirs(dirs + "/" + str(i))

id_done = {}
if os.path.exists("log/" + date_now):
    for line in open("log/" + date_now):
        if "-" in line and 'successed' in line:
            id_tmp = line.split(' ')[0].split('_')[0]
            id_done[id_tmp] = 1

for line in open('id/' + file_all):
    id_tmp = line.split(',')[0]
    if  id_done.get(id_tmp,-1) == -1:
        list_new.append(line.strip())
n = 170
sep_data(list_new,n)
time.sleep(5)
for i in range(n):
    time.sleep(2)
    os.system('nohup cat id_sep/%d |python -u get_wenben.py %s >>log/%s 2>>error &'%(i,date_now,date_now))
