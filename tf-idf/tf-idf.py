import MeCab
import re
import csv

def csv_file_open():
    file = open('tf_idf_keywords1.csv', encoding='utf-8')
    csv_reader = csv.reader(file) #csvfileを読み込む
    data = list(csv_reader) #csvfileをリスト化

    file.close()
    return data

data = csv_file_open()

for i in range(len(data)):
    print(data[i][0])
    if '香川' in data[i][0]:
        print('香川')
