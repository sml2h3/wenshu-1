#!/usr/bin/pthon
# -*- coding: utf-8 -*- 
__author__ = 'Wind'
"""Wish No Bug"""
import uuid
import datetime
import requests
import json
import hashlib
import random
import time
import os
import sys

#proxy = {'http': "http://106.12.34.123:7798"}
proxy = {'http': "http://localhost:7798"}
s = requests.session()
s.keep_alive =False
class wenshu(object):
    def __init__(self, proxy):
        self.proxy = proxy
        self.time_validate = 0
        self.empty_count  = 0

    def devid(self):
        devid = str(uuid.uuid1()).replace('-', '')
        return devid

    def timespan(self):
        timespan = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return timespan

    def nonce(self):
        nonce = []
        s = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v',
             'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in range(0, 4):
            a = random.choice(s)
            nonce.append(a)
        non = str(nonce).replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace(" ", "")
        return non

    def signature(self, timespan, nonce, devid):
        s = timespan + nonce + devid
        mid = hashlib.md5(s.encode(encoding='utf-8')).hexdigest()
        return mid

    def user_agent(self):
        user_agent = ['Dalvik/2.1.0 (Linux; U; Android 6.0.1; VTR-AL00 Build/V417IR)',
                      'Dalvik/2.1.0 (Linux; U; Android 6.0.1; BLA-AL00 Build/V417IR)',
                      'Dalvik/2.1.0 (Linux; U; Android 6.0.1; BLA-AL00 Build/V417IR)',
                      'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MI 6 Build/V417IR)',
                      'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MI NOTE 3 Build/V417IR)',
                      'Dalvik/1.6.0 (Linux; U; Android 4.4.2; vivo X20A Build/NMF26X)']
        return random.sample(user_agent, 1)[0]

    def headers(self):
        times = self.timespan()
        dev = self.devid()
        nonc = self.nonce()
        toke = self.token()
        headers = {
            'Content-Type': 'application/json',
            'timespan': times,
            'nonce': nonc,
            'devid': dev,
            'signature': self.signature(times, nonc, dev),
            'User-Agent': self.user_agent(),
            'Host': 'wenshuapp.court.gov.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            # 'Content-Length': '60'

        }

    def token(self):
        times = self.timespan()
        dev = self.devid()
        nonc = self.nonce()
        url = 'http://wenshuapp.court.gov.cn/MobileServices/GetToken'
        user_agent = ['Dalvik/2.1.0 (Linux; U; Android 6.0.1; VTR-AL00 Build/V417IR)',
                      'Dalvik/2.1.0 (Linux; U; Android 6.0.1; BLA-AL00 Build/V417IR)',
                      'Dalvik/2.1.0 (Linux; U; Android 6.0.1; BLA-AL00 Build/V417IR)',
                      'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MI 6 Build/V417IR)',
                      'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MI NOTE 3 Build/V417IR)',
                      'Dalvik/1.6.0 (Linux; U; Android 4.4.2; vivo X20A Build/NMF26X)']
        headers = {
            'Content-Type': 'application/json',
            'timespan': times,
            'nonce': nonc,
            'devid': dev,
            'signature': self.signature(times, nonc, dev),
            'User-Agent': self.user_agent(),
            'Host': 'wenshuapp.court.gov.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            # 'Content-Length': '71'
        }
        data = '{"app":"cpws","devid":"%s","apptype":"1"}' % (dev)
        html = requests.post(url=url, headers=headers, data=data, proxies=proxy, timeout=5)
        token = json.loads(html.text)['token']
        return token

    def get_token_headers(self, sep_time=180):
        """
        获取heanders和token, 多次重复使用，如果超过sep_time 秒，才会更新
        :param retry_time:重新连接次数
        :param sep_time
        :return:
        """
        if (time.time() - self.time_validate) <= sep_time:
            pass
        else:
            times = self.timespan()
            dev = self.devid()
            nonc = self.nonce()
            url = 'http://wenshuapp.court.gov.cn/MobileServices/GetToken'
            headers = {
                'Content-Type': 'application/json',
                'timespan': times,
                'nonce': nonc,
                'devid': dev,
                'signature': self.signature(times, nonc, dev),
                'User-Agent': self.user_agent(),
                'Host': 'wenshuapp.court.gov.cn',
                #'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                # 'Content-Length': '71'
            }
            data = '{"app":"cpws","devid":"%s","apptype":"1"}' % (dev)
            html = requests.post(url=url, headers=headers, data=data, proxies=proxy, timeout=5)
            token = json.loads(html.text)['token']
            self.time_validate = time.time()
            self.toke = token
            self.header = headers
        return self.header, self.toke


    def get_test(self):
        count = 0
        fail_count = 0
        headers, toke = self.get_token_headers()
        print(toke)
        time.sleep(1)
        headers, toke = self.get_token_headers(sep_time=0)
        success_count  = 0
        print(toke)
        while count < 300:
            count += 1
            fail_count += 1

            try:
                time.sleep(2)
                # if True:
                # url='http://wenshuapp.court.gov.cn/MobileServices/GetAddCountAndTotalAndPVCount'
                url = 'http://wenshuapp.court.gov.cn/MobileServices/GetLawListData'
                if fail_count > 10:
                    sep_time = 0
                    fail_count = 0
                else:
                    sep_time = 180
                headers, toke = self.get_token_headers(sep_time=sep_time)
                # data='{"app":"cpws","reqtoken":"%s"}' % toke
                if success_count == 0:
                    data = '{"dicval":"asc","reqtoken":"%s","condition":"/CaseInfo/案/@法院名称=* AND ' \
                           '/CaseInfo/案/@案件类型=1 AND /CaseInfo/案/@审判程序=一审 AND ' \
                           '/CaseInfo/案/@裁判日期=[2018-12-01 TO 2019-02-07]"' \
                           ',"skip":"0","app":"cpws","limit":"20","dickey":"/CaseInfo/案/@法院层级"}' % toke
                else:
                    data = '{"dicval":"asc","reqtoken":"%s","condition":"/CaseInfo/案/@法院名称=* AND ' \
                           '/CaseInfo/案/@案件类型=1 AND /CaseInfo/案/@审判程序=一审 AND ' \
                           '/CaseInfo/案/@裁判日期=[2017-12-01 TO 2018-02-07]"' \
                           ',"skip":"0","app":"cpws","limit":"20","dickey":"/CaseInfo/案/@法院层级"}' % toke
                data = data.encode('utf-8')
                html = requests.post(url=url, headers=headers, data=data, timeout=5, proxies=self.proxy)
                # print(count, toke, html.text)
                if html.text == '':
                    # print('html.text=null')
                    continue
                elif 'Request Error' in html.text:
                    # print('Request Error')
                    continue
                elif html.status_code != 200:
                    continue
                fail_count = 0
                #return 1
                success_count += 1
            except Exception as e:
                print(e)


    def stare_request(self, data_0):
        # data为请求的参数情况
        i = 0
        length = -1
        count = 0
        success_count = 0
        while count <= 150 and success_count < 1:
            # 150次请求不成功就放弃
            count += 1
            self.empty_count += 1
            try:
                time.sleep(1)
                if self.empty_count < 5:
                    sep_time = 180
                else:
                    sep_time = 1
                    self.empty_count = 0
                headers, toke = self.get_token_headers(sep_time)

                """{"dicval":"asc","reqtoken":"2515cd1c6e2069c883ac6a5bf81c006c","condition":"/CaseInfo/案/案由/查询案由/@案由ID=002001001* AND /CaseInfo/案/@法院层级=4 AND /CaseInfo/案/@审判程序=一审 AND /CaseInfo/案/@文书类型=* AND /CaseInfo/案/@裁判日期=[2019-01-01 TO 2019-01-03]","skip":"0","app":"cpws","limit":"20","dickey":"/CaseInfo/案/@法院层级"}"""
                #data = '{"dicval":"asc","reqtoken":"%s",' % toke
                #data = '{"app":"cpws","reqtoken":"'
                data = ',"app":"cpws","reqtoken":"%s"}'% toke
                data = data_0 + data
                data = data.encode('utf-8')
                url = 'http://wenshuapp.court.gov.cn/MobileServices/GetAllFileInfoByIDNew'
                html = requests.post(url=url, headers=headers, data=data, timeout=6, proxies=proxy)
                #print(data)
                #print(count,self.empty_count,toke,html.status_code,html.text)
                if html.text == '':
                    continue
                elif 'Request Error' in html.text:
                    continue
                elif html.status_code != 200:
                    continue
                success_count += 1
                times = headers['timespan']
                nonc = headers['nonce']
                dev = headers['devid']
                list_result = list(
                    map(str, [time.time(), count, success_count, toke, times, dev, nonc, html.text.strip("\"")]))
                i += 20
                self.empty_count = 0
            except Exception as e:
                #print(e)
                continue
        if count > 150:
            list_result = list(map(str, ["failed", time.time(), count, success_count, ]))
        return list_result

    def get_request_data(self,sep_time, court_name, type_wenshu, shenpan_chengxu):
        str_0 = '"condition":"/CaseInfo/案/@法院名称=*%s* ' % court_name
        str_1 = 'AND /CaseInfo/案/@案件类型=%s ' % str(type_wenshu)
        str_2 = 'AND /CaseInfo/案/@审判程序=%s ' % shenpan_chengxu
        str_3 = 'AND /CaseInfo/案/@裁判日期=[%s]"' % sep_time
        str_4 = ',"skip":"0","app":"cpws","limit":"20","dickey":"/CaseInfo/案/@法院层级"}'
        str_all = str_0 + str_1 + str_2 + str_3 + str_4
        return str_all

    def get_doc_data(self,doc_id):
        data_0 = '{"fileId":"%s"'%doc_id
        return self.stare_request(data_0)

