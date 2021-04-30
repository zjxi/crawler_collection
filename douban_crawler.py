"""
Author: ZJHsi
Date: 2019-2-21
Theme：爬取《流浪地球》豆瓣短评，并生成相应高频词汇词云
"""
import requests
import re
import xlwt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba


def get_url(page):
    url = 'https://movie.douban.com/subject/26266893/comments?start={0}' \
          '&limit=20&sort=new_score&status=P'.format(str(page))

    headers = {
        'Accept': 'text / event - stream',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept - Language': 'zh - CN, zh;q = 0.9',
        'Cache - Control': 'no - cache',
        'Connection': 'keep-alive',
        'Origin': 'https://movie.douban.com',
        'Referer': 'https://movie.douban.com/subject/26266893/comments?start='
                   + str(page) + '&limit=20&sort= new_score&status=P',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.110 Safari/537.36'
    }

    req = requests.get(url=url, headers=headers)
    req.encoding = 'utf-8'
    return req.text


def get_selection(html):
    select = re.compile(
        r'<span class="votes">(.*?)</span>.*?<span class="short">(.*?)</span>',
        re.S)
    selection = re.findall(select, html)
    return selection


data_list = []


def get_content():
    for i in range(0, 450720, 20):
        print('****正在爬取第' + str(i / 20 + 1) + '页信息****')
        html = get_url(i)
        for j in get_selection(html):
            print(j[1], j[0])  # print short-comments and thumbs-up
            data = []
            for z in range(0, 2):
                data.append(j[z])
            data_list.append(data)


def to_excel(path):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('流浪地球_豆瓣热门短评', cell_overwrite_ok=True)
    col = ('短评', '点赞数')
    for i in range(0, 2):
        sheet.write(0, i, col[i])
    for i in range(len(data_list)):
        data = data_list[i]
        for j in range(0, 2):
            sheet.write(i + 1, j, data[j])
    book.save(path)


def word_cloud_creation(filename):
    text = open(filename).read()
    word_list = jieba.cut(text, cut_all=True)
    wl = ' '.join(word_list)
    return wl


def word_cloud_settings():
    wc = WordCloud(
        background_color='white',
        max_words=2000,
        max_font_size=100,
        height=1200,
        width=1500,
        random_state=30,
        font_path='C:\Windows\Fonts\simfang.ttf'
    )
    return wc


def word_cloud_implementation(wl, wc):
    my_words = wc.generate(wl)
    plt.imshow(my_words)
    plt.axis('off')
    plt.show()
    wc.to_file('word_cloud.png')  # save pic to the relative path


if __name__ == '__main__':
    # to_excel('流浪地球_豆瓣热门短评.xls')
    # word_cloud_implementation(word_cloud_creation('流浪地球_豆瓣热门短评.txt'), word_cloud_settings())
    get_content()


