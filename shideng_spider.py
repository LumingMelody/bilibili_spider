import json
import random
import time

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
    'cookie': "sign_val=baac4a1fbedc496d7a9012d5322e9869; source=1; Hm_lvt_8732c75af60700696c14686fb85b09b2=1618383603,1618450626; top=0; vtoken=uct14Z%252FxXBsANF4Dg5Td6qrFPrxVd61yzpm7McS44w%252FPpALodJuIiwbgg%252F7XaL0QC%252BpZxL507RcN5frXqbeGfsG35qtqJtKrmp4F74gnst8Fmzg%252B7WPImYzo0lpaqo4K3YoUaoqNH8zsDCuQcV%252BkfP2m9QhUbOiTQ%252FbaocwaXolmG3F6%252BEZ9sXYozhkEKJivazVMNZwhe8dPx3E1oPdJQLvAh1sUw7p4gFBKRUeZ9aV8qNcnYN7gkzvTx0Sl2UbB; headimageurl=https%3A//aldpicsh-1252823355.cossh.myqcloud.com/video/user/headImg/20210414/161838480206i.jpg; phone=****; nickname=%u10DA%u850D%u9E23%u10DA; Hm_lpvt_8732c75af60700696c14686fb85b09b2=1618451534",
    "content-type": "application/json",
}
headers2 = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    'cookie': "sign_val=baac4a1fbedc496d7a9012d5322e9869; source=1; Hm_lvt_8732c75af60700696c14686fb85b09b2=1618383603,1618450626; vtoken=uct14Z%252FxXBsANF4Dg5Td6qrFPrxVd61yzpm7McS44w%252FPpALodJuIiwbgg%252F7XaL0QC%252BpZxL507RcN5frXqbeGfsG35qtqJtKrmp4F74gnst8Fmzg%252B7WPImYzo0lpaqo4K3YoUaoqNH8zsDCuQcV%252BkfP2m9QhUbOiTQ%252FbaocwaXolmG3F6%252BEZ9sXYozhkEKJivazVMNZwhe8dPx3E1oPdJQLvAh1sUw7p4gFBKRUeZ9aV8qNcnYN7gkzvTx0Sl2UbB; headimageurl=https%3A//aldpicsh-1252823355.cossh.myqcloud.com/video/user/headImg/20210414/161838480206i.jpg; phone=****; nickname=%u10DA%u850D%u9E23%u10DA; Hm_lpvt_8732c75af60700696c14686fb85b09b2=1618465442; top=0",
    "content-length": "490",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://shidengdata.com",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-site": "same-site"
}
# "date": "2021-03",
url = "https://wwwapi.shidengdata.com/pc/monthRank/list"
data = {
    "date": "2021-03",
    "category_id": 0,
    "category": "总榜",
    "page": 1,
    "size": 10,
    "sign_val": "baac4a1fbedc496d7a9012d5322e9869",
    "token": "uct14Z%2FxXBsANF4Dg5Td6qrFPrxVd61yzpm7McS44w%2FPpALodJuIiwbgg%2F7XaL0QC%2BpZxL507RcN5frXqbeGfsG35qtqJtKrmp4F74gnst8Fmzg%2B7WPImYzo0lpaqo4K3YoUaoqNH8zsDCuQcV%2BkfP2m9QhUbOiTQ%2FbaocwaXolmG3F6%2BEZ9sXYozhkEKJivazVMNZwhe8dPx3E1oPdJQLvAh1sUw7p4gFBKRUeZ9aV8qNcnYN7gkzvTx0Sl2UbB",
}
user_name = ""

data2 = {
    "token": "lsDFa5H0YY%2BLO1xlU4L%2BsCY254%2BLQe5z7mRJluTgmk7t%2FadfMRCD2dMdQB7w2K%2Bswh2qPqprMw3MwY0A3kKuCd341rz87cydrBJmIGQb7kXrdVsH5xKmM6Fq2Z776xF5yAhi5c6SX3OshmrYpsJjBNBvtd7uepZS%2FaaiM3gp5%2BIvyIe3dSqekQkvsGO8xxLvF2O%2B4lzkvwT2PtNUqUmpgUMfrTcSovvJ%2B39AOTVLF34%2FYm9Sbaz28WRYvHvJ9ZpB",
    "ald_id": "",
    "str_type": "78PigJYiGT7q89aK748IafiBXkLztLg42JoZJ8SBNJux6QYHM9UMN5MGQqyJvUWqgUqSXvs%2FsLdEBAW%2FwYPZuA%3D%3D",
    "sign_val": "dce6666d0b6a43abfc1aece88bb33f71"
}

wb = Workbook()
ws = wb.active
ws.append([
    "微信名",
    "微信头像",
    "最高获赞",
    "总评论",
])


def get_comment(d_url):
    response = requests.post(url=d_url, headers=headers, data=data).json()
    if response:
        print(response)
        d_list = response["data"]["list"]
        print(d_list)

        for d in d_list:
            name = d["name"]
            head_pic = d["wx_head_url"]
            # max_like = d["max_likes"]
            avg_like = d["avg_likes"]
            comment_summary = d["comment_summary"]
            ald_id = d["ald_id"]
            data2["ald_id"] = ald_id
            # print(data2)
            # rsp = requests.get(url="https://shidengdata.com/vdetails?id=273a7dbd16bf8de632b4da222114ccbf",
            #                    headers=headers2, data=data2).json()
            # print(rsp)
            ws.append([name, head_pic, avg_like, comment_summary])
        wb.save("D:/bilibili/shideng2-4-14.xlsx")


if __name__ == '__main__':
    # for j in ["dayRank", "ranking", "monthRank"]:
    #     url.format(j)
    for i in range(3):
        data["page"] = i + 1
        get_comment(url)
        time.sleep(3)

