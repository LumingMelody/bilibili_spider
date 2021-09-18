import json
import time
from concurrent.futures import ProcessPoolExecutor

import requests
import random
# from bs4 import BeautifulSoup
import re
import re  # 正则表达式库
import collections  # 词频统计库
import numpy as np  # numpy数据处理库
import jieba  # 结巴分词
import wordcloud  # 词云展示库
from PIL import Image  # 图像处理库
import matplotlib.pyplot as plt  # 图像展示库

# start = '20201231'
# end = '20210218'
# date_list = [x for x in pd.date_range(start, end).strftime('%Y-%m-%d')]
# url_list = []
# for date in date_list:
#     url = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=283851334&date={}'.format(date)
#     url_list.append(url)
from lxml import etree
from openpyxl import Workbook

wb = Workbook()

ws = wb.active
ws1 = wb.create_sheet()

ws.append(
    [
        "视频类型",
        "视频ID",
        "视频链接",
        "标题",
        "视频简介",
        "视频图片链接",
        "视频播放数",
        "视频弹幕数",
        "视频收藏数",
        "视频评论数",
        "标签",
        "视频时长",
        "发布时间",
        "发布时间戳",
        "用户名",
        "用户ID",
        "用户链接",
        "用户关注数",
        "用户粉丝数",
    ]
)

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

headers = {
    'User-Agent': random.choice(USER_AGENT),
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
    res = requests.get(url=b_url, headers=headers, proxies=proxies)
    print(proxies)
    html = res.content.decode("utf-8")
    html_node = etree.HTML(html)
    script_data = html_node.xpath('//script[contains(text(),"window.__INITIAL_STATE__")]/text()')[0]
    article = script_data.replace(
        'window.__INITIAL_STATE__=', '').replace(
        ';(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.rem'
        'oveChild(s);}());', '').replace("False", "1").replace("True", "0").replace("None", "1")
    user_json = json.loads(article)
    print(user_json)
    results = user_json['flow']['getSingleTypeList-jump-keyword-小细跟-search_type-video']['result']
    try:
        for result in results:
            video_type = result['typename']
            video_id = result['aid']
            video_url = result['arcurl']
            video_title = re.sub(r'<.*?>', '', result['title'])
            video_desc = result['description']
            video_pic = "https:" + result['pic']
            video_play = result['play']
            video_review = result['video_review']
            video_coll = result['favorites']
            video_comment = result['review']
            video_tag = result['tag']
            video_time = result['duration']
            video_ts = result['pubdate']
            video_post_time = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(result['pubdate']))
            user_name = result['author']
            user_id = result['mid']
            user_url = "https://space.bilibili.com/{}".format(user_id)
            user_json_url = "https://api.bilibili.com/x/web-interface/card?mid={}&jsonp=jsonp&article=true".format(user_id)
            rs = requests.get(user_json_url, headers=headers).json()
            print(rs)
            fans = str(rs['data']['card']['fans'])
            follows = str(rs['data']['card']['attention'])
            ws.append(
                [video_type, video_id, video_url, video_title, video_desc, video_pic, video_play, video_review, video_coll,
                 video_comment, video_tag, video_time, video_post_time, video_ts, user_name, user_id, user_url, follows,
                 fans])
            time.sleep(2)
    except Exception as e:
        print(e)
    # wb.save('D:/bilibili/bili_0527_小细跟.xlsx')
    #     print(e)
    # for i in result:
    #     # result.remove(i[0])
    #     # print(type(i))
    #     if type(i) == str:
    #         print(i)
    #         with open("D:/bilibili/bilibli3.txt", "a", encoding="utf-8") as f:
    #             f.write(i)
    #             f.write("\n")


# def world_cloud(file_path):
#     fn = open(file_path, "r", encoding="utf-8")
#     string_data = fn.read()
#     fn.close()
#     # 文本预处理
#     pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
#     string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除
#     seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词
#     object_list = []
#     remove_words = [u"的", u"我", u"吧", u"了", u"是", u"在", u"，", u"。", u"！", u"？", u"《", u"》", u"]", u"[", u"R", u"用"]
#     for word in seg_list_exact:  # 循环读出每个分词
#         if word not in remove_words:  # 如果不在去除词库中
#             object_list.append(word)  # 分词追加到列表
#
#     # 词频统计
#     word_counts = collections.Counter(object_list)  # 对分词做词频统计
#     word_counts_top10 = word_counts.most_common(10)  # 获取前10最高频的词
#     print(word_counts_top10)  # 输出检查
#     word_counts_top10 = str(word_counts_top10)
#
#     # 词频展示
#     mask = np.array(Image.open('D:/bilibili/img.png'))  # 定义词频背景
#     wc = wordcloud.WordCloud(
#         font_path='simfang.ttf',  # 设置字体格式
#         mask=mask,  # 设置背景图
#         max_words=200,  # 最多显示词数
#         max_font_size=150,  # 字体最大值
#         background_color='white',
#         width=800, height=600,
#     )
#
#     wc.generate_from_frequencies(word_counts)  # 从字典生成词云
#     plt.imshow(wc)  # 显示词云
#     plt.axis('off')  # 关闭坐标轴
#     plt.show()  # 显示图像
#     wc.to_file('D:/bilibili/爱乐薇.png')


if __name__ == '__main__':
    # file_path = "D:/bilibili/爱乐薇.txt"
    # pool = ProcessPoolExecutor(10)
    # for i in range(7):
    #     url = f"https://search.bilibili.com/video?keyword=小细跟&page={i + 1}"
    url = "https://www.bilibili.com/video/BV1xK4y1X79x?spm_id_from=333.851.b_7265636f6d6d656e64.5"
    get_content(url)
    # pool.submit(get_content, str(url))
    time.sleep(2)
    # pool.shutdown(wait=True)
    # world_cloud(file_path)
    # start_time = time.time()
