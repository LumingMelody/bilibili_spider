import random
from openpyxl import Workbook
import requests

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
    # iPhone 6???
    # "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
]

headers = {
    'User-Agent': random.choice(USER_AGENTS),
    'cookie': "_uuid=D2FF843E-42C8-6D5B-698B-F8E0D70BDA4853737infoc; buvid3=F89283D2-C301-42BB-9978-E604E789C7AE34772infoc; DedeUserID=332587554; DedeUserID__ckMd5=783d9715138b1cf4; fingerprint=699aaf816a2b1ba4713dd5ea2fba467b; fingerprint=89d8878c5aa2d37a5c0369dc18a616fb; buvid_fp=F89283D2-C301-42BB-9978-E604E789C7AE34772infoc; buvid_fp_plain=1BA7E56C-4343-4645-9A91-9A7038A3499D34784infoc; buvid_fp_plain=F89283D2-C301-42BB-9978-E604E789C7AE34772infoc; SESSDATA=9691bd37%2C1640765104%2Cf6479%2A71; bili_jct=4b409bac2340cd5ae864e8014a4250b1; sid=8yru8fjg; _pickup=eyJhbGciOiJIUzI1NiJ9.eyJTSUdORURfQVVESVQiOjIsInByb3h5TmFtZSI6IuS4iua1t-WMoOiwpuenkeaKgOacjeWKoeaciemZkOWFrOWPuDAxLeWVhuWNleiKseeBq-W5s-WPsCIsImRlcGFydG1lbnRJZCI6MTY5LCJpc3MiOiLkuIrmtbfljKDosKbnp5HmioDmnI3liqHmnInpmZDlhazlj7gwMS3llYbljZXoirHngavlubPlj7AiLCJtaWQiOjMzMjU4NzU1NCwiSU5EVVNUUllfQVVESVQiOjIsInR5cGUiOjQsImRlcGFydG1lbnRUeXBlIjo0LCJJU19ORVdfQ1VTVE9NRVIiOjAsIkVOVEVSUFJJU0VfQVVESVQiOjEsIklTX0NPUkVfQUdFTlQiOjEsImV4cCI6MTYyNTgxNzkwNywibWFnaWNfbnVtYmVyIjoiQ09NTUVSQ0lBTE9SREVSIiwiaWF0IjoxNjI1MjEzMTA3LCJqdGkiOiIzNDgyMyIsInByb3h5SWQiOjE5ODU2NDgsIklTX0tBX0FDQ09VTlQiOjB9.kNv00FA-Ep9u0SUV1nbZN8akd7j73JPdghKj3ifwHHY"
}
wb = Workbook()
ws = wb.active
ws.append([
    'UP?????????',
    'UP???ID',
    'UP????????????',
    'UP?????????mcn',
    'UP?????????',
    'UP???URL',
    'UP?????????',
    'UP???????????????',
    'UP???????????????',
    'UP?????????',
    'UP???????????????',
    'UP???????????????',
    'UP???????????????',
    'UP?????????',
    'UP?????????????????????',
    'UP?????????????????????',
    'UP?????????????????????',
    'UP?????????????????????',
    'UP??????????????????',
    'UP??????????????????',
    'UP??????????????????',
    'UP??????????????????',
    'UP??????????????????',
    'UP??????????????????',
    'UP?????????????????????',
    'UP?????????????????????',
    'UP?????????????????????',
    'UP?????????????????????',
    'UP?????????????????????',
    'UP?????????????????????'
])


