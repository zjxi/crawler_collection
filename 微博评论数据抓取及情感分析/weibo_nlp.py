from snownlp import sentiment
import pandas as pd
import snownlp


def read_csv():
    weibo_text = pd.read_csv('weibo_wumai.csv', usecols=[1], skiprows=1, encoding='utf-8')
    weibo_text.to_csv('weibo_text.csv', encoding='utf-8', index_label=False)
    # return weibo_text


def train():
    sentiment.train('D:\\neg.txt', 'D:\\pos.txt')
    sentiment.save('sentiment.marshal')

sentiment_list = []


def test(path):
    with open(path, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            s = snownlp.SnowNLP(line)
            sent_dict = {
                '情感分析结果': s.sentiments,
                '微博内容': line
            }
            sentiment_list.append(sent_dict)
            print(sent_dict)
        # df = pd.DataFrame(sentiment_list)
        # df.to_csv('微博情感分析结果.csv', index=False, encoding='utf_8_sig')






