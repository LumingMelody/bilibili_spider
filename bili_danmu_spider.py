# -*- coding = utf-8 -*-
# @Time: 2021/2/18 10:59
# @Auther: luming
# @File: B站.py
# @Software: PyCharm

import requests
import random
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import threading
import queue
import pymongo

start = '20201231'
end = '20210218'
date_list = [x for x in pd.date_range(start, end).strftime('%Y-%m-%d')]
url_list = []
for date in date_list:
    url = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=283851334&date={}'.format(date)
    url_list.append(url)

USER_AGENT = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
]
user_agent = random.choice(USER_AGENT)
headers = {
    'User-Agent': user_agent,
    'cookie': "_uuid=34ACBA34-03DD-81AA-6CAC-F33D00D3C74163588infoc; buvid3=2BDB8C60-1CDD-4B10-9568-AEFC038707E4138384infoc; sid=9gh59bea; DedeUserID=162908107; DedeUserID__ckMd5=2ea1fddf76014573; SESSDATA=b0db349e%2C1618572887%2Cad8e8*a1; bili_jct=5290e8016acb744b893f3f89c21ffff2; LIVE_BUVID=AUTO6916030209297118; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(um~kmu))k|0J'uY|J))YluJ; fingerprint3=747574fae5a412761591446c90163fdf; buvid_fp_plain=2BDB8C60-1CDD-4B10-9568-AEFC038707E4138384infoc; buivd_fp=2BDB8C60-1CDD-4B10-9568-AEFC038707E4138384infoc; PVID=1; bsource=search_baidu; buvid_fp=2BDB8C60-1CDD-4B10-9568-AEFC038707E4138384infoc; fingerprint=ec81492c55a05ba0ed410e591b59428f; fingerprint_s=39be7e6ca7f35a48e7e16afb9927b904; bfe_id=fdfaf33a01b88dd4692ca80f00c2de7f; bp_video_offset_162908107=492966450637890747; bp_t_offset_162908107=492966450637890747",
}


class crawl_and_parse:
    def __init__(self, url_queue, lock, danmu_path):
        self.url_queue = url_queue
        self.lock = lock
        self.danmu_path = danmu_path

    def spider(self):
        '''
        输入：url_queue.get()
        --------------------------
        爬取：requests.get
        解析：re正则表达式语法
        --------------------------
        返回一个列表文件danmu_list
        '''
        self.lock.acquire()
        url = self.url_queue.get()
        self.lock.release()
        danmu_list = []
        collection_name = url.split('=')[-1]
        danmu_list.append(collection_name)
        req = requests.get(url, headers=headers)
        resp = req.text
        soup = BeautifulSoup(resp, 'lxml')
        search_path = re.compile(':(.*?)@')
        datas = re.findall(search_path, soup.text)
        for data in datas:
            data = data.strip('\r')
            data = data.strip('\n')
            data = data.strip('\t')
            data = data.strip('-')
            data = data.strip('*')
            data = data.strip('$')
            data = data.strip('+')
            data = data.strip()
            danmu_list.append(data)
        return danmu_list


class spider(threading.Thread):
    def __init__(self, url_queue, lock, *args, **kwargs):
        super(spider, self).__init__(*args, **kwargs)
        self.url_queue = url_queue
        self.lock = lock

    def run(self):
        while True:
            if self.url_queue.empty() == True:
                break
            danmu_list = crawl_and_parse.spider()
            save_mongodb.saveData(danmu_list)


class save_mongodb:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://127.0.0.1:27017')  # 访问端口

    def saveData(self, danmu_list):
        global danmu_number
        # 创建名叫bilibili的数据库，下面的集合名分别为历史弹幕的日期
        collection = self.client["bilibili"]["{}".format(danmu_list[0])]
        del danmu_list[0]
        data = {}
        for id, danmu in enumerate(danmu_list):
            data['_id'] = id + 1
            data['弹幕'] = danmu
            collection.insert_one(data)
            danmu_number += 1


if __name__ == '__main__':
    start_time = time.time()
    thread_list = []
    danmu_path = re.compile(':(.*?)@')
    danmu_number = 0
    url_queue = queue.Queue(100)
    lock = threading.Lock()
    crawl_and_parse = crawl_and_parse(url_queue, lock, danmu_path)
    save_mongodb = save_mongodb()

    for url in url_list:
        url_queue.put(url)

    for i in range(len(url_list)):
        th = spider(url_queue, lock, name="爬虫线程%d" % (i + 1))
        thread_list.append(th)

    for l in thread_list:
        l.setDaemon(True)
        l.start()
        l.join()

    print('弹幕总数量为：%d' % danmu_number)
    end_time = time.time()
    print('it costs {}s'.format(end_time - start_time))
