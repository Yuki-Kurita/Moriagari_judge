# coding utf-8
import sys
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
underOrDownerCount = []
# 盛り上がり検出されたタイミング配列
enthuTimeStart = []
enthuTimeStop = []
enthuSwitch = []
# 各タイミングにおける盛り上がり閾値のリスト
thresholdList = [0]
firstFlg = True
enthuFlg = False
count = 0
enthuCount = []
lvThirdCount = []
lvThirdTime = []
lvSecondCount = []
lvSecondTime = []
lvOneCount = []
lvOneTime = []

# サッカー(二時間)のときはrange(1440) ダッシュ（1時間）のときは720 報道ステーションは912
x = [5*x for x in range(1440)]

FirstTweetTime = datetime.datetime.strptime(TweetTimeArray[0], '%H:%M:%S')
SectionST = FirstTweetTime - datetime.timedelta(seconds=FirstTweetTime.second)
for i in range(len(TweetTimeArray)):
    TweetTime = datetime.datetime.strptime(TweetTimeArray[i], '%H:%M:%S')
    if datetime.timedelta(0, 5) <= TweetTime-SectionST:
        SectionTwCount.append(0)
        SectionST += datetime.timedelta(seconds=5)

        if firstFlg:
            # normalTwCount.append(SectionTwCount[a-1])
            underOrDownerCount.append(SectionTwCount[a-1])
            thresholdList.append(0)
            enthuSwitch.append(0)
            SectionTwCount[a] += 1
            firstFlg = False
            a += 1
            continue
        # 盛り上がり判定
        if a <= 3:
            # データ不足のため判定しない
            underOrDownerCount.append(SectionTwCount[a-1])
            thresholdList.append(0)
            enthuSwitch.append(0)
        elif a > 3:
            ave = mean(underOrDownerCount)
            # ave = mean(SectionTwCount)
            sd = stdev(underOrDownerCount)
            # sd = stdev(SectionTwCount)
            baseline = ave + 2*sd
            thresholdList.append(baseline)
            #前が盛り上がりでない場合
            if enthuSwitch[a-1] == 0:
                if SectionTwCount[a-1] >= baseline:
                    if (SectionTwCount[a-1]-SectionTwCount[a-2] > 0):
                        enthuTimeStart.append(x[a])
                        enthuCount.append(SectionTwCount[a-1])
                        enthuSwitch.append(1)
                        enthuFlg = True
                    else:
                        underOrDownerCount.append(SectionTwCount[a-1])
                        enthuSwitch.append(0)
                        if SectionTwCount[a-1]-baseline > 0.7*baseline:
                            # 盛り上がり度3
                            lvThirdCount.append(SectionTwCount[a-1])
                            lvThirdTime.append(x[a-1])
                        elif SectionTwCount[a-1]-baseline <= 0.66*baseline and SectionTwCount[a-1]-baseline >= 0.33*baseline:
                            # 盛り上がり度2
                            lvSecondCount.append(SectionTwCount[a-1])
                            lvSecondTime.append(x[a-1])
                        elif SectionTwCount[a-1]-baseline <= 0.33*baseline and SectionTwCount[a-1]-baseline >= 0:
                            # 盛り上がり度1
                            lvOneCount.append(SectionTwCount[a-1])
                            lvOneTime.append(x[a-1])
                else:
                    underOrDownerCount.append(SectionTwCount[a-1])
                    enthuSwitch.append(0)
                    enthuFlg = False
            #前が盛り上がりである場合
            if enthuSwitch[a-1] == 1:
                if SectionTwCount[a-1] >= baseline:
                    if (SectionTwCount[a-1]-SectionTwCount[a-2] > 0):
                        enthuCount.append(SectionTwCount[a-1])
                        enthuSwitch.append(1)
                        enthuFlg = True
                    else:
                        underOrDownerCount.append(SectionTwCount[a-1])
                        enthuSwitch.append(0)
                        enthuTimeStop.append(x[a])
                else:
                    underOrDownerCount.append(SectionTwCount[a-1])
                    enthuSwitch.append(0)
                    enthuTimeStop.append(x[a])
                    enthuFlg = False
        a += 1
    SectionTwCount[a] += 1
print(len(enthuCount))
print("SectionTwCountの長さは{}　Xの長さは{}".format(len(SectionTwCount), len(x)))
# 最終的にthresholdListは一つ足りなくなるため追加で計算
ave = mean(underOrDownerCount)
ave = mean(SectionTwCount)
sd = stdev(SectionTwCount)
sd = stdev(underOrDownerCount)
baseline = ave + 2*sd
thresholdList.append(baseline)
# print("標準偏差{}".format(sd))
# plt.plot(x, SectionTwCount)
# thirdx = [90 for i in range(len(lvThirdTime))]
# secondx = [80 for i in range(len(lvSecondTime))]
# onex = [70 for i in range(len(lvOneTime))]
# plt.scatter(lvThirdTime, thirdx, c='red', marker='*', linewidth='2')
# plt.scatter(lvSecondTime, secondx, c='orange', marker='*', linewidth='2')
# plt.scatter(lvOneTime, onex, c='green', marker='*', linewidth='2')
# y = [15 for i in range(1440)]
# plt.plot(x, thresholdList, "r")
# # plt.plot(x, y, "r")
# plt.show()
