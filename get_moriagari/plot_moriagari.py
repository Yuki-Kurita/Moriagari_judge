# codin utf-8
import sys
import matplotlib.pyplot as plt
import datetime
import csv
from statistics import mean, stdev

TweetTimeArray = []
with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    for row in reader:
        # 24:00:00とか言う表記には対応していないため変換してあげる
        if row[1].find("23") == 0:
            row[1] = "0"+row[1][2:]
        if row[1].find("24") == 0:
            row[1] = "1"+row[1][2:]
        if row[1].find("25") == 0:
            row[1] = "2"+row[1][2:]

        TweetTimeArray.append(row[1])
a = 0
SectionTwCount = [0]
# normalTwCount = []
notEnthu_time = []
# 盛り上がり検出されたタイミング配列
enthu_time = []
# 各タイミングにおける盛り上がり閾値のリスト
threshold_list = []
firstFlg = True

# サッカー(二時間)のときはrange(1440) ダッシュ（1時間）のときは720
x = [(1/12)*x for x in range(1440)]

FirstTweetTime = datetime.datetime.strptime(TweetTimeArray[0], '%H:%M:%S')
SectionST = FirstTweetTime - datetime.timedelta(seconds=FirstTweetTime.second)
for i in range(len(TweetTimeArray)):
    TweetTime = datetime.datetime.strptime(TweetTimeArray[i], '%H:%M:%S')
    if datetime.timedelta(0, 5) <= TweetTime-SectionST:
        SectionTwCount.append(0)
        SectionST += datetime.timedelta(seconds=5)

        if firstFlg:
            # normalTwCount.append(SectionTwCount[a-1])
            notEnthu_time.append(SectionTwCount[a-1])

            threshold_list.append(0)
            SectionTwCount[a] += 1
            firstFlg = False
            a += 1
            continue
        # 盛り上がり判定
        if a <= 3:
            # データ不足のため判定しない
            notEnthu_time.append(SectionTwCount[a-1])
            threshold_list.append(0)
        elif a > 3:
            ave = mean(notEnthu_time)
            sd = stdev(notEnthu_time)
            enthu_threshold = ave + 2*sd
            threshold_list.append(enthu_threshold)
            if(SectionTwCount[a-1] >= enthu_threshold):
                enthu_time.append(x[a-1])
            else:
                notEnthu_time.append(SectionTwCount[a-1])
        a += 1
    SectionTwCount[a] += 1


print("SectionTwCountの長さは{}　Xの長さは{}".format(len(SectionTwCount), len(x)))
# 最終的にThreshold_listは一つ足りなくなるため追加で計算
ave = mean(notEnthu_time)
# ave = mean(SectionTwCount)
sd = stdev(notEnthu_time)
# sd = stdev(SectionTwCount)
enthu_threshold = ave + 2*sd
threshold_list.append(enthu_threshold)
# print("標準偏差{}".format(sd))
# plt.plot(x, SectionTwCount)
# plt.plot(x, threshold_list, "r")
# plt.show()
print(enthu_time)
# --- 盛り上がり区間の時間抽出 ---

t = 5
time = []
for i in range(len(threshold_list)):
    time.append(t)
    t += 5
not_enth = []
enth = []
for i in range(len(threshold_list)):
    try:
        if SectionTwCount[i] > threshold_list[i]:
            #盛り上がり継続の場合
            if SectionTwCount[i-1] > threshold_list[i-1]:
                continue
            #盛り上がり検知の場合
            else:
                enth.append(time[i])
        #前で盛り上がっていて、現在盛り上がっていない場合
        elif SectionTwCount[i-1] >  threshold_list[i-1]:
            not_enth.append(time[i])
    except:
        pass
enth_section = [enth, not_enth]
print(enth_section)
