"""
written by xizijun @ 2019-3-2 , updated by xizijun @ 2020/3/17
a crawler for the whole detailed information of www.39.net

"""
import requests
from lxml import etree
import xlwt
import time

# 若当前ip长时间爬取过多信息会被反爬机制发现，此时需要更改此处的cookie值，或者使用代理ip
_COOKIE = 'Hm_lvt_eefa4d8db0fa9214fbd06e08764b6cdc=1584447269; Hm_lvt_0711a4f91bc0a9d22a67012693562b07=1584447269; Hm_lvt_9840601cb51320c55bca4fa0f4949efe=1584447269; Hm_lpvt_9840601cb51320c55bca4fa0f4949efe=1584447481; Hm_lpvt_0711a4f91bc0a9d22a67012693562b07=1584447481; Hm_lpvt_eefa4d8db0fa9214fbd06e08764b6cdc=1584447481'


# 请求体
def req_headers(url):
    headers = {
        'Host': 'jbk.39.net',
        'Cookie': _COOKIE,
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/70.0.3538.110 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    return resp.text


# 二级链接请求体
def hosp_req_headers(url):
    headers = {
        'Cookie': _COOKIE,
        'Host': 'yyk.39.net',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/70.0.3538.110 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'gbk'
    return resp.text


# 不同科室的url参数
section = ['fuke', 'nanke', 'neike', 'waike', 'pifuke', 'wuguanke']


def get_all_url(pg):
    url = 'http://www.39.net/bw/p' + str(pg)
    return url


def get_section_url(sec):
    url = 'http://www.39.net/bw/' + sec
    return url


def get_spec_url(url, pg):
    spec_url = url + '_p{}/'.format(str(pg))
    return spec_url


def get_other_url(other_src):
    return other_src


def html_parser(text):
    html = etree.HTML(text)
    return html


# 解析并提取所需的主要疾病信息
def get_all_content(htm):
    html = html_parser(htm)
    divs = html.xpath("//div[@class='result_item']")

    for div in divs:
        title = div.xpath(".//p[@class='result_item_top_l']/a/@title")[0]
        try:
            nick_name = div.xpath(".//p[@class='result_item_top_l']/i/text()")[0]
        except:
            nick_name = '暂无'
        detail = div.xpath(".//p[@class='result_item_content']/text()")[0]
        related = div.xpath(".//p[@class='result_item_content_label']/a[position()>0]/text()")

        cause_src = div.xpath(".//p[@class='result_item_top_r']/a[1]/@href")[0]
        symptom_src = div.xpath(".//p[@class='result_item_top_r']/a[2]/@href")[0]
        prevent_src = div.xpath(".//p[@class='result_item_top_r']/a[3]/@href")[0]
        hospital_src = div.xpath(".//p[@class='result_item_top_r']/a[4]/@href")[0]
        visit_src = div.xpath(".//p[@class='result_item_top_r']/a[5]/@href")[0]

        cause = get_other_content(cause_src)
        symp = get_other_content(symptom_src)
        pre = get_other_content(prevent_src)
        hosp = get_hosp_info(hospital_src)
        vis = get_visit_info(visit_src)

        add_to_list(title, nick_name, detail, related, cause, symp, pre, hosp, vis)


# 解析并提取所需的其他疾病信息
def get_other_content(cause_src):
    url = get_other_url(cause_src)
    text = req_headers(url)
    html = html_parser(text)
    other = html.xpath("//div[@class='article_paragraph']//text()")
    return other


# 提取推荐医院信息
def get_hosp_info(hosp_src):
    url = get_other_url(hosp_src)
    text = hosp_req_headers(url)
    html = html_parser(text)
    hosp = html.xpath("//div[@class='yy-msg']//a[@class='yy-name']/text()")
    return hosp


# 提取就诊信息
def get_visit_info(vis_src):
    url = get_other_url(vis_src)
    text = req_headers(url)
    html = html_parser(text)
    vis = html.xpath("//div[@class='zn-main']/dl[position()>0]//text()")
    return vis


sick_list = []


# 将解析提取到的数据存入sick_list列表
def add_to_list(title, nick_name, detail, related, cause, symp, pre, hosp, vis):
    sick = {
        '疾病名称': title,
        '别称': nick_name,
        '疾病介绍': detail,
        '相关症状': related,
        '病因': cause,
        '症状': symp,
        '预防': pre,
        '找医院': hosp,
        '就诊': vis
    }
    print(sick)
    sick_list.append(sick)


# 将sick_list内的信息保存成excel
def to_excel(filename):
    book = xlwt.Workbook(encoding='gbk', style_compression=0)
    sheet = book.add_sheet('39健康网—所有科室疾病', cell_overwrite_ok=True)
    col = ('疾病名称', '别称', '疾病介绍', '相关症状', '病因', '症状', '预防', '找医院', '就诊')
    for i in range(0, 9):
        sheet.write(0, i, col[i])
    for i in range(len(sick_list)):
        data = sick_list[i]
        for j in range(0, 9):
            sheet.write(i + 1, j, data[col[j]])
    book.save(filename)


def section_main():  # 按不同科室依次爬取数据
    for i in section:
        print('***正在爬取{}疾病***'.format(str(i)))
        sec_url = get_section_url(i)
        for j in range(1, 22):
            print('-----正在爬取第{}页内容-----'.format(str(j)))
            try:
                spec_url = get_spec_url(sec_url, j)
            except:
                break
            html = req_headers(spec_url)
            get_all_content(html)
            time.sleep(1)
    print('爬取结束!')
    to_excel('39健康网-全部科室疾病.xlsx')


def main():  # 不按科室直接爬取数据
    for i in range(1, 101):  # 爬取的起始页数(左闭右开)
        print('-----正在爬取第{}页内容-----'.format(str(i)))
        # 获取url
        url = get_all_url(i)
        # 通过该url模拟用户请求服务器，并返回当前页面的html
        html = req_headers(url)
        # 解析html，获得所需信息
        get_all_content(html)
        # 每爬一页保存成一个excel文件
        # to_excel(f'39健康网-第{i}页疾病信息.xls')
        time.sleep(1)  # 设置1s延时
    print('爬取结束!')
    # 保存当前抓取信息至excel
    to_excel('39健康网-全部疾病信息.xls')


if __name__ == '__main__':
    main()
