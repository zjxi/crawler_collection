"""

written by xzj, 2019-2-25

description: a spider based on info concerning Python books from Tianmao mall.
To get what we need more convenient and defend tne anti-crawler strategy successfully，so that
the XPath and proxy-ip tech are being taken. And intergrated request headers, such as cookie,
also add odds to get the correct response from the corresponding server

"""

import requests
from lxml import etree
import time
from urllib import request
import os
import xlwt
import re


def get_url():
    tianmao_url = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000721.1.43c57e17JAJCLz&cat=50021913&q' \
                  '=python&sort=s&style=g&from=sn_1_cat-qp'

    headers = {

        'cookie': 'tk_trace=1; cna=+TCJFAlPUxYCAT2jFcTZVJUB; t=1c5a843f19521e532a6ed298e4a32f05; _tb_token_=e3887b3e1fe7e; cookie2=1efeb8fb9b73b1622ee5f2fcbe8eaf1d; _m_h5_tk=4b904e861ad6b647d974e353c9f151d4_1551081339350; _m_h5_tk_enc=39bbae20eb1b95f754a13acce34eeb2f; _med=dw:1360&dh:768&pw:1360&ph:768&ist:0; hng=""; uc1=cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=VFC%2FuZ9aiKCaj7AzMHh1&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie14=UoTZ5bOdimfOSw%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByEzYGCGNfoSLg9E%3D&id2=UU6kUEirem8l9Q%3D%3D&nk2=tZ4F%2B3IBfuPckoeT&lg2=V32FPkk%2Fw0dUvg%3D%3D; tracknick=%5Cu7EC8%5Cu96E8%5Cu843D%5Cu82B1%5Cu6C38%5Cu591C; _l_g_=Ug%3D%3D; ck1=""; unb=2653730920; lgc=%5Cu7EC8%5Cu96E8%5Cu843D%5Cu82B1%5Cu6C38%5Cu591C; cookie1=B0b1pXFZ61%2FdH%2FQL2Q4Z1eXRg0ZGzbKl%2FxgDvc8gYbs%3D; login=true; cookie17=UU6kUEirem8l9Q%3D%3D; _nk_=%5Cu7EC8%5Cu96E8%5Cu843D%5Cu82B1%5Cu6C38%5Cu591C; uss=""; csg=e8d88a7b; skt=e104e4e2f9bc7299; enc=bXdqofzR%2F1nMiLmPDV7KQ1lxjh6L5r%2BDP%2FqUXJ%2FPUgSj%2BuUokTlOLlrVErhugCAFf%2FNXDLIcIGSawYONLp6FkQ%3D%3D; tt=tmall-main; _uab_collina=155107527520406646181406; cq=ccp%3D0; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=253691; x=__ll%3D-1%26_ato%3D0; x5sec=7b22746d616c6c7365617263683b32223a223636333934363966326534353737393931373332633264343032383665653331434d4c6b7a754d46454d76336c4c6e6a3435694231414561444449324e544d334d7a41354d6a41374d673d3d227d; res=scroll%3A1222*5419-client%3A1222*177-offset%3A1222*5419-screen%3A1360*768; pnm_cku822=098%23E1hvbvvUvbpvUpCkvvvvvjiPRLzvgjlWRFSOzjD2PmPvzjEbR2s9sjr2RFLW1jtPR9GCvvpvvvvvvphvC9v9vvCvpbyCvm9vvvvHphvvzvvvvKrvpv2Vvvmm8hCv2vvvvUUIphvUOQvvvSnvpvF7kphvC99vvOCzBTyCvv9vvUm6OtR4qpyCvhQUUWyvCzPxAfev%2BtgIv8oQeNpOHFU41Wky%2BboJaZfUtb2XrqpyCW2%2BFO7t%2BeCOTWex6fItb9Txfw1l5dUf8z7QD76Od56Ofw1l%2Bb8rRphvCvvvvvm5vpvhvvmv99%3D%3D; whl=-1%260%260%260; l=bBjF376Pv1CWUIZsBOCMNZOjhOQOIIRAguWfcRPBi_5ps1YscobOlrAXhev6Vj5RsrYB4ATie6p9-etui; isg=BA4O3O3i3gqmn2ou6_duRcpYX-Tag8iggLGFBjhXdJHMm671oB4CmQTZ04dSg8qh',
        'Referer': 'https://list.tmall.com/search_product.htm?q=python&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.'
                   'd100&from=mallfp..pc_1_searchbutton',
        'referer': 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000721.1.43c57e17JAJCLz&cat=50021913&q'
                   '=python&sort=s&style=g&from=sn_1_cat-qp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.110 Safari/537.36',
        'upgrade-insecure-requests': '1'
    }
    proxy = {
        'http': '111.72.155.121:9999'
    }
    resp = requests.get(url=tianmao_url, headers=headers, proxies=proxy)
    resp.encoding = 'gbk'
    return resp.text


