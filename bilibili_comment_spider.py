import random
import json
import time
import pandas as pd
from openpyxl import Workbook

import requests

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
    'cookie': "_uuid=19E3D158-5C4C-5313-15F4-D0E0652B856B61295infoc; buvid3=BA6017C5-E479-4596-97FA-EF03FC1E1435185012infoc; buvid_fp=BA6017C5-E479-4596-97FA-EF03FC1E1435185012infoc; LIVE_BUVID=AUTO8616167213810503; fingerprint=3057ac8ee6ac336ca85353bf3ade1252; buvid_fp_plain=7E65C238-AD53-4548-A5A5-AB7C47EE239D185015infoc; SESSDATA=a050ad08%2C1632555146%2C8004d%2A31; bili_jct=b82a7d19334d1f1cbbc1d74982f871e4; DedeUserID=20221702; DedeUserID__ckMd5=d6786b5d622ed8dc; sid=dbdf5h6y; CURRENT_FNVAL=80; blackside_state=1; bsource=search_baidu; PVID=1",
}


wb = Workbook()
ws = wb.active
ws.append([
    "用户名",
    "性别",
    "签名",
    "评论内容"
])


def get_comment(b_url, oid):
    response = requests.get(url=b_url, headers=headers).json()
    print(b_url)
    time.sleep(2)
    if response:
        # print(response)
        data = response["data"]
        print(data)
        # print(data)
        # replies = data["replies"]
        count = data['page']['count']
        if count % 20 == 0:
            page_count = int(count / 20)
        else:
            page_count = int((count / 20) + 1)
            for page in range(page_count+1):
                # print(page)
                n_url = f"https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={page+1}&type=1&oid={oid}&sort=2"
                resp = requests.get(n_url, headers).json()
                time.sleep(3)
                result = resp["data"]
                print(result)
                if result['replies'] is not None:
                    replies = result["replies"]
                    if replies is not None:
                        for reply in replies:
                            content = reply["content"]["message"]
                            # print(content)
                            user_name = reply["member"]["uname"]
                            gender = reply["member"]["sex"]
                            sign = reply["member"]["sign"]
                            ws.append([user_name, gender, sign, content])
                    else:
                        return "所有评论抓取完成"
    wb.save(r"D:\bilibili\bilibili_08_27\小米平板5_comment.xlsx")


if __name__ == '__main__':
    # oid可以用Chrome F12抓到获取
    df = pd.read_excel(r"D:\bilibili\bilibili_08_30\bili_urls.xlsx")
    oids = df['oid']
    for oid in oids:
        url = f"https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid={oid}&sort=2"
        get_comment(url, oid)
        # time.sleep(3)
