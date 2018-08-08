# -*- coding: utf-8 -*-
import csv
import MeCab
import sys
import re
from statistics import mean, stdev
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

#盛り上がりレベル判定
def moriagari_level(cnt, baseline):
    if cnt - baseline > 0.66 * baseline:
        # 盛り上がり度3
        level = 3
    elif cnt - baseline <= 0.66 * baseline and cnt - baseline > 0.33 * baseline:
        # 盛り上がり度2
        level = 2
    elif cnt - baseline <= 0.33 * baseline and cnt - baseline >= 0:
        # 盛り上がり度1
        level = 1
    return level


def get_event(moriagari_tweet, top):
    kyouki_meisi1 = {}
    top1_tweet = []
    top1_text = ''
    for z in range(len(moriagari_tweet)):
        if moriagari_tweet[z].find(top) != -1:
            top1_tweet.append(moriagari_tweet[z])
    for a in top1_tweet:
        top1_text += a
        #top3ワードと共起しているワードをリスト化
    mecab = MeCab.Tagger()
    mecab.parse("")
    node1 = mecab.parseToNode(top1_text)
    while node1:
        kyouki_meisi1[node1.surface] = kyouki_meisi1.get(node1.surface, 0) + 1 # 辞書に単語を追加
        node1 = node1.next
    sort_kyouki_meisi1 = sorted(kyouki_meisi1.items(), key=lambda x:-x[1])
    return sort_kyouki_meisi1

def get_meisi_kandousi(moriagari_tweet):
    text = ''
    frequency_meisi, frequency_kandousi = {}, {}
    new_frequency_meisi, new_frequency_kandousi = [], []
    for x in moriagari_tweet:
        text += x
    mecab = MeCab.Tagger()
    mecab.parse("")
    node1 = mecab.parseToNode(text)
    while node1:
        if node1.feature.startswith('名詞'):
            frequency_meisi[node1.surface] = frequency_meisi.get(node1.surface, 0) + 1 # 辞書に単語を追加
        node1 = node1.next
    node2 = mecab.parseToNode(text)
    while node2:
        if node2.feature.startswith('感動詞') or node2.feature.startswith('フィラー'):
            frequency_kandousi[node2.surface] = frequency_kandousi.get(node2.surface, 0) + 1 # 辞書に単語を追加
        node2 = node2.next
    #降順に変換
    sort_frequency_meisi = sorted(frequency_meisi.items(), key=lambda x:-x[1])
    sort_frequency_kandousi = sorted(frequency_kandousi.items(), key=lambda x:-x[1])
    #中のタプルからリストに変換
    for y in range(len(sort_frequency_meisi)):
        new_frequency_meisi.append(list(sort_frequency_meisi[y]))
    for y in range(len(sort_frequency_kandousi)):
        new_frequency_kandousi.append(list(sort_frequency_kandousi[y]))
    #必要ない名詞を削除
    try:
        for j in range(len(new_frequency_meisi)):
            if new_frequency_meisi[j][0] == 'の' or new_frequency_meisi[j][0] == 'ー'or new_frequency_meisi[j][0] == '(' or new_frequency_meisi[j][0] == 'ん' or new_frequency_meisi[j][0] == 'o' or new_frequency_meisi[j][0] == 'ﾟ' or new_frequency_meisi[j][0] == '＃' or new_frequency_meisi[j][0] == '-' or new_frequency_meisi[j][0] == 'ーー':
                del new_frequency_meisi[j]
        for j in range(len(new_frequency_meisi)):
            if new_frequency_meisi[j][0] == 'ん' or new_frequency_meisi[j][0] == '〜' or new_frequency_meisi[j][0] == '一' or new_frequency_meisi[j][0] == 'ーーー' or new_frequency_meisi[j][0] == '～' or new_frequency_meisi[j][0] == 'これ':
                del new_frequency_meisi[j]
    except IndexError:
        pass
    try:
        for j in range(0,3):
            if new_frequency_kandousi[j][0] == 'ま' or new_frequency_kandousi[j][0] =='なんか' or new_frequency_kandousi[j][0] =='う' or new_frequency_kandousi[j][0] =='w':
                del new_frequency_kandousi[j]
    except IndexError:
        pass
    return new_frequency_meisi, new_frequency_kandousi

