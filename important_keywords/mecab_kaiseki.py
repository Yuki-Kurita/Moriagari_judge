# -*- coding: utf-8 -*-
import csv
import MeCab
import sys
import numpy as np
import matplotlib.pyplot as plt

#csvfileを開いてコメントデータを配列で返す
def csv_file_open(text):
    comment_data = []
    file = open(text, encoding='utf-8')
    csv_reader = csv.reader(file) #csvfileを読み込む
    data = list(csv_reader) #csvfileをリスト化
    for i in range(len(data)):
        comment_data.append(data[i][0])
    file.close()
    return comment_data

#品詞の数を表示、配列で返す
def hinsi_kaiseki(comment_list):
    total_hinsi = 0
    hinsi_list = []
    for text in comment_list:
        mecab = MeCab.Tagger()
        mecab.parse("")
        node = mecab.parseToNode(text)
        while node:
            if node.feature.startswith('BOS/EOS'):
                node = node.next
                continue
            hinshi = node.feature.split(",")[0]
            if hinshi in hinsi_count.keys():
                freq = hinsi_count[hinshi]
                hinsi_count[hinshi] = freq + 1
            else:
                hinsi_count[hinshi] = 1
            node = node.next

    for key,value in hinsi_count.items():
        print(key+","+str(value))
        hinsi_list.append(value)
        total_hinsi += value
    print('総品詞数,{}'.format(total_hinsi))
    return hinsi_list

#円グラフを出力
# def circle_plot(data):
#     label = ["名詞", "動詞", "形容詞", "助詞", "助動詞","感動詞","接頭詞","記号","接続詞","フィラー","副詞"]
#     plt.pie(data,labels=label,counterclock=False,startangle=90)
#     plt.axis('equal')
#     plt.show()

if __name__ == '__main__':
    hinsi_count = {}
    hito_comment_list = csv_file_open(sys.argv[1])
    tweet_comment_list = csv_file_open(sys.argv[2])
    print('人の発話')
    hito_list = hinsi_kaiseki(hito_comment_list)
    print('Tweet')
    tweet_list = hinsi_kaiseki(tweet_comment_list)
    print('実験データAのコメント数,{}'.format(len(hito_comment_list)))
    print('実験データBのコメント数,{}'.format(len(tweet_comment_list)))
    # circle_plot(hito_list)
    # circle_plot()
