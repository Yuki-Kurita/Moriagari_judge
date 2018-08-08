# -*- coding: utf-8 -*-
import MeCab
import math
import csv

def analyse(text):
    mecab = MeCab.Tagger() ## MeCab のインスタンス作成
    mecab.parse("")
    feature_vector = {} ## 結果を納める辞書
    node = mecab.parseToNode(text) ## 解析を実行
    while node:
        # print(node.surface, node.feature) ## それぞれ単語とその情報（品詞など）
        surface = node.surface
        feature_vector[surface] = feature_vector.get(surface, 0) + 1 # 辞書に単語を追加
        node = node.next

    return feature_vector

def frequency_write(text,i):
    comment = []
    file = open(text, 'r')
    feature_vector = analyse(file.read())
    with open('frequency_keywords{}.csv'.format(i),'w') as f:
         writer = csv.writer(f)
         for k,v in sorted(feature_vector.items(), key=lambda x: -x[1]):
            writer.writerow([k,v])
            comment.append(k)
    file.close()
    return comment

def calc_tf_idf(text,N):
    nij = 0
    tf = []
    idf = []
    tf_idf = []

    file = open(text, encoding='utf-8')
    csv_reader = csv.reader(file) #csvfileを読み込む
    tf = list(csv_reader) #csvfileをリスト化
    count = [0 for i in range(len(tf))]

    for i in range(len(tf)):
        nij = nij + int(tf[i][1])

    # print(nij)
    for j in range(len(tf)):
        tf[j][1] = int(tf[j][1]) / nij

    file.close()

    #dfを計算
    for i in range(0,N):
        f = open('moriagari_data{}.txt'.format(i),'r')
        data = f.read()
        for j in range(len(tf)):
            index = data.find(tf[j][0])
            # print(index)
            if index != -1:
                count[j] = count[j] + 1
    f.close()

    for k in range(len(count)):
        idf.append(math.log(N/count[k-1]) + 1)
        tf_idf.append(tf[k][1] * idf[k])

    return tf_idf

if __name__ == '__main__':
    tf_idf = []
    N = 18#データ数
    #出現キーワード毎に書き出し
    for i in range(0,N):
        # 頻出キーワード
        comment = frequency_write('moriagari_data{}.txt'.format(i),i)
        # tf-idf
        tf_idf = calc_tf_idf('frequency_keywords{}.csv'.format(i),N)
        tf_idf_dic = dict(zip(comment, tf_idf))
        tf_idf_dic_sort = sorted(tf_idf_dic.items(), key=lambda x: -x[1])

        with open('tf_idf_keywords{}.csv'.format(i),'w') as f:
            writer = csv.writer(f)
            for k in range(len(tf_idf)):
                writer.writerow([tf_idf_dic_sort[k][0],tf_idf_dic_sort[k][1]])

        f.close()
    print('処理が完了しました')



    # for word,freq in feature_vector.items():
    #     word_list.append(word)
    #     freq_list.append(freq)
    #
    # print(word_list, freq_list)