# -*- coding: utf-8 -*-
import csv

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

comment_list = []
#盛り上がり開始 - 盛り上がり終了
enth_section = [[35, 310, 320, 675, 760, 815, 840, 855, 965, 975, 1235, 1250, 1260, 1280, 1955, 2095, 2115, 2130, 2170, 2180, 2235, 2375, 2435, 2550, 2580, 2605, 2740, 2755, 2800, 2870, 2885, 2900, 2920, 2950, 2965, 3015, 3030, 3825, 3840, 3855, 3885, 3895, 3970, 4305, 4360, 4405, 4555, 4595, 4655, 4665, 4815, 4825, 4845, 4870, 4935, 4950, 5000, 5040, 5060, 5190, 5400, 5410, 5470, 5540, 5595, 5605, 5635, 5720, 5755, 5765, 5805, 5855, 5870, 5920, 5940, 5985, 6115, 6135, 6160, 6330, 6415, 6495, 6840], [45, 315, 325, 680, 800, 835, 845, 860, 970, 990, 1240, 1255, 1265, 1315, 2075, 2105, 2125, 2135, 2175, 2185, 2250, 2380, 2440, 2555, 2600, 2610, 2750, 2760, 2865, 2880, 2895, 2910, 2925, 2955, 2970, 3020, 3035, 3835, 3850, 3865, 3890, 3965, 3975, 4355, 4365, 4435, 4560, 4605, 4660, 4800, 4820, 4830, 4855, 4880, 4940, 4990, 5035, 5055, 5105, 5195, 5405, 5420, 5475, 5590, 5600, 5625, 5715, 5750, 5760, 5790, 5810, 5865, 5915, 5935, 5950, 6090, 6125, 6145, 6320, 6405, 6490, 6835, 7130]]

second_data, comment_data = csv_file_open('0628日本ポーランド.csv')
print(len(second_data), len(comment_data))
for j in range(len(enth_section[0])):
    for k in range(len(second_data)):
        if enth_section[0][j] <= int(second_data[k]) < enth_section[1][j]:
            comment_list.append(comment_data[k])

    comment = ','.join(comment_list)
    file = open('moriagari_data_soccer{}.txt'.format(j),'w')
    file.write(comment)
    comment_list = []
    comment = ''
