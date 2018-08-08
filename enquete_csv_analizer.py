import csv
import sys

def get_result(text):
    count = 0
    question = []
    q1_result = []
    q2_result = []
    q3_result = []
    q4_result = []
    q5_result = []

    with open(text, 'r')as f:
        reader = csv.reader(f)
        for row in reader:
            if count == 0:
                # 質問内容
                question = row
            else:
                q1_result.append(row[1])
                q2_result.append(row[3])
                q3_result.append(row[5])
                q4_result.append(row[7])
                q5_result.append(row[9])
            count += 1

        #外れ値の削除
        # del q1_result[7:10]
        # del q2_result[7:10]
        # del q3_result[7:10]
        # del q4_result[7:10]
        # del q5_result[7:10]
        writer.writerows([q1_result])
        writer.writerows([q2_result])
        writer.writerows([q3_result])
        writer.writerows([q4_result])
        writer.writerows([q5_result])

    print(question[1])
    print(q1_result)
    print(question[3])
    print(q2_result)
    print(question[5])
    print(q3_result)
    print(question[7])
    print(q4_result)
    print(question[9])
    print(q5_result)

if __name__ == '__main__':
    with open('C出力結果ver.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        get_result(sys.argv[1])
        # get_result(sys.argv[2])
