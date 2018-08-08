# -*- coding: utf-8 -*-
import csv
import MeCab
import sys
import re
#csvファイルの読み込み, 秒データとコメントデータを返す
def csv_file_open(text):
    time = []
    hour = []
    min = []
    second = []
    second_data = []
    comment_data = []
    file = open(text, encoding='utf-8')
    csv_reader = csv.reader(file) #csvfileを読み込む
    data = list(csv_reader) #csvfileをリスト化
    file.close()
    for i in range(len(data)):
        time.append(data[i][1].split(':'))
        comment_data.append(data[i][0])
    for i in range(len(time)):
        hour.append(time[i][0])
        min.append(time[i][1])
        second.append(time[i][2])
    for j in range(len(hour)):
        second_data.append((3600*(int(hour[j])-int(hour[0])) + 60*(int(min[j]) - int(min[0])) + (int(second[j]) - int(second[0]))))
    return second_data, comment_data

# 5秒ごとの時間リストと, ツイート数を返す
def count(text):
    #5秒ごとの時間リスト
    time_list = [0]
    #5秒おきのツイート数をカウントするリスト
    cnt_list = [0]
    sec = 5
    cnt = 0
    second_data, comment_data = csv_file_open(text)
    # 5秒ごとにカウント
    for k in range(len(second_data)):
        if int(second_data[k]) > sec:
            cnt_list.append(cnt)
            time_list.append(sec)
            cnt = 0
            sec += 5
        else:
            cnt += 1
    return time_list, cnt_list

def get_event(moriagari_tweet, top):
    kyouki_meisi1, kyouki_meisi2, kyouki_meisi3 = {}, {}, {}
    top1_tweet, top2_tweet, top3_tweet = [], [], []
    top1_text, top2_text, top3_text = '', '', ''
    for z in range(len(moriagari_tweet)):
        if moriagari_tweet[z].find(top[0]) != -1:
            top1_tweet.append(moriagari_tweet[z])
        if moriagari_tweet[z].find(top[1]) != -1:
            top2_tweet.append(moriagari_tweet[z])
        if moriagari_tweet[z].find(top[2]) != -1:
            top3_tweet.append(moriagari_tweet[z])
    for a in top1_tweet:
        top1_text += a
    for b in top2_tweet:
        top2_text += b
    for c in top3_tweet:
        top3_text += c
        #top3ワードと共起しているワードをリスト化
    mecab = MeCab.Tagger()
    mecab.parse("")
    node1 = mecab.parseToNode(top1_text)
    while node1:
        if node1.feature.startswith('名詞'):
            kyouki_meisi1[node1.surface] = kyouki_meisi1.get(node1.surface, 0) + 1 # 辞書に単語を追加
        node1 = node1.next
    sort_kyouki_meisi1 = sorted(kyouki_meisi1.items(), key=lambda x:-x[1])

    node2 = mecab.parseToNode(top2_text)
    while node2:
        if node2.feature.startswith('名詞'):
            kyouki_meisi2[node2.surface] = kyouki_meisi2.get(node2.surface, 0) + 1 # 辞書に単語を追加
        node2 = node2.next
    sort_kyouki_meisi2 = sorted(kyouki_meisi2.items(), key=lambda x:-x[1])

    node3 = mecab.parseToNode(top3_text)
    while node3:
        if node3.feature.startswith('名詞'):
            kyouki_meisi3[node3.surface] = kyouki_meisi3.get(node3.surface, 0) + 1 # 辞書に単語を追加
        node3 = node3.next
    sort_kyouki_meisi3 = sorted(kyouki_meisi3.items(), key=lambda x:-x[1])
    return sort_kyouki_meisi1, sort_kyouki_meisi2, sort_kyouki_meisi3

