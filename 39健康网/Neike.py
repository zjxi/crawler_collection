from Section import *
import time


def main():
    print('***正在爬取内科疾病***')
    sec_url = get_section_url('neike')
    for i in range(1, 101):
        print(f'-----正在爬取第{i}页内容-----')
        spec_url = get_spec_url(sec_url, i)
        html = req_headers(spec_url)
        get_all_content(html)
        time.sleep(2)
    print('爬取结束!')
    to_csv('39健康网-内科疾病.csv')
