import MeCab
import re
import csv
from collections import Counter

#テキストを形素態解析して名詞、動詞、形容詞だけを抜き出したリストを返す
def extract_word(text):
        tagger = MeCab.Tagger('-Ochasen')
        node = tagger.parseToNode(text)
        word_list = []
        while node:
                if node.feature.split(",")[0] in ("名詞", "動詞", "形容詞"):
                    word_list.append(node.surface)
                node = node.next
        return word_list

def csv_file_open():
    file = open('0612soccerTwitter_moreTweet.csv', encoding='utf-8')
    csv_reader = csv.reader(file) #csvfileを読み込む
    data = list(csv_reader) #csvfileをリスト化

    file.close()
    return data

def make_histogram(word_list):
        histogram = Counter(word_list)
        return histogram


if __name__ == "__main__":

    comment_data = []
    word_list = []
    histogram = []
    total_data = csv_file_open()

    #コメントのみを抽出
    for j in range(len(total_data)):

        comment_data.append(total_data[j-1][0])
    comment = "\n".join(comment_data)
    print(comment)
    
    #コメントを形素態解析
    # for i in range(0, 3):
    #     word_list.append(extract_word(comment_data[i]))
    # print(word_list)
    #
    # #ヒストグラム化
    # for i in range(0, 3):
    #     histogram.append(make_histogram(word_list[i]))
    # print(histogram)
