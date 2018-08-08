# -*- coding: utf-8 -*-
import csv
import numpy as np
import matplotlib.pyplot as plt

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

def calc_histgram(text):
    time_data = []
    time_list = [0]
    min_list = []
    cnt_list = [0]
    #　second, ヒストグラムの区切り
    sec = 60
    cnt = 0
    time_data, comment_data = csv_file_open(text)

    # for i in range(len(data)):
    #     time_data.append(data[i][1])
    # １分ごとにカウント
    for k in range(len(time_data)):
        if int(time_data[k]) > sec:
            cnt_list.append(cnt)
            time_list.append(sec)
            cnt = 0
            sec += 60
        else:
            cnt += 1

    for j in range(len(time_list)):
        min_list.append(j)
    return time_list, cnt_list, min_list

def make_histgram(min_list, cnt_list, con_detection_time, con_detection, detection_time, detection, moriagari_value):
    plt.plot(min_list, cnt_list, c='blue',alpha=0.7)
    plt.plot(min_list, moriagari_value, c='orange',alpha=0.7)
    plt.scatter(detection_time, detection, s=50, c="yellow", marker="*", alpha=0.5,linewidths="2", edgecolors="orange", label = 'Enthusiasm detection')
    plt.scatter(con_detection_time, con_detection, s=50, c="red", marker=">", alpha=0.5,linewidths="2", edgecolors="orange", label = 'Enthusiasm continued')
    plt.plot([detection_time,detection_time], [0,700],'green',linestyle = 'dashed',alpha=0.3)
    plt.plot([con_detection_time,con_detection_time], [0,700],'orange',linestyle = 'dashed',alpha=0.3)
    plt.xlim(0,60)
    plt.ylim(0,400)

    plt.xticks(np.arange(0,65,5))
    plt.title('Enthusiasm judge')
    plt.xlabel('Time[min]')
    plt.ylabel('The number of tweets')
    plt.legend(loc = 'upper right')
    plt.show()

def moriagari_detection(cnt_list,min_list):
    #盛り上がり判定のリスト, 盛り上がりを検出したら1, それ以外は0
    moriagari_switch = []
    #盛り上がり検出の閾値
    moriagari_value = []
    # グラフ用のデータ
    detection_time = []
    detection = []
    con_detection_time = []
    con_detection = []
    # 盛り上がり継続用リスト
    moriagari_con = []

    for i in range(len(cnt_list)):
        #前3分間のデータを扱うため, indexが負の値を参照する場合を除外
        if i == 0 :
            moriagari_value.append(cnt_list[i])
        elif i == 1:
            data1 = np.array([cnt_list[i],cnt_list[i-1]])
            moriagari_value.append(np.std(data1) + np.average(data1))
        # elif i == 2:
        #     data2 = np.array([cnt_list[i],cnt_list[i-1],cnt_list[i-2]])
        #     moriagari_value.append(np.std(data2) + np.average(data2))
        else:
            #　３分間の平均, 標準偏差を計算
            data = np.array([cnt_list[i-1],cnt_list[i-2]])
            std = np.std(data)
            ave = np.average(data)
            moriagari_value.append(std + ave)

        # 盛り上がり検出, 閾値を超えているか
        if cnt_list[i] > moriagari_value[i]:
            moriagari_switch.append(1)
            detection_time.append(min_list[i])
            detection.append(300)
        else:
            moriagari_switch.append(0)

        #盛り上がり継続判定
        try:
            #1分前に盛り上がりが検出された,もしくは盛り上がり継続があった場合
            if moriagari_switch[i-1] == 1 or moriagari_con[i-1] == 1:
                if cnt_list[i] > np.average(data):
                    moriagari_con.append(1)
                    con_detection_time.append(min_list[i])
                    con_detection.append(250)
                else:
                    moriagari_con.append(0)
            else:
                moriagari_con.append(0)
        except:
            moriagari_con.append(0)

    return con_detection_time, con_detection, detection_time, detection, moriagari_value

def tf_idf(detection_time, con_detection_time):
    detection_time.extend(con_detection_time)
    detection_time.sort()
    for i in range(len(detection_time)):
        try:
            if detection_time[i] == detection_time[i-1]:
                del detection_time[i-1]
        except:
            pass
    return detection_time

if __name__ == '__main__':
    #盛り上がり判定のリスト, 盛り上がりを検出したら1, それ以外は0
    moriagari_switch = []
    #盛り上がり検出の閾値
    moriagari_value = []
    #コメント, 時間(sec)のデータを渡すと一分間のツイート数と時間の配列を返す
    time_list, cnt_list, min_list = calc_histgram('0628日本ポーランド.csv')
    #ツイート数と時間の配列を渡すと, 盛り上がりを検出したタイミングを返す
    con_detection_time, con_detection, detection_time, detection, moriagari_value= moriagari_detection(cnt_list, min_list)
    #グラフを作成
    make_histgram(min_list, cnt_list, con_detection_time, con_detection, detection_time, detection,moriagari_value)
    #盛り上がり区間の時間幅を抽出
    ent_time = tf_idf(detection_time, con_detection_time)
    print(ent_time)
