# -*- coding: utf-8 -*-
import csv

#データの読み込み
comment_data =[]
PN_value = []
P_value = []
N_value = []
P_time = []
N_time =[]
P_comment = []
N_comment = []
time_data = []
with open('Tweetdata.csv','r') as f:

    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        comment_data.append(row[0]) #コメント
        time_data.append(row[1]) #時間
        PN_value.append(row[2]) #PN値

f.close()

for j in range(len(PN_value)): #PN値の振り分け
    if float(PN_value[j-1]) > 0:
        P_value.append(PN_value[j-1]) #P値
        P_time.append(time_data[j-1]) #P値の時間
        P_comment.append(comment_data[j-1]) #P値のコメント

    elif float(PN_value[j-1]) < 0:
        N_value.append(PN_value[j-1]) #N値
        N_time.append(time_data[j-1]) #N値の時間
        N_comment.append(comment_data[j-1]) #N値のコメント

with open('TweetPdata.csv', 'w') as f:    #書き込み作業 P値
    writer = csv.writer(f,lineterminator='\n')
    for i in range(len(P_value)):
        writer.writerow([P_comment[i-1], P_time[i-1], P_value[i-1]])

f.close

with open('TweetNdata.csv', 'w') as f:    #書き込み作業 N値
    writer = csv.writer(f,lineterminator='\n')
    for k in range(len(N_value)):
        writer.writerow([N_comment[k-1], N_time[k-1], N_value[k-1]])

f.close()

#PN値の総数を表示
print('P値の総数は{}です'.format(len(P_value)))
print('N値の総数は{}です'.format(len(N_value)))
print('判定されなかったコメントの総数は{}です'.format(len(PN_value)-len(P_value)-len(N_value)))
