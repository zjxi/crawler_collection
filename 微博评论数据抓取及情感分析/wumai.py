import requests
from lxml import etree
import time
from urllib import parse
import xlwt
import threading
import pandas as pd


class Thread (threading.Thread):
    def __init__(self, region):
        threading.Thread.__init__(self)
        self.region = region

    def run(self):  # 线程体
        self.region = str(self.region).replace('\n', '')
        try:
            max_page = get_total_pages(get_url(1, self.region + '雾霾'))
            for i in range(1, int(max_page)+1):
                print(f'---{self.region}---正在爬取第{i}页数据---')
                get_main_data(get_url(i, self.region + '雾霾'), self.region)
            # to_excel(f'{self.region}雾霾话题—微博.csv')
            df = pd.DataFrame(info_list)
            df.to_csv('雾霾话题—微博.csv', index=False, encoding='utf_8_sig')
            print(f'{self.region}爬取结束！')
        except Exception as e:
            # to_excel(f'{self.region}雾霾话题—微博.csv')
            df = pd.DataFrame(info_list)
            df.to_csv('雾霾话题—微博.csv', index=False, encoding='utf_8_sig')
            print(f'{self.region}数据获取失败！', e)


# 获取单个页数页面的url
def get_url(page, city):
    param = {'q': city}
    parser = parse.urlencode(param)

    url = 'https://s.weibo.com/weibo?' + parser + '&nodup=1&page={}'.format(str(page))

    headers = {
        'Host': 's.weibo.com',
        'Cookie': 'SINAGLOBAL=4570002959653.581.1547617397438; UOR=www.spss.com.cn,widget.weibo.com,www.baidu.com; wvr=6; ALF=1597716462; SSOLoginState=1566180462; SCF=AmE2sfIHrRxxsL-bm2788o6oicC2jEhXXziT4E1aBUPEzgjAt903HdHADCkQZu6jXaNHs8H742dtQr63UoBsn2A.; SUB=_2A25wXnQ_DeRhGeRI4lIS8i_JwzyIHXVTKuL3rDV8PUNbmtANLRjzkW9NUsjyDEQ3SOnQCgBBqZr009JWk20G8Mpv; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh9DWTmbmK8RElKnBY8SAOP5JpX5KzhUgL.Fozc1K50eo2f1h52dJLoI7U8MJLoCGSD; SUHB=0tKrKmJYxuVVmf; _s_tentry=login.sina.com.cn; Apache=1687362249267.157.1566180487915; ULV=1566180487923:11:3:2:1687362249267.157.1566180487915:1566107000472; webim_unReadCount=%7B%22time%22%3A1566221380081%2C%22dm_pub_total%22%3A377%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D; WBStorage=5bb151908a2d8e92|undefined',
        'Referer': 'https://s.weibo.com/weibo?' + parser + '&nodup=1&page={}'.format(str(int(page) - 1)),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.110 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'
    }
    proxy = {
        'https': '218.108.175.15:80'
    }

    req = requests.get(url=url, headers=headers)
    req.encoding = 'utf-8'
    return req.text