def re_filename(title, suffix):  # 利用正则使图片命名规范, 即清洗不合理符号
    img_name = re.sub(r'[\?？\.,。！/!]', '', title)
    filename = img_name + suffix

    return filename


COUNT = 1


def get_items_images(img_src, title):
    global COUNT
    suffix = os.path.splitext(img_src)[1]  # 提取img的后缀类型
    full_img_url = 'http:' + img_src
    print('-----正在下载第' + str(COUNT) + '图片-----')
    request.urlretrieve(full_img_url, 'Python_book_imgs/' + re_filename(title, suffix))
    COUNT = COUNT + 1
    print(full_img_url)
    time.sleep(1)  # 设置1s延时


def get_content(html_page):
    parser = etree.HTMLParser(encoding='gbk')
    html = etree.parse(html_page, parser=parser)
    divs = html.xpath("//div[@class='product-iWrap']")
    for div in divs:
        price = div.xpath("./p[@class='productPrice']//@title")[0]
        title = div.xpath("./p[@class='productTitle']//@title")[0]
        month_volume = div.xpath("./p[@class='productStatus']/span[1]/em/text()")[0]
        comments = div.xpath("./p[@class='productStatus']/span[2]/a/text()")[0]
        shop = div.xpath("./p[@class='productStatus']/span[3]/@data-nick")[0]
        img_src = div.xpath("./div[@class='productImg-wrap']/a/img/@src | "
                            "./div[@class='productImg-wrap']/a/img/@data-ks-lazyload")[0]

        get_items_images(img_src, title)  # 下载图书封面图至Python_book_imgs目录下
        add_info_to_list(title, price, month_volume, comments, img_src, shop)  # 将图书信息加入列表


products_list = []


def add_info_to_list(title, price, month_volume, comments, img_src, shop):
    product_info = {
        '书名': title,
        '价格': price,
        '月成交量': month_volume,
        '评价数': comments,
        '店铺': shop,
        '图书封面URL': 'http:' + img_src
    }
    print(product_info)  # 打印title, price, month_volume, comments, img_src, shop信息
    products_list.append(product_info)
    # time.sleep(5)  # 延时5s, 根据需要自行设置


def to_csv(filename):
    book = xlwt.Workbook(encoding='gbk', style_compression=0)
    sheet = book.add_sheet('天猫Python相关图书信息', cell_overwrite_ok=True)
    col = ('书名', '价格', '月成交量', '评价数', '店铺', '图书封面URL')
    for i in range(0, 6):
        sheet.write(0, i, col[i])
    for i in range(len(products_list)):
        data = products_list[i]  #
        for j in range(0, 6):
            sheet.write(i + 1, j, data[col[j]])
    book.save(filename)


def main():
    get_content('tianmao_1.html')
    to_csv('天猫Python相关图书信息.csv')


if __name__ == '__main__':
    main()
