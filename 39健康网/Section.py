"""

 written by ZJ.Hsi, 2019-3-2
 a crawler for the whole detailed info of www.39.net using requests+XPath+proxy-ip
 as well as multi-thread tech to get them smoothly

"""
import requests
from lxml import etree
import xlwt


def req_headers(url):
    headers = {
        # 'Host': 'jbk.39.net',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/70.0.3538.110 Safari/537.36'
    }
    proxy = {
        'https': '223.100.166.3:36945',
        'https': '111.177.183.154:9999'
    }
    resp = requests.get(url=url, headers=headers, proxies=proxy)
    resp.encoding = 'UTF-8'
    return resp.text


def hosp_req_headers(url):
    headers = {
        # 'Host': 'yyk.39.net',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/70.0.3538.110 Safari/537.36'
    }
    proxy = {
        'https': '223.100.166.3:36945',
        'https': '111.177.183.154:9999'
    }
    resp = requests.get(url=url, headers=headers, proxies=proxy)
    resp.encoding = 'gbk'
    return resp.text


# section = ['fuke', 'nanke', 'neike', 'waike', 'pifuke',
#            'wuguanke', 'erke', 'xingbingke', 'chanke']


def get_section_url(section):
    url = 'http://jbk.39.net/bw/' + section
    return url


def get_spec_url(url, pg):
    spec_url = url + '_p{}/'.format(str(pg))
    return spec_url


def get_other_url(other_src):
    return other_src


sick_list = []


def html_parser(text):
    html = etree.HTML(text)
    return html


def get_all_content(htm):
    html = html_parser(htm)
    divs = html.xpath("//div[@class='result_item']")

    for div in divs:
        """
        get the major info of the current page
        """
        title = div.xpath(".//p[@class='result_item_top_l']/a/@title")[0]
        try:
            nick_name = div.xpath(".//p[@class='result_item_top_l']/i/text()")[0]
        except:
            nick_name = '暂无'
        detail = div.xpath(".//p[@class='result_item_content']/text()")[0]
        try:
            related = div.xpath(".//p[@class='result_item_content_label']/a[position()>0]/text()")
        except:
            related = '暂无'
        '''
        get the other info from the other src
        '''
        try:
            cause_src = div.xpath(".//p[@class='result_item_top_r']/a[1]/@href")[0]
            cause = get_other_content(cause_src)
        except:
            cause = '暂无'
        try:
            symptom_src = div.xpath(".//p[@class='result_item_top_r']/a[2]/@href")[0]
            symp = get_other_content(symptom_src)
        except:
            symp = '暂无'
        try:
            prevent_src = div.xpath(".//p[@class='result_item_top_r']/a[3]/@href")[0]
            pre = get_other_content(prevent_src)
        except:
            pre = '暂无'
        try:
            hospital_src = div.xpath(".//p[@class='result_item_top_r']/a[4]/@href")[0]
            hosp = get_hosp_info(hospital_src)
        except:
            hosp = '暂无'
        try:
            visit_src = div.xpath(".//p[@class='result_item_top_r']/a[5]/@href")[0]
            vis = get_visit_info(visit_src)
        except:
            vis = '暂无'
        '''
        add all the needed info to a list
        '''
        add_to_list(title, nick_name, detail, related, cause, symp, pre, hosp, vis)


def get_other_content(src):
    url = get_other_url(src)
    text = req_headers(url)
    html = html_parser(text)
    try:
        other = html.xpath("//div[@class='article_paragraph']//text()")
    except:
        other = '暂无'
    return other


def get_hosp_info(hosp_src):
    url = get_other_url(hosp_src)
    text = hosp_req_headers(url)
    html = html_parser(text)
    try:
        hosp = html.xpath("//div[@class='yy-msg']//a[@class='yy-name']/text()")
    except:
        hosp = '暂无'
    return hosp


def get_visit_info(vis_src):
    url = get_other_url(vis_src)
    text = req_headers(url)
    html = html_parser(text)
    try:
        vis = html.xpath("//div[@class='zn-main']/dl[position()>0]//text()")
    except:
        vis = '暂无'
    return vis


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


def to_csv(filename):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('39健康网—所有科室疾病', cell_overwrite_ok=True)
    col = ('疾病名称', '别称', '疾病介绍', '相关症状', '病因', '症状', '预防', '找医院', '就诊')
    for i in range(0, 9):
        sheet.write(0, i, col[i])
    for i in range(len(sick_list)):
        data = sick_list[i]
        for j in range(0, 9):
            sheet.write(i + 1, j, data[col[j]])
    book.save(filename)