def get_huohua(h_url):
    resp = requests.get(url=h_url, headers=headers).json()
    results = resp['result']['data']

    for result in results:
        print(result)
        up_tag = ""
        up_user_feature_tags = ""
        up_attention_user_distributed_tags = ""
        up_sax_distributions = ""
        up_original_price = ""
        up_forward_price = ""
        up_age_distributions = ""
        up_device_distributions = ""
        up_top_region_distributions = ""
        up_mcn = ""
        up_mid = result['upper_mid']
        up_mcn_id = result['mcn_id']
        up_url = f"https://space.bilibili.com/{up_mid}"
        up_detail_url = f"https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/portrait?upper_mid=" \
                        f"{up_mid}&mcn_id={up_mcn_id}"
        res = requests.get(url=up_detail_url, headers=headers).json()
        u_result = res['result']
        # up?????????
        up_name = u_result['nickname']
        # up????????????
        up_fans = u_result['fans_num']
        # up??????????????????
        up_fans_like = u_result['fans_like_num']
        # up????????????
        up_video_num = u_result['video_num']
        # up?????????
        up_signature = u_result['signature']
        # up?????????
        up_gender = u_result['gender_desc']
        # up???????????????
        up_region_desc = u_result['region_desc']
        # up???????????????
        up_second_region = u_result['second_region_desc']
        # up?????????
        up_partition = u_result['partition_name']
        # up???????????????
        up_second_partition = u_result['second_partition_name']
        # up?????????
        up_tags = u_result['tags']
        for tag in up_tags:
            up_tag += tag
        upper_prices = u_result['upper_prices']
        # print(len(upper_prices))
        # up???????????????
        up_implantation_price = upper_prices[0]['platform_price']
        # up???????????????
        up_customized_price = upper_prices[1]['platform_price']
        for upper_price in upper_prices:
            # up?????????????????????
            if upper_price['cooperation_type_desc'] == "????????????":
                up_original_price = upper_price['platform_price']
            # up?????????????????????
            if upper_price['cooperation_type_desc'] == "????????????":
                up_forward_price = upper_price['platform_price']
        # up??????????????????
        up_average_play = u_result['average_play_cnt']
        # up??????????????????
        up_average_comment = u_result['average_comment_cnt']
        # up??????????????????
        up_average_collect = u_result['average_collect_cnt']
        # up??????????????????
        up_average_like = u_result['average_like_cnt']
        # up???????????????
        up_average_barrage = u_result['average_barrage_cnt']
        # up??????????????????
        up_average_interactive = u_result['average_interactive_rate']
        # up?????????mcn
        if "mcn_company_name" in u_result.keys():
            up_mcn = u_result['mcn_company_name']
        # up?????????????????????
        up_attention_user_feature_tags = u_result['attention_user_feature_tags']
        for u in up_attention_user_feature_tags:
            up_user_feature_tags += u
        # up???????????????????????????
        attention_user_distributed_tags = u_result['attention_user_distributed_tags']
        for a in attention_user_distributed_tags:
            up_attention_user_distributed_tags += a
        # up?????????????????????
        sax_distributions = u_result['sax_distributions']
        for sax in sax_distributions:
            section_desc = sax['section_desc']
            count = sax['count']
            sax_result = str(section_desc) + "???????????????" + str(count)
            up_sax_distributions += sax_result
            up_sax_distributions = "".join(str(i) for i in up_sax_distributions)
        # up???????????????
        age_distributions = u_result['age_distributions']
        for age in age_distributions:
            section_desc = age['section_desc']
            count = age['count']
            age_result = str(section_desc) + "????????????:" + str(count)
            up_age_distributions += age_result
            up_age_distributions = "".join(str(i) for i in up_age_distributions)
        # up?????????????????????
        device_distributions = u_result['device_distributions']
        for device in device_distributions:
            section_desc = device['section_desc']
            count = device['count']
            device_result = str(section_desc) + "????????????:" + str(count)
            up_device_distributions += device_result
            up_device_distributions = "".join(str(i) for i in up_device_distributions)
        # up?????????????????????
        top_region_distributions = u_result['top_region_distributions']
        for region in top_region_distributions:
            section_desc = region['section_desc']
            count = region['count']
            region_result = str(section_desc) + "??????????????????:" + str(count)
            up_top_region_distributions += region_result
            up_top_region_distributions = "".join(str(i) for i in up_top_region_distributions)
        ws.append([
            up_name, up_mid, up_fans, up_mcn, up_signature, up_url, up_gender, up_region_desc, up_second_region,
            up_partition, up_second_partition, up_fans_like, up_video_num, up_tag, up_implantation_price,
            up_customized_price, up_original_price, up_forward_price, up_average_play, up_average_comment,
            up_average_collect, up_average_like, up_average_barrage, up_average_interactive, up_user_feature_tags,
            up_attention_user_distributed_tags, up_sax_distributions, up_age_distributions, up_device_distributions,
            up_top_region_distributions
        ])
        wb.save(r"D:\bilibili\bilibli_07_02\huahuo_test.xlsx")


if __name__ == '__main__':
    # ???????????????
    min_fans = 1000000
    # ???????????????
    max_fans = 2000000
    # ??????
    type = 1
    for page in range(2):  # rang???????????????
        page += 1
        url = f"https://huahuo.bilibili.com/commercialorder/api/web_api/v1/advertiser/search?region_id=&second_region_id=&partition_id=&second_partition_id=&nickname=&upper_mid=&task_type=1&order_bys=&is_include_potential_upper=0&min_fans_num={min_fans}&max_fans_num={max_fans}&content_tag_id={type}&style_tag_id=0&provider_id=&cooperation_types=&min_task_price=&max_task_price=&male_attention_user_rates=&female_attention_user_rates=&attention_user_ages=&attention_user_regionIds=&bus_type=&gender=&page={page}&size=10"
        get_huohua(url)
