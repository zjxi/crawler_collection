import requests
from lxml import etree
import time
from urllib import parse
import threading
import pandas as pd


# class Thread(threading.Thread):
#     def __init__(self):
#     # self.region = region
#     pass
#
#     def run(self):
#         for i in range(50):
#             text = self.request_url(f'https://s.weibo.com/user?q=&auth=ord&region=custom:11:1000&page={i+1}')
#             self.extract_user_id(text)
#
#     def request_url(self, url):
#         headers = {
#             'Host': 's.weibo.com',
#             'Cookie': 'SINAGLOBAL=4570002959653.581.1547617397438; UOR=www.spss.com.cn,widget.weibo.com,www.baidu.com; wvr=6; login_sid_t=f06bc7463106ddc896d39a3f979f4633; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=7108743734008.756.1566388805911; ULV=1566388805919:12:4:3:7108743734008.756.1566388805911:1566180487923; SCF=AmE2sfIHrRxxsL-bm2788o6oicC2jEhXXziT4E1aBUPE-_5Qq9WhOAdTVBRMFYcgXpuZbP1AgEB9CiItoDPhCSo.; SUB=_2A25wWULiDeRhGeRI4lIS8i_JwzyIHXVTLzMqrDV8PUNbmtB-LWPmkW9NUsjyDBcxrY-1MpK3xnboK6H5Apcp_tJs; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh9DWTmbmK8RElKnBY8SAOP5JpX5KzhUgL.Fozc1K50eo2f1h52dJLoI7U8MJLoCGSD; SUHB=0N20AfH7J0MQhg; ALF=1597924913; SSOLoginState=1566388914; webim_unReadCount=%7B%22time%22%3A1566391990577%2C%22dm_pub_total%22%3A377%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                           'Chrome/70.0.3538.110 Safari/537.36',
#             'Upgrade-Insecure-Requests': '1'
#         }
#         req = requests.get(url, headers=headers)
#         req.encoding = 'utf-8'
#         return req.text
#
#     def request_user_url(self, url):
#         headers = {
#             'Host': 'weibo.com',
#             'Cookie': 'SINAGLOBAL=4570002959653.581.1547617397438; UOR=www.spss.com.cn,widget.weibo.com,www.baidu.com; wvr=6; Ugrow-G0=1ac418838b431e81ff2d99457147068c; login_sid_t=f06bc7463106ddc896d39a3f979f4633; cross_origin_proto=SSL; YF-V5-G0=4358a4493c1ebf8ed493ef9c46f04cae; _s_tentry=passport.weibo.com; wb_view_log=1536*8641.25; Apache=7108743734008.756.1566388805911; ULV=1566388805919:12:4:3:7108743734008.756.1566388805911:1566180487923; SCF=AmE2sfIHrRxxsL-bm2788o6oicC2jEhXXziT4E1aBUPE-_5Qq9WhOAdTVBRMFYcgXpuZbP1AgEB9CiItoDPhCSo.; SUB=_2A25wWULiDeRhGeRI4lIS8i_JwzyIHXVTLzMqrDV8PUNbmtB-LWPmkW9NUsjyDBcxrY-1MpK3xnboK6H5Apcp_tJs; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh9DWTmbmK8RElKnBY8SAOP5JpX5KzhUgL.Fozc1K50eo2f1h52dJLoI7U8MJLoCGSD; SUHB=0N20AfH7J0MQhg; ALF=1597924913; SSOLoginState=1566388914; wb_view_log_2690321580=1536*8641.25; YF-Page-G0=afcf131cd4181c1cbdb744cd27663d8d|1566392565|1566392559; webim_unReadCount=%7B%22time%22%3A1566392565693%2C%22dm_pub_total%22%3A377%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A377%2C%22msgbox%22%3A0%7D',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                           'Chrome/70.0.3538.110 Safari/537.36',
#             'Upgrade-Insecure-Requests': '1'
#         }
#         req = requests.get(url, headers=headers)
#         req.encoding = 'utf-8'
#         return req.text
#
#     def extract_user_id(self, text):
#         html = etree.HTML(text)
#         divs = html.xpath("//div[@class='card-wrap']")
#         for div in divs:
#             uid = div.xpath(".//div[@class='info']/div/a[3]/@uid")[0]
#             info_list.append(uid)
#             print(uid)
#
#     def extract_user_url(self, text, region):
#         html = etree.HTML(text)
#         divs = html.xpath("//div[@class='card-wrap']")
#         for div in divs:
#             user_url = div.xpath(".//div[@class='info']/div/a/@href")[0]
#             user_url = 'https:' + user_url
#             user_name = div.xpath(".//div[@class='info']/div/a/text()")[0]
#             self.extract_weibo_url(self.request_user_url(user_url), region, user_name)
#
#     def extract_weibo_url(self, text, region, user_name):
#         html = etree.HTML(text)
#         weibo_url = html.xpath("//div[@class='PCD_counter']//td[3]/a/@href")[0]
#         weibo_url = 'https:' + weibo_url
#         self.extract_content(self.request_user_url(weibo_url), region, user_name)
#
#     def extract_content(self, text, region, user_name):
#         html = etree.HTML(text)
#         try:
#             max_page = div("//div[@class='WB_cardwrap S_bg2']//ul/li[1]/a/text()")[0]
#             max_page = str(max_page).replace(' ', '').replace('第', '').replace('页', '')
#         except Exception as e:
#             print(f'获取-最大页数-失败:', e)
#         divs = html.xpath("//div[@class='WB_feed WB_feed_v3 WB_feed_v4']")
#         for div in divs:
#             try:  # 发布时间
#                 send_time = div.xpath("./div[@class='WB_cardwrap WB_feed_type S_bg2 WB_feed_like ']"
#                                       "//div[@class='WB_detail']/div[@class='WB_from S_txt2']/a[1]/text()")[0]
#             except Exception as ex:
#                 print(f'发布时间获取失败！', ex)
#                 send_time = ''
#             try:  # 来自
#                 from_type = div.xpath("./div[@class='WB_cardwrap WB_feed_type S_bg2 WB_feed_like ']"
#                                       "//div[@class='WB_detail']/div[@class='WB_from S_txt2']/a[2]/text()")[0]
#             except Exception as ex:
#                 print(f'来自获取失败！', ex)
#                 from_type = ''
#             try:  # 微博内容
#                 content = div.xpath("./div[@class='WB_cardwrap WB_feed_type S_bg2 WB_feed_like ']"
#                                     "//div[@class='WB_detail']/div[@node-type='feed_list_content']//text()")
#                 if str(content).__contains__('展开全文'):
#                     content = div.xpath("./div[@class='WB_cardwrap WB_feed_type S_bg2 WB_feed_like ']"
#                                         "//div[@class='WB_detail']/div[@node-type='feed_list_content_full']//text()")
#             except Exception as e:
#                 print(f'微博内容获取失败！', e)
#                 content = ''
#             try:  # 转发量
#                 shares = \
#                 div.xpath("./div[@class='WB_cardwrap WB_feed_type S_bg2 WB_feed_like ']/div[@class='WB_feed_handle']"
#                           "//ul[@class='WB_row_line WB_row_r4 clearfix S_line2']/li[2]//text()")[0]
#             except Exception as e:
#                 print(f'分享量获取失败！', e)
#                 shares = ''
#             try:  # 评论量
#                 comments = \
#                 div.xpath("./div[@class='WB_cardwrap WB_feed_type S_bg2 WB_feed_like ']/div[@class='WB_feed_handle']"
#                           "//ul[@class='WB_row_line WB_row_r4 clearfix S_line2']/li[3]//text()")[0]
#             except Exception as e:
#                 print(f'分享量获取失败！', e)
#                 comments = ''
#             try:  # 点赞量
#                 likes = \
#                 div.xpath("./div[@class='WB_cardwrap WB_feed_type S_bg2 WB_feed_like ']/div[@class='WB_feed_handle']"
#                           "//ul[@class='WB_row_line WB_row_r4 clearfix S_line2']/li[4]//text()")[0]
#             except Exception as e:
#                 print(f'分享量获取失败！', e)
#                 likes = ''
#
#             info = {
#                 '地区': region,
#                 '发布时间': send_time,
#                 '来自': from_type,
#                 '转发量': shares,
#                 '评论量': comments,
#                 '点赞量': likes,
#                 '微博内容': content
#             }
#             info_list.append(info)
#             print(info)
#             time.sleep(2)


