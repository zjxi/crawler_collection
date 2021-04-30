import requests
from lxml import etree
import pandas as pd
import time

_COOKIE = 'UM_distinctid=16f8fa24e76803-0ddd1c7d340683-6701b35-144000-16f8fa24e77498; SINAGLOBAL=4427183000823.765.1578662776664; UOR=www.baidu.com,vdisk.weibo.com,www.baidu.com; wb_view_log=1536*8641.25; wb_view_log_2690321580=1536*8641.25; wvr=6; Ugrow-G0=5c7144e56a57a456abed1d1511ad79e8; YF-V5-G0=8c4aa275e8793f05bfb8641c780e617b; _s_tentry=login.sina.com.cn; Apache=5693463038441.978.1592979782107; ULV=1592979782143:9:2:2:5693463038441.978.1592979782107:1592977767780; SCF=AqEpi4aCCyuklPGcTpgZM7ijPmQViiJ7tQPuhY4btC-8hCCNJdCYohZH2zE59vOabubi_q3RHykqhU9pawNwrn0.; SUB=_2A25z9oZTDeRhGeRI4lIS8i_JwzyIHXVQhfCbrDV8PUNbmtAKLUGskW9NUsjyDHuNwjRFeSVOUqwGZG41zKkXwwYz; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh9DWTmbmK8RElKnBY8SAOP5JpX5KMhUgL.Fozc1K50eo2f1h52dJLoI7U8MJLoCGSD; SUHB=04WvdKNodgcdH-; ALF=1624516992; SSOLoginState=1592980995; YF-Page-G0=d30fd7265234f674761ebc75febc3a9f|1592985083|1592985083; webim_unReadCount=%7B%22time%22%3A1592985118491%2C%22dm_pub_total%22%3A377%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D'

def request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.110 Safari/537.36',
        'Cookie': _COOKIE,
        'Host': 'weibo.com',
        'Upgrade-Insecure-Requests': '1'
    }
    resp = requests.get(url, headers)
    resp.encoding = 'utf-8'
    return resp.text


def extract_comments(text):
    html = etree.HTML(text)
    divs = html.xpath("//div")
    print(divs)


if __name__ == '__main__':
    url = 'https://weibo.com/2970452952/J4WSRjSgH?filter=hot&root_comment_id=0&type=comment&User-Agent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML%2C+like+Gecko)+Chrome%2F70.0.3538.110+Safari%2F537.36&Cookie=UM_distinctid%3D16f8fa24e76803-0ddd1c7d340683-6701b35-144000-16f8fa24e77498%3B+SINAGLOBAL%3D4427183000823.765.1578662776664%3B+UOR%3Dwww.baidu.com%2Cvdisk.weibo.com%2Cwww.baidu.com%3B+wb_view_log%3D1536*8641.25%3B+wb_view_log_2690321580%3D1536*8641.25%3B+wvr%3D6%3B+Ugrow-G0%3D5c7144e56a57a456abed1d1511ad79e8%3B+YF-V5-G0%3D8c4aa275e8793f05bfb8641c780e617b%3B+_s_tentry%3Dlogin.sina.com.cn%3B+Apache%3D5693463038441.978.1592979782107%3B+ULV%3D1592979782143%3A9%3A2%3A2%3A5693463038441.978.1592979782107%3A1592977767780%3B+SCF%3DAqEpi4aCCyuklPGcTpgZM7ijPmQViiJ7tQPuhY4btC-8hCCNJdCYohZH2zE59vOabubi_q3RHykqhU9pawNwrn0.%3B+SUB%3D_2A25z9oZTDeRhGeRI4lIS8i_JwzyIHXVQhfCbrDV8PUNbmtAKLUGskW9NUsjyDHuNwjRFeSVOUqwGZG41zKkXwwYz%3B+SUBP%3D0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh9DWTmbmK8RElKnBY8SAOP5JpX5KMhUgL.Fozc1K50eo2f1h52dJLoI7U8MJLoCGSD%3B+SUHB%3D04WvdKNodgcdH-%3B+ALF%3D1624516992%3B+SSOLoginState%3D1592980995%3B+YF-Page-G0%3Db1c63e15d8892cdaefd40245204f0e21|1592984233|1592984147%3B+webim_unReadCount%3D{%22time%22%3A1592984697795%2C%22dm_pub_total%22%3A377%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2}&Host=weibo.com'
    print(request(url))