def moriagari_kabo_talk(moriagari_tweet,kyouki_list1,frequency_meisi):
    #いらない文字を削除
    text = ','.join(moriagari_tweet)
    text = re.sub('【|】|⚽|🇯🇵|🇵🇱|🏆|🔥|😍|👏|🇸🇳|🇨🇴|😭|😅|🙏|👎|🙌|🌏|😞|💦|💭|😲|🇷🇺|🎉|\u3000',"", text)
    text = re.sub('#|▼|＃|☆|「|」|;|。|https://t.co/mcKKhNj9vn|https://t.co/fvy93R50Bn|https://t.co/40zwTUx4gT|https://t.co/Ujrw0FMZBl|https://t.co/7KxfMM9ng2',"", text)
    moriagari_tweet = text.split(',')
    terms1 = True
    #kabo1に話させる内容
    #共起名詞3つと被っている場合
    if len(kyouki_list1) > 2:
        for a in range(len(moriagari_tweet)):
            if moriagari_tweet[a].find(kyouki_list1[0]) != -1 and moriagari_tweet[a].find(kyouki_list1[1]) != -1 and moriagari_tweet[a].find(kyouki_list1[2]) != -1:
                kabo1_talk = moriagari_tweet[a]
                del moriagari_tweet[a]
                terms1 = False
                break
            else:
                terms1 = True
    #共起名詞2つと被っている場合
    if len(kyouki_list1) > 1:
        if terms1:
            for a in range(len(moriagari_tweet)):
                if moriagari_tweet[a].find(kyouki_list1[0]) != -1 and moriagari_tweet[a].find(kyouki_list1[1]) != -1:
                    kabo1_talk = moriagari_tweet[a]
                    del moriagari_tweet[a]
                    terms1 = False
                    break
                else:
                    terms1 = True
    #共起名詞1つと被っているば場合
    if len(kyouki_list1) == 1:
        if terms1:
            for a in range(len(moriagari_tweet)):
                if moriagari_tweet[a].find(kyouki_list1[0]) != -1 :
                    kabo1_talk = moriagari_tweet[a]
                    terms1 = False
                    del moriagari_tweet[a]
                    break

    if len(moriagari_tweet) != 0 and terms1:
            kabo1_talk = moriagari_tweet[a]
            del moriagari_tweet[a]
    #kabo2に話させる内容
    kabo2_talk = min(moriagari_tweet, key=len)
    return kabo1_talk, kabo2_talk

def normal_kabo_talk(normal_tweet, i, kabo1_talk_list, kabo2_talk_list, kabo3_talk_list):
    try:
        if i % 3 == 0:
            kabo1_talk_list.append(normal_tweet[0])
        if i % 3 == 1:
            kabo2_talk_list.append(normal_tweet[0])
        if i % 3 == 2:
            kabo3_talk_list.append(normal_tweet[0])
    except IndexError:
        pass

