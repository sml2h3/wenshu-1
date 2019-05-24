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
import gc
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

date_0 = time.strftime("%Y%m%d_%H", time.localtime(time.time() + 1800))
#if not os.path.exists('data/' + date_0):
#    os.mkdir('data/' + date_0)
list_new =[]
file_all = sys.argv[1]
date_now = file_all.split('_')[-1][:-4]
id_done = {}
id_need_do = {}
if os.path.exists("log/" + date_now):
    for line in open("log/" + date_now):
        if "-" in line and 'successed' in line:
            id_tmp = line.split(' ')[0].split('_')[0]
            id_done[id_tmp] = 1

for line in open('id/' + file_all):
    id_tmp = line.split(',')[0]
    if  id_done.get(id_tmp,-1) == -1:
        id_need_do[line.strip()] = 1
n = 55
list_new = list(id_need_do.keys())[::-1]
sep_data(list_new,n)
list_new=0
id_done=0
id_need_do=0
gc.collect()
time.sleep(20)
crawl_type = 'app'
#crawl_type = 'web'
if crawl_type == 'app':
    for i in range(n):
        time.sleep(1)
        os.system('nohup cat id_sep/%d |python -u get_app_data.py %s >>log/%s 2>>error &'%(i,date_now,date_now))
if crawl_type == 'web':
    for i in range(n):
        time.sleep(1)
        os.system('nohup cat id_sep/%d |python -u get_web_data.py >>log/%s 2>>error &'%(i,date_now))

while True: 
    date_0 = time.strftime("%Y%m%d_%H", time.localtime(time.time() + 1800))
    if os.path.exists('End'):
        break
    #if not os.path.exists('data/' + date_0):
    #    os.mkdir('data/' + date_0)
    time_0 = time.ctime()
    n_success = str(os.popen('cat log/%s|grep successed|wc -l '%date_now).read()).strip()
    n_failed = str(os.popen('cat log/%s|grep failed|wc -l '%date_now).read()).strip()
    n_process = str(os.popen('ps -ef|grep get_app_data|wc -l').read()).strip()
    n_200 = str(os.popen('tail -n 5000 /var/log/squid/access.log |grep /200|wc -l ').read()).strip()
    os.system('echo %s %s %s %s %s >> log/tmp_speed'%(time_0, n_process,  n_success, n_failed, n_200)) 
    for i in range(60):
        # 延时3分钟
        time.sleep(3)
        if os.path.exists('End'):
            break