def get_kabo_talk(moriagari_tweet,kyouki_list1,kyouki_list2,kyouki_list3, frequency_meisi):
    kabo1_talk, kabo2_talk, kabo3_talk, kabo4_talk = [],[],[],[]
    #kabo1に話させる内容
    #共起名詞3つと被っている場合
    for k in range(len(moriagari_tweet)):
        if moriagari_tweet[k].find(kyouki_list1[0]) != -1 and moriagari_tweet[k].find(kyouki_list1[1]) != -1 and moriagari_tweet[k].find(kyouki_list1[2]) != -1:
            kabo1_talk.append(moriagari_tweet[k])
            del moriagari_tweet[k]
            terms1 = False
            break
        else:
            terms1 = True
    #共起名詞2つと被っている場合
    if terms1:
        for k in range(len(moriagari_tweet)):
            if moriagari_tweet[k].find(kyouki_list1[0]) != -1 and moriagari_tweet[k].find(kyouki_list1[1]) != -1:
                kabo1_talk.append(moriagari_tweet[k])
                del moriagari_tweet[k]
                terms1 = False
                break
            else:
                terms1 = True
    #共起名詞1つと被っているば場合
    if terms1:
        for k in range(len(moriagari_tweet)):
            if moriagari_tweet[k].find(kyouki_list1[0]) != -1 :
                kabo1_talk.append(moriagari_tweet[k])
                terms1 = False
                del moriagari_tweet[k]
                break
    if terms1:
        kabo1_talk.append(moriagari_tweet[k])
        del moriagari_tweet[k]
    #kabo2に話させる内容
    terms2 = True
    for k in range(len(moriagari_tweet)):
        if moriagari_tweet[k].find(kyouki_list2[0]) != -1 and moriagari_tweet[k].find(kyouki_list2[1]) != -1 and moriagari_tweet[k].find(kyouki_list2[2]) != -1:
            kabo2_talk.append(moriagari_tweet[k])
            del moriagari_tweet[k]
            terms2 = False
            break
        else:
            terms2 = True
    if terms2:
        for k in range(len(moriagari_tweet)):
            if moriagari_tweet[k].find(kyouki_list2[0]) != -1 and moriagari_tweet[k].find(kyouki_list2[1]) != -1:
                kabo2_talk.append(moriagari_tweet[k])
                del moriagari_tweet[k]
                terms2 = False
                break
            else:
                terms2 = True
    if terms2:
        for k in range(len(moriagari_tweet)):
            if moriagari_tweet[k].find(kyouki_list2[0]) != -1 :
                kabo2_talk.append(moriagari_tweet[k])
                del moriagari_tweet[k]
                terms2 = False
                break
            else:
                terms2 = True
    if terms2:
        kabo2_talk.append(moriagari_tweet[k])
        del moriagari_tweet[k]
    #kabo3に話させる内容
    terms3 = True
    for k in range(len(moriagari_tweet)):
        if moriagari_tweet[k].find(kyouki_list3[0]) != -1 and moriagari_tweet[k].find(kyouki_list3[1]) != -1 and moriagari_tweet[k].find(kyouki_list3[2]) != -1:
            kabo3_talk.append(moriagari_tweet[k])
            del moriagari_tweet[k]
            terms3 = False
            break
        else:
            terms3 = True
    if terms3:
        for k in range(len(moriagari_tweet)):
            if moriagari_tweet[k].find(kyouki_list3[0]) != -1 and moriagari_tweet[k].find(kyouki_list3[1]) != -1:
                kabo3_talk.append(moriagari_tweet[k])
                del moriagari_tweet[k]
                terms3 = False
                break
            else:
                terms3 = True
    if terms3:
        for k in range(len(moriagari_tweet)):
            if moriagari_tweet[k].find(kyouki_list3[0]) != -1 :
                kabo3_talk.append(moriagari_tweet[k])
                del moriagari_tweet[k]
                terms3 = False
                break
            else:
                terms3 = True
    if terms3:
        kabo3_talk.append(moriagari_tweet[k])
        del moriagari_tweet[k]
    #kabo4に話させる内容
    for k in range(len(moriagari_tweet)):
        if moriagari_tweet[k].find(frequency_meisi[-1][0]) != -1:
            kabo4_talk.append(moriagari_tweet[k])
            break
        elif moriagari_tweet[k].find(frequency_meisi[-2][0]) != -1:
            kabo4_talk.append(moriagari_tweet[k])
            break

    return kabo1_talk, kabo2_talk, kabo3_talk, kabo4_talk