def request_url(url):
    headers = {
        'Host': 's.weibo.com',
        'Cookie': 'SINAGLOBAL=4570002959653.581.1547617397438; UOR=www.spss.com.cn,widget.weibo.com,login.sina.com.cn; TC-V5-G0=0dba63c42a7d74c1129019fa3e7e6e7c; WBStorage=f54cf4e4362237da|undefined; login_sid_t=7c0a10e2b16b1fca08e63748cab99ab4; cross_origin_proto=SSL; Ugrow-G0=cf25a00b541269674d0feadd72dce35f; _s_tentry=weibo.com; wb_view_log=1536*8641.25; Apache=7425834238884.023.1567082761408; ULV=1567082761420:17:9:1:7425834238884.023.1567082761408:1566529036414; SCF=AmE2sfIHrRxxsL-bm2788o6oicC2jEhXXziT4E1aBUPEcDr9VmX2cSlMIR4klMDvqAWRY_QtHvcwou-FVd6bNYw.; SUB=_2A25wY7kUDeRhGeRI4lIS8i_JwzyIHXVTGK3crDV8PUNbmtAKLUnxkW9NUsjyDIdsqprdb3UcxqKi9V5mkfmRB-s3; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh9DWTmbmK8RElKnBY8SAOP5JpX5KzhUgL.Fozc1K50eo2f1h52dJLoI7U8MJLoCGSD; SUHB=0rr6WycApejIHw; ALF=1598618819; SSOLoginState=1567082820; wvr=6; wb_view_log_2690321580=1536*8641.25; TC-Page-G0=7a922a70806a77294c00d51d22d0a6b7|1567083110|1567083110; webim_unReadCount=%7B%22time%22%3A1567083112816%2C%22dm_pub_total%22%3A377%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.110 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'
    }
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    return req.text