if __name__ == '__main__':
    not_moriagari_list = []
    moriagari_switch = []
    moriagari_tweet = []
    second_data, comment_data = csv_file_open(sys.argv[1])
    time_list, cnt_list = count(sys.argv[1])
    time_data = []
    kabo1_time, kabo2_time, kabo3_time = [], [], []
    kabo1_talk_list, kabo2_talk_list, kabo3_talk_list = [],[],[]
    for i in range(len(time_list)):
        new_frequency_meisi, new_frequency_kandousi, kyouki_list1 = [], [], []
        text = ''
        #開始15s以内はデータ不足のため考えない
        if time_list[i] <= 15:
            not_moriagari_list.append(cnt_list[i])
            moriagari_switch.append(0)
        elif time_list[i] > 15:
            if time_list[i] < 900:
                ave = mean(not_moriagari_list)
                sd = stdev(not_moriagari_list)
            if time_list[i] >= 900:
                ave = mean(not_moriagari_list[-180+len(time_data):])
                sd = stdev(not_moriagari_list)
            baseline = ave + 2 * sd
            #盛り上がり判定
            if cnt_list[i] >= baseline and (cnt_list[i]-cnt_list[i-1] > 0):
                #盛り上がりレベル判定
                level = moriagari_level(cnt_list[i], baseline)
                time_data.append(time_list[i])
                moriagari_switch.append(1)
                #5秒前 ~ 現在のツイートをリスト化, 盛り上がり継続の場合はそれまでのツイートをリスト化
                for j in range(len(second_data)):
                    if time_list[i-1] <= second_data[j] < time_list[i]:
                        moriagari_tweet.append(comment_data[j])
                #リストに対して名詞のみ形態素解析を行う->出現頻度と名詞の辞書に変換
                new_frequency_meisi, new_frequency_kandousi = get_meisi_kandousi(moriagari_tweet)
                #kabo3(コミュ障)が喋る内容
                if len(new_frequency_kandousi) != 0:
                    kabo3_talk = new_frequency_kandousi[0][0]
                else:
                    kabo3_talk = 'おおお'
                if len(new_frequency_meisi) != 0:
                    top = new_frequency_meisi[0][0]
                else:
                    top = ''
                #---- 頻出ワードと共起している単語を取得 ----
                sort_kyouki_meisi1 = get_event(moriagari_tweet, top)
                if len(sort_kyouki_meisi1) == 0:
                    kyouki_list1 = []
                elif len(sort_kyouki_meisi1) == 1:
                    kyouki_list1 = [sort_kyouki_meisi1[0][0]]
                elif len(sort_kyouki_meisi1) == 2:
                    kyouki_list1 = [sort_kyouki_meisi1[0][0],sort_kyouki_meisi1[1][0]]
                else:
                    kyouki_list1 = [sort_kyouki_meisi1[0][0],sort_kyouki_meisi1[1][0],sort_kyouki_meisi1[2][0]]
                #---- kaboちゃんに発話させる内容を決める ----
                if len(moriagari_tweet) == 0:
                    kabo1_talk, kabo2_talk = [], []
                else:
                    kabo1_talk, kabo2_talk = moriagari_kabo_talk(moriagari_tweet, kyouki_list1, new_frequency_meisi)
                #---- 盛り上がりレベルによる発話時間の振り分け ----
                if level == 1:
                    kabo1_time.append(time_list[i]-2.5)
                    kabo1_talk_list.append(kabo1_talk)
                if level == 2:
                    kabo1_time.append(time_list[i]-3.75)
                    kabo1_talk_list.append(kabo1_talk)
                    kabo2_time.append(time_list[i]-1.25)
                    kabo2_talk_list.append(kabo2_talk)
                if level == 3:
                    kabo1_time.append(time_list[i]-4.2)
                    kabo1_talk_list.append(kabo1_talk)
                    kabo2_time.append(time_list[i]-0.8)
                    kabo2_talk_list.append(kabo2_talk)
                    kabo3_time.append(time_list[i]-2.5)
                    kabo3_talk_list.append(kabo3_talk)
                #15[s]以上盛り上がりが続いた場合はデータを消す
                if moriagari_switch[i-4] == 1:
                    moriagari_tweet = []

            #盛り上がりでない場合での処理
            else:
                normal_tweet = []
                moriagari_switch.append(0)
                not_moriagari_list.append(cnt_list[i])
                for j in range(len(second_data)):
                    if time_list[i-1] <= second_data[j] < time_list[i]:
                        normal_tweet.append(comment_data[j])
                # normal_kabo_talk(normal_tweet,i,kabo1_talk_list,kabo2_talk_list,kabo3_talk_list)
                #盛り上がり継続でないのでツイートを消す
                moriagari_tweet = []

    print(kabo1_time)
    print(len(moriagari_switch))
    print(len(kabo1_talk_list),len(kabo1_time),len(kabo2_talk_list),len(kabo2_time),len(kabo3_talk_list),len(kabo3_time))
    #csvファイルへの書き込み
    # with open('all_kabo1_talk.csv', 'w') as f:
    #     writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    #     writer.writerows([kabo1_talk_list, kabo1_time])
    # f.close
    # with open('all_kabo2_talk.csv', 'w') as f:
    #     writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    #     writer.writerows([kabo2_talk_list, kabo2_time])
    # f.close
    # with open('all_kabo3_talk.csv', 'w') as f:
    #     writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    #     writer.writerows([kabo3_talk_list, kabo3_time])
    # f.close
    # print('処理完了')