# 通过主页面，进入二级页面，获取单个用户的url
def get_personal_url(person_src):
    headers = {
        'Host': 'weibo.com',
        'Cookie': 'SINAGLOBAL=4570002959653.581.1547617397438; UOR=www.spss.com.cn,widget.weibo.com,www.baidu.com; wvr=6; Ugrow-G0=140ad66ad7317901fc818d7fd7743564; ALF=1597716462; SSOLoginState=1566180462; SCF=AmE2sfIHrRxxsL-bm2788o6oicC2jEhXXziT4E1aBUPEzgjAt903HdHADCkQZu6jXaNHs8H742dtQr63UoBsn2A.; SUB=_2A25wXnQ_DeRhGeRI4lIS8i_JwzyIHXVTKuL3rDV8PUNbmtANLRjzkW9NUsjyDEQ3SOnQCgBBqZr009JWk20G8Mpv; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh9DWTmbmK8RElKnBY8SAOP5JpX5KzhUgL.Fozc1K50eo2f1h52dJLoI7U8MJLoCGSD; SUHB=0tKrKmJYxuVVmf; YF-V5-G0=d30fd7265234f674761ebc75febc3a9f; _s_tentry=login.sina.com.cn; Apache=1687362249267.157.1566180487915; ULV=1566180487923:11:3:2:1687362249267.157.1566180487915:1566107000472; wb_view_log_2690321580=1536*8641.25; webim_unReadCount=%7B%22time%22%3A1566185664909%2C%22dm_pub_total%22%3A377%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D; YF-Page-G0=89906ffc3e521323122dac5d52f3e959|1566185678|1566185678',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.110 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    data = {
        'refer_flag': '1001030103_',
        'is_hot': '1'
    }
    proxy = {
        'https': '183.129.207.80:12926'
    }
    resp = requests.get(url=person_src, headers=headers, data=data)
    resp.encoding = 'utf-8'
    # print('****正在进入二级页面****')
    return resp.text


# 获取‘更多’，进入三级页面的URL
def get_more_url(more_info_url):
    headers = {
        'Host': 'weibo.com',
        'Cookie': 'SINAGLOBAL=4570002959653.581.1547617397438; UOR=www.spss.com.cn,widget.weibo.com,www.baidu.com; wvr=6; Ugrow-G0=140ad66ad7317901fc818d7fd7743564; ALF=1597716462; SSOLoginState=1566180462; SCF=AmE2sfIHrRxxsL-bm2788o6oicC2jEhXXziT4E1aBUPEzgjAt903HdHADCkQZu6jXaNHs8H742dtQr63UoBsn2A.; SUB=_2A25wXnQ_DeRhGeRI4lIS8i_JwzyIHXVTKuL3rDV8PUNbmtANLRjzkW9NUsjyDEQ3SOnQCgBBqZr009JWk20G8Mpv; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh9DWTmbmK8RElKnBY8SAOP5JpX5KzhUgL.Fozc1K50eo2f1h52dJLoI7U8MJLoCGSD; SUHB=0tKrKmJYxuVVmf; YF-V5-G0=d30fd7265234f674761ebc75febc3a9f; _s_tentry=login.sina.com.cn; Apache=1687362249267.157.1566180487915; ULV=1566180487923:11:3:2:1687362249267.157.1566180487915:1566107000472; wb_view_log_2690321580=1536*8641.25; YF-Page-G0=7f483edf167a381b771295af62b14a27|1566184854|1566184820; webim_unReadCount=%7B%22time%22%3A1566185334405%2C%22dm_pub_total%22%3A377%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.110 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    proxy = {
        'https': '183.129.207.80:12926'
    }
    resp = requests.get(url=more_info_url, headers=headers)
    resp.encoding = 'utf-8'
    print('****正在进入三级页面****')
    return resp.text


# 获取页面的最大页数
def get_total_pages(text):
    html = etree.HTML(text)
    max_page = html.xpath("//div[@class='m-page']//ul[@class='s-scroll']/li[last()]//text()")[0]
    max_page = str(max_page).replace('第', '').replace('页', '')
    return max_page.strip()


def clean_forward(data):  # 清洗文本，获取纯数字
    data = str(data).replace('转发', '').strip()
    return data


def clean_comment(data):  # 清洗文本，获取纯数字
    data = str(data).replace('评论', '').strip()
    return data


def clean_space(data):  # 清除空格
    return str(data).strip()


info_list = []


# 获取主页面的所需信息
def get_main_data(text, city):
    # 设置同步锁，防止资源掠夺
    # lock = threading.RLock()
    # lock.acquire()

    html = etree.HTML(text)
    divs = html.xpath("//div[@class='card-wrap']")
    for div in divs:
        try:  # 用户昵称
            nick_name = div.xpath(".//p[@node-type='feed_list_content']/@nick-name")[0]
        except Exception as e:
            nick_name = ''
            print('用户昵称-获取异常：', e)
        try:  # 微博内容
            content = div.xpath(".//p[@node-type='feed_list_content']//text()")
            content = str(content).replace(' ', '').replace('[', '').replace(']', '').replace('\\n', '')
            if str(content).__contains__('展开全文'):
                content = div.xpath(".//p[@node-type='feed_list_content_full']//text()")
                content = str(content).replace(' ', '').replace('[', '').replace(']', '').replace('\\n', '')
        except Exception as e:
            print('微博内容-获取异常：', e)
        try:  # 微博的发布时间
            send_time = div.xpath(".//p[@class='from']/a[1]/text()")[0]
        except Exception as e:
            send_time = ''
            print('发布时间-获取异常：', e)
        try:  # 来自手机等型号信息
            from_type = div.xpath(".//p[@class='from']/a[2]/text()")[0]
        except Exception as e:
            from_type = ''
            print('来自信息-获取异常：', e)
        try:
            # 该微博的转发数量
            forward = div.xpath(".//div[@class='card-act']//li[2]//text()")[0]
        except Exception as e:
            forward = ''
            print('转发量-获取异常：', e)
        try:
            # 该微博的评论数
            comment = div.xpath(".//div[@class='card-act']//li[3]//text()")[0]
        except Exception as e:
            comment = ''
            print('评论数-获取异常：', e)
        try:
            # 该微博的点赞数
            likes = div.xpath(".//div[@class='card-act']//li[4]//text()")[0]
        except Exception as e:
            likes = ''
            print('点赞数-获取异常：', e)

        # 获取单个用户的url
        # person_src = div.xpath(".//div[@class='info']/div[2]/a/@href")[0]
        # person_src = 'https:' + person_src
        # print(get_personal_url(person_src))
        # # 二级页面，获得当前用户所有基本信息
        # try:
        #     person_info_dict = get_personal_info(get_personal_url(person_src))
        # except Exception as e:
        #     print('二级页面的返回的dict获取失败！', e)
        # follow = person_info_dict['关注']
        # fans = person_info_dict['粉丝']
        # weibo_num = person_info_dict['微博']
        # loc = person_info_dict['所在地']
        # sex = person_info_dict['性别']
        # desc = person_info_dict['简介']
        # reg = person_info_dict['注册时间']
        # other = person_info_dict['其他信息']

        info = {
            '省市': city,
            '用户昵称': nick_name,
            # '性别': sex,
            # '所在地': loc,
            # '注册时间': reg,
            # '简介': desc,
            '微博内容': content,
            '发表时间': clean_space(send_time),
            '来自': from_type,
            '转发数': clean_forward(forward),
            '评论数': clean_comment(comment),
            '点赞数': likes,
            # '关注数': follow,
            # '粉丝数': fans,
            # '微博数': weibo_num,
            # '其他信息': other
        }
        info_list.append(info)
        print(info)
        # 设置延时
        time.sleep(2)
        # lock.release()


# 获取二级页面，当前用户下的‘关注’，‘粉丝’，‘微博’信息
def get_personal_info(text):
    html = etree.HTML(text)
    try:
        # 用户的关注量
        follow = html.xpath("//div[@class='WB_innerwrap']//tr/td[2]//strong/text()")[0]
    except Exception as e:
        follow = ''
        print('二级页面-用户关注量-获取异常：', e)
    try:
        # 用户的粉丝量
        follower = html.xpath("//div[@class='WB_innerwrap']//tr/td[2]//strong/text()")[0]
    except Exception as e:
        follower = ''
        print('二级页面-用户粉丝量-获取异常：', e)
    try:
        # 用户的微博量
        weibo_num = html.xpath("//div[@class='WB_innerwrap']//tr/td[3]//strong/text()")[0]
    except Exception as e:
        weibo_num = ''
        print('二级页面-用户微博量-获取异常：', e)

    # 获取并拼接“更多”信息点击的url
    # try:
    #     more_info_url = html.xpath("//div[@class='PCD_person_info']/a[@class='WB_cardmore S_txt1 S_line1 clearfix']/@href")
    #     more_info_url = 'https://weibo.com' + more_info_url
    #     print('三级页面url:', more_info_url)
    # except Exception as e:
    #     print('获取更多url失败！！！', e)
    #
    # # 调用方法，获取“更多”页面下的基本信息字典
    # basic_info_dict = get_basic_info(get_more_url(more_info_url))
    # # 分别获取相关具体信息
    # loc = basic_info_dict['所在地']
    # sex = basic_info_dict['性别']
    # desc = basic_info_dict['简介']
    # reg = basic_info_dict['注册时间']

    person_info = {
        # '所在地': loc,
        # '性别': sex,
        # '简介': desc,
        # '注册时间': reg,
        '关注': follow,
        '粉丝': follower,
        '微博': weibo_num,
    }
    time.sleep(1)
    return person_info


# 三级页面，获取当前用户的更多信息
def get_basic_info(text):
    html = etree.HTML(text)
    try:
        # 用户的位置信息
        location = html.xpath("//div[@id='Pl_Official_PersonalInfo__57']/div[1]//li[2]/span[2]/text()")[0]
    except Exception as e:
        location = ''
        print('三级页面-用户位置信息-获取异常：', e)
    try:
        # 用户的性别信息
        sex = html.xpath("//div[@id='Pl_Official_PersonalInfo__57']/div[1]//li[3]/span[2]/text()")[0]
    except Exception as e:
        sex = ''
        print('三级页面-用户性别信息-获取异常：', e)
    try:
        # 用户的个人说明介绍
        description = html.xpath("//div[@id='Pl_Official_PersonalInfo__57']/div[1]//li[4]/span[2]/text()")[0]
    except Exception as e:
        description = ''
        print('三级页面-用户个人说明介绍-获取异常：', e)
    try:
        # 用户的注册时间
        register_time = html.xpath("//div[@id='Pl_Official_PersonalInfo__57']/div[1]//li[last()]/span[2]/text()")[0]
    except Exception as e:
        register_time = ''
        print('三级页面-用户注册时间-获取异常：', e)

    # 其他信息
    try:
        other_info = html.xpath("//div[@id='Pl_Official_PersonalInfo__57']"
                                "/div[position()>1]//ul[@class='clearfix']//text()")[0]
    except Exception as e:
        other_info = ''
        print('三级页面-其他信息-获取异常：', e)

    basic_info = {
        '所在地': location,
        '性别': sex,
        '简介': description,
        '注册时间': clean_space(register_time),
        '其他信息': other_info
    }
    time.sleep(1)
    return basic_info


def to_excel(filename):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('雾霾-微博话题', cell_overwrite_ok=True)
    # col = ('省市', '用户昵称', '性别', '所在地', '注册时间', '简介', '微博内容','发表时间',
    #        '来自', '转发数', '评论数', '点赞数', '关注数', '粉丝数', '微博数', '其他信息')
    col = ('省市', '用户昵称', '微博内容', '发表时间', '来自', '转发数', '评论数', '点赞数', )
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(len(info_list)):
        data = info_list[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[col[j]])
    book.save(filename)


def main():
    with open('region.txt', 'r', encoding='utf-8') as fr:
        regions = fr.readlines()
        for region in regions:
            thread = Thread(region)  # 开启线程
            thread.start()


if __name__ == '__main__':
    main()