def extract_user_id(text, region):
    html = etree.HTML(text)
    divs = html.xpath("//div[@class='m-wrap']//div[@class='card card-user-b s-pg16 s-brt1']")
    for div in divs:
        try:
            uid = div.xpath(".//div[@class='info']/div/a[@class='s-btn-c']/@uid")[0]
            # name = div.xpath(".//div[@class='info']/div/a[@class='name']/text()")[0]
        except Exception as e:
            print(e)
        # info_list.append(uid + ',%s' % region)
        info_list.append(uid)
        print(uid, region)


info_list = []

region = {
    34: '安徽', 11: '北京', 50: '重庆', 35: '福建', 62: '甘肃', 44: '广东',
    45: '广西', 52: '贵州', 46: '海南', 13: '河北', 23: '黑龙江', 41: '河南',
    42: '湖北', 43: '湖南', 15: '内蒙古', 32: '江苏', 36: '江西', 22: '吉林',
    21: '辽宁', 64: '宁夏', 63: '青海', 14: '山西', 37: '山东', 31: '上海',
    51: '四川', 12: '天津', 54: '西藏', 65: '新疆', 53: '云南', 33: '浙江',
    61: '陕西', 71: '台湾', 81: '香港', 82: '澳门'
}


def main():
    for k, v in region.items():
        for i in range(50):
            text = request_url(f'https://s.weibo.com/user?q=&auth=ord&region=custom:{k}:1000&page={i + 1}')
            extract_user_id(text, v)
            time.sleep(1)
    df = pd.DataFrame(info_list)
    df.to_csv('uids.csv', encoding='utf-8', index=None)


if __name__ == '__main__':
    main()