if __name__ == '__main__':
    wenshu_0 = wenshu(proxy=proxy)
    '''
    print(wenshu_0.get_token_headers())
    print(wenshu_0.get_test())
    '''
    date_now = sys.argv[1]
    begin_time = time.time()
    print("begin is:",begin_time)
    #court_name, type_wenshu, shenpan_chengxu = sys.argv[1:]
    #all_time = open("all_time").read().strip().split('\n')
    #wenshu_0.get_wenshu_data_quick(court_name, type_wenshu, shenpan_chengxu, all_time)
    for line in sys.stdin:
        if os.path.exists('End'):
            break
        time_begin_0 = time.time()
        tmp_0 = line.strip().split(',')
        out_file = "_".join([tmp_0[0]] + tmp_0[2:])
        doc_id = tmp_0[0]
        list_0 = wenshu_0.get_doc_data(doc_id)
        list_0.insert(3, '1984-02-25 TO 2001-08-20')
        str_1 = ' '.join(list_0[:-1]) + "\n"
        str_2 = list_0[-1]
        hour = time.strftime("%H", time.localtime())
        time_end_0 = time.time()
        if list_0[0] != "failed":
            print(out_file,"successed",time_end_0 - time_begin_0)
            w = open('data/' + hour + '/' +out_file, "a+")
            w.write(str_1)
            w.write(str_2)
            w.close()
        else:
            print(out_file,"failed",time_end_0 - time_begin_0)
        #print(" ".join(list_0[:-1]))
        #print(list_0[-1].strip('"'))
    end_time = time.time()
    print("end is:",end_time)
    print("spend time is:",end_time - begin_time)