if __name__ == '__main__':
    second_data, comment_data = csv_file_open(sys.argv[1])
    time_list, cnt_list = count(sys.argv[1])
    #盛り上がり区間のツイート
    moriagari_tweet = []
    time_data = []
    #盛り上がり区間の名詞と出現頻度を表した辞書
    frequency_meisi = {}
    new_frequency_meisi = []
    kyouki_list1, kyouki_list2, kyouki_list3 =[],[],[]
    top1, top2, top3 = [],[],[]
    kabo1_talk_list, kabo2_talk_list, kabo3_talk_list = [],[],[]
    kyouki11, kyouki12, kyouki13, kyouki21, kyouki22, kyouki23, kyouki31, kyouki32, kyouki33 = [],[],[],[],[],[],[],[],[]
    text = ''
    #閾値
    thre = 20
    #カウント数が閾値を超えた場合、盛り上がりとする
    for i in range(len(cnt_list)):
        if cnt_list[i] > thre:
            time_data.append(time_list[i])
                #5秒前 ~ 現在のツイートをリスト化
            for j in range(len(second_data)):
                if time_list[i-1] <= second_data[j] < time_list[i]:
                    moriagari_tweet.append(comment_data[j])
            #リストに対して名詞のみ形態素解析を行う->出現頻度と名詞の辞書に変換
            for x in moriagari_tweet:
                text += x
            mecab = MeCab.Tagger()
            mecab.parse("")
            node = mecab.parseToNode(text)
            while node:
                if node.feature.startswith('名詞'):
                    frequency_meisi[node.surface] = frequency_meisi.get(node.surface, 0) + 1 # 辞書に単語を追加
                node = node.next
            #降順に変換
            sort_frequency_meisi = sorted(frequency_meisi.items(), key=lambda x:-x[1])
            #中のタプルからリストに変換
            for y in range(len(sort_frequency_meisi)):
                new_frequency_meisi.append(list(sort_frequency_meisi[y]))
            #必要ない名詞を削除
            try:
                for j in range(0,5):
                    if new_frequency_meisi[j][0] == 'の' or new_frequency_meisi[j][0] == 'ー'or new_frequency_meisi[j][0] == '(' or new_frequency_meisi[j][0] == 'ん' or new_frequency_meisi[j][0] == 'o' or new_frequency_meisi[j][0] == 'ﾟ' or new_frequency_meisi[j][0] == '＃' or new_frequency_meisi[j][0] == '-' or new_frequency_meisi[j][0] == 'ーー':
                        del new_frequency_meisi[j]

                for j in range(0,5):
                    if new_frequency_meisi[j][0] == 'ん' or new_frequency_meisi[j][0] == '〜' or new_frequency_meisi[j][0] == '一' or new_frequency_meisi[j][0] == 'ーーー' or new_frequency_meisi[j][0] == '～' or new_frequency_meisi[j][0] == 'これ':
                        del new_frequency_meisi[j]
                top = [new_frequency_meisi[0][0],new_frequency_meisi[1][0],new_frequency_meisi[2][0]]
            except IndexError:
                pass
            #---- 頻出ワードと共起している単語を取得 ----
            sort_kyouki_meisi1, sort_kyouki_meisi2, sort_kyouki_meisi3 = get_event(moriagari_tweet, top)
            print(top,sort_kyouki_meisi1[0][0], sort_kyouki_meisi1[1][0], sort_kyouki_meisi1[2][0])
            try:
                kyouki_list1 = [sort_kyouki_meisi1[0][0],sort_kyouki_meisi1[1][0],sort_kyouki_meisi1[2][0]]
                kyouki_list2 = [sort_kyouki_meisi2[0][0],sort_kyouki_meisi2[1][0],sort_kyouki_meisi2[2][0]]
                kyouki_list3 = [sort_kyouki_meisi3[0][0],sort_kyouki_meisi3[1][0],sort_kyouki_meisi3[2][0]]
            except:
                pass
            #---- kaboちゃんに発話させる内容を決める ----
            kabo1_talk, kabo2_talk, kabo3_talk, kabo4_talk = get_kabo_talk(moriagari_tweet, kyouki_list1, kyouki_list2, kyouki_list3, new_frequency_meisi)
            #csvで出力するためのリスト作り
            kabo1_talk_list.append(kabo1_talk[0])
            kabo2_talk_list.append(kabo2_talk[0])
            kabo3_talk_list.append(kabo3_talk[0])
            top1.append(new_frequency_meisi[0][0])
            top2.append(new_frequency_meisi[1][0])
            top3.append(new_frequency_meisi[2][0])
            kyouki11.append(kyouki_list1[0])
            kyouki12.append(kyouki_list1[1])
            kyouki13.append(kyouki_list1[2])
            kyouki21.append(kyouki_list2[0])
            kyouki22.append(kyouki_list2[1])
            kyouki23.append(kyouki_list2[2])
            kyouki31.append(kyouki_list3[0])
            kyouki32.append(kyouki_list3[1])
            kyouki33.append(kyouki_list3[2])

            frequency_meisi = {}
            moriagari_tweet = []
            sort_frequency_meisi = []
            text = ''
            new_frequency_meisi = []
            kyouki_meisi1, kyouki_meisi2, kyouki_meisi3 = {}, {}, {}
    #csvファイルへの書き込み
    # with open('kabo_talk_all.csv', 'w') as f:
    #     writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    #     writer.writerows([time_data, top1, top2, top3,kyouki11,kyouki12,kyouki13,kyouki21,kyouki22,kyouki23,kyouki31,kyouki32,kyouki33,kabo1_talk_list,kabo2_talk_list,kabo3_talk_list])
    # f.close
