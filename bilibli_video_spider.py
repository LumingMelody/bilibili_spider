import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
import gevent
import gevent.pool
import requests

import random
# from bs4 import BeautifulSoup


# start = '20201231'
# end = '20210218'
# date_list = [x for x in pd.date_range(start, end).strftime('%Y-%m-%d')]
# url_list = []
# for date in date_list:
#     url = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=283851334&date={}'.format(date)
#     url_list.append(url)
from gevent import monkey
from lxml import etree
from openpyxl import Workbook
import asyncio

monkey.patch_socket()

sys.setrecursionlimit(1000000)

wb = Workbook()

ws = wb.active
ws1 = wb.create_sheet()

ws.append(
    [
        # "UP昵称",
        # "粉丝数",
        # "性别",
        # "签名",
        "视频类型",
        "视频标题",
        "视频发布时间",
        "视频播放量",
        "视频弹幕数量",
        "视频评论回复数量",
        "视频收藏数",
        "视频硬币数",
        "视频点赞数",
        "视频分享数",
        "全站最高排名",
    ]
)


USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
]


headers = {
    'User-Agent': random.choice(USER_AGENTS),
    'cookie': "_uuid=19E3D158-5C4C-5313-15F4-D0E0652B856B61295infoc; buvid3=BA6017C5-E479-4596-97FA-EF03FC1E1435185012infoc; buvid_fp=BA6017C5-E479-4596-97FA-EF03FC1E1435185012infoc; LIVE_BUVID=AUTO8616167213810503; fingerprint=3057ac8ee6ac336ca85353bf3ade1252; buvid_fp_plain=7E65C238-AD53-4548-A5A5-AB7C47EE239D185015infoc; SESSDATA=a050ad08%2C1632555146%2C8004d%2A31; bili_jct=b82a7d19334d1f1cbbc1d74982f871e4; DedeUserID=20221702; DedeUserID__ckMd5=d6786b5d622ed8dc; sid=dbdf5h6y; CURRENT_FNVAL=80; blackside_state=1; bsource=search_baidu; PVID=1"
}

# 代理服务器
proxyHost = "forward.apeyun.com"
proxyPort = "9082"
# 代理隧道验证信息
proxyUser = "2021040800226731834"
proxyPass = "pA7prxttyuCTFjwM"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}


# oid可以用Chrome F12抓到获取
# url = "https://api.bilibili.com/x/v1/dm/list.so?oid=119278568"
# INDEX_URL = 'https://search.bilibili.com/all?keyword={keyword}&page={page}'


def get_content(b_url):
    resp = requests.get(url=b_url, headers=headers)
    # print(proxies)
    html = resp.content.decode("utf-8")
    html_node = etree.HTML(html)
    script_data = html_node.xpath('//script[contains(text(),"window.__INITIAL_STATE__")]/text()')[0]
    article = script_data.replace(
        'window.__INITIAL_STATE__=', '').replace(
        ';(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.rem'
        'oveChild(s);}());', '').replace("False", "1").replace("True", "0").replace("None", "1")
    json_data = json.loads(article)
    # print(json_data)
    try:
        # UP主信息
        # up_info = json_data['upData']
        # # UP主名字
        # up_name = up_info['name']
        # # UP主粉丝数
        # up_fans = up_info['fans']
        # # UP主性别
        # up_gender = up_info['sex']
        # # UP主签名
        # up_sign = up_info['sign']

        # 视频相关信息
        video_info = json_data['videoData']
        print(video_info)
        # 视频分类
        video_type = video_info['tname']
        # 视频标题
        video_title = video_info['title']
        # 视频描述
        video_desc = video_info['desc']
        # 视频发布时间
        video_create_time = video_info['pubdate']
        timeArray = time.localtime(video_create_time)
        video_create_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # 视频播放量
        video_play = video_info['stat']['view']
        # 视频弹幕数量
        video_danmu = video_info['stat']['danmaku']
        # 视频评论回复数量
        video_reply = video_info['stat']['reply']
        # 视频收藏数
        video_favorite = video_info['stat']['favorite']
        # 视频硬币数
        video_coin = video_info['stat']['coin']
        # 视频点赞数
        video_like = video_info['stat']['like']
        # 视频分享数
        video_share = video_info['stat']['share']
        # 全站最高排名
        video_his_rank = video_info['stat']['his_rank']
        related = json_data['related']
        print([video_type, video_title, video_create_time, video_play, video_danmu, video_reply, video_favorite,
               video_coin, video_like, video_share, video_his_rank])
        # ws.append(
        #     [up_name, up_fans, up_gender, up_sign, video_type, video_title, video_create_time, video_play, video_danmu,
        #      video_reply, video_favorite, video_coin, video_like, video_share, video_his_rank])
        ws.append(
            [video_type, video_title, video_create_time, video_play, video_danmu,
             video_reply, video_favorite, video_coin, video_like, video_share, video_his_rank])
        wb.save(r'D:\bilibili\bilibli_07_21\bili_07_21_五菱汽车.xlsx')
    # process_list = []
    # pool = gevent.pool.Pool(100)
    # for j in related:
    #     n_url = f"https://www.bilibili.com/video/{j['bvid']}"
    #     print(n_url)
    #     # process_list.append(n_url)
    #     # pool.map(get_content, process_list)
    #     get_content(n_url)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # pool = ProcessPoolExecutor(10)
    for i in range(1, 5):
        video_list_url = f"https://api.bilibili.com/x/space/arc/search?mid=439868658&ps=30&tid=0&pn={i}&keyword=&order=pubdate&jsonp=jsonp"
        resp = requests.get(video_list_url, headers=headers).json()
        video_list = resp['data']['list']['vlist']
        for video in video_list:
            bvid = video['bvid']
            url = f"https://www.bilibili.com/video/{bvid}"
    # # for url in urls:
            get_content(url)
            time.sleep(2)
    # pool.submit(get_content, str(url))
    # time.sleep(2)
    # pool.shutdown(wait=True)
