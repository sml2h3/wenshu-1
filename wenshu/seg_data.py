#!/usr/bin/python
#-*- coding:utf-8 -*-
"""wish no bug"""
############################
#File Name: work_0.py
#Author: zhangyang
#Mail: ass7798@qq.com
#Created Time: 2019-03-02 19:12:24
############################
#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Wind'
"""Wish No Bug"""
import time
import os
import re
import sys
def test_text(text):
    # 按照文书正文长度来过滤空文档
    content = text
    if "{" not in content:
        return -1
    
    if "� ！" in content:
        return -1
    
    if len(content.split('"PubDate"')) == 1:
        return -1

    if len(content) < 200:  # 如果控制在 200 以内，则仅过滤掉有问题的文书；如果控制在 400 以内，则会将”法院认为不宜公开的文书“及”以调节方式结案的文书“（同样不包含实质性内容）都去掉。

        content_splited = content.split('"PubDate"')

        # 如果拆分之后依然只有一个部分，则必然是出错了
        if len(content_splited) == 1:
            # 标记回传文书出错
            doc_error_tag = 1
            return -1

        else:
            content_judge = content_splited[1]
            content_judge = re.sub('\s', '', content_judge)  # 将所有空白字符删除掉

            # 情形1: 如果属于 当事人申请不公开及个人隐私，则是正常文书
            if len(re.findall('>当事人申请不公开<|隐私', content_judge)) > 0:
                return 1

            # 情形2: 如果属于 当事人申请不公开，则是正常文书
            if len(re.findall('敏感案件', content_judge)) > 0:
                return 1


            # 情形3: 如果属于 人民法院认为不宜在互联网公布的其他情形，则是正常文书
            elif len(re.findall('>人民法院.*不宜.*<|不宜?上网|不.*公[布开]', content_judge)) > 0:
                return 1

            # 情形4: 如果属于 以调解方式结案的，则是正常文书
            elif len(re.findall('>以调解方式结案的<', content_judge)) > 0:
                return 1

            # 情形5: 如果属于 确认人民调解协议效力的，则是正常文书
            elif len(re.findall('>确认人民调解协议效力的<', content_judge)) > 0:

                return 1

            # 情形6: 如果属于 离婚诉讼或者涉及未成年子女抚养、监护的，则是正常文书
            elif len(re.findall('>离婚诉讼或者涉及未成年子女抚养、监护的<', content_judge)) > 0:
                return 1

            # 情形7: 如果属于 涉及国家秘密的，则是正常文书
            elif len(re.findall('>涉及国家秘密的<', content_judge)) > 0:
                return 1

            # 情形8: 如果属于 未成年人犯罪的，则是正常文书
            elif len(re.findall('>未成年人犯罪的<', content_judge)) > 0:
                return 1


            # 情形9: 如果属于 结案文书为通知书，则是正常文书
            elif len(re.findall('>结案文书为通知书<', content_judge)) > 0:
                return 1

            # 情形10: 如果属于 撤诉，则是正常文书
            elif len(re.findall('>.*撤诉.*<', content_judge)) > 0:
                return 1

            # 情形11: 如果属于 撤诉，则是正常文书
            elif len(re.findall('>.*撤诉.*<', content_judge)) > 0:
                return 1

            # 情形12: 如果属于 其他，则是正常文书
            elif len(re.findall('>其他', content_judge)) > 0:
                return 1

            # 剩余情形，必是回传文书出错，标记之
            return -1
    return 1


# path_0 = r"F:/wenshu/wenben/201903"
#file_list = os.listdir(path_0)  # 给出文件夹中的文件名列表
count = 0
list_tmp = ['','']
i  = 0
error  =0
dic_0 ={}
file_0 = "doc_id_data/"
os.chdir(file_0)
file_1 = sys.argv[1]
#file_0 = time.strftime("%Y%m%d_%H/", time.localtime())
if not os.path.exists(file_1 + '/' ):
    os.mkdir(file_1 + "/")
os.chdir(file_1 + "/")
#print(os.getcwd())
for line in sys.stdin:
    if line.strip() == "##########":
        if count == 2:
            result  = test_text(list_tmp[1])
            if result == 1:
                w=open(list_tmp[0],'w')
                w.write(list_tmp[1] + "\n")
                w.close()
                i+= 1
            else:
                error += 1
        list_tmp = ['','']
        count = 1
        continue
    if count == 1:
        list_tmp[0] = line.strip()
        count = 2
        continue
    if count == 2:
        list_tmp[1] += line.strip()
        continue

print(time.ctime(),file_1,i,error )
'''
            if count > 1:
                result  = test_text(list_tmp[1])
                if result == 1:
                    w = open('F:/wenshu/wenben/json/' + list_tmp[0].replace("\"",''),'w', encoding='UTF-8')
                    w.write(list_tmp[1])
                    w.close()
                    i += 1
                else:
                    pass
            list_tmp[0] = line.strip()
            list_tmp[1] = ''
            count += 1
        else:
            list_tmp[1] += line.strip()
    print(count,i)
'''
'''
    if "{" in line:
        list_tmp[1] = line
        print(list_tmp)
    else:
        list_tmp[0] = line
    if count == 0:
        list_tmp[0] = line
        if len(line) > 100 or len(line) <5:
            print(i,len(line))
            break
        
    if count == 1:
        text = line
        result  = test_text(text)
        if result == 1:
            list_tmp[1] = line.strip()
            try:
                w = open('tmp/' + list_tmp[0],'w')
                w.write(list_tmp[1])
                w.close()
            except:
                #print(i)
                pass
        else:
            #print(error, i,list_tmp[0],len(text))
            error += 1
            pass
    count += 1
    count = count % 2
print(i, error)
'''
