# -*- coding: utf-8 -*-
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

def csv_file_open(text):

    file = open(text, encoding='utf-8')
    csv_reader = csv.reader(file) #csvfileを読み込む
    data = list(csv_reader) #csvfileをリスト化
    file.close()
    return data

def do_plot(x,y):
    plt.plot(x,y)
    plt.plot([sys.argv[2],sys.argv[3]],[0,4])
    plt.plot([sys.argv[4],sys.argv[5]],[0,4])
    # plt.scatter(detection_time, detection, s=50, c="yellow", marker="*", alpha=0.5,linewidths="2", edgecolors="orange", label = 'Enthusiasm detection')
    # plt.scatter(con_detection_time, con_detection, s=50, c="red", marker=">", alpha=0.5,linewidths="2", edgecolors="orange", label = 'Enthusiasm continued')
    # plt.plot([detection_time,detection_time], [0,700],'green',linestyle = 'dashed',alpha=0.3)
    # plt.plot([con_detection_time,con_detection_time], [0,700],'orange',linestyle = 'dashed',alpha=0.3)
    plt.xlim(0,5)
    plt.ylim(0,10)
    # plt.xticks(np.arange(0,3800,200))
    # plt.title('Enthusiasm judge')
    # plt.xlabel('Time[sec]')
    # plt.ylabel('The number of tweets')
    # plt.legend(loc = 'upper right')
    plt.show()

if __name__ == '__main__':
    x_data = []
    y_data = []
    data_list = csv_file_open(sys.argv[1])
    for i in range(len(data_list)):
        x_data.append(data_list[i][0])
        y_data.append(data_list[i][1])
    do_plot(x_data, y_data)
