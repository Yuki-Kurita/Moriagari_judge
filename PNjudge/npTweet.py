import MeCab
import re
import csv

def csv_file_open():
    file = open('0612soccerTwitter_moreTweet.csv', encoding='utf-8')
    csv_reader = csv.reader(file) #csvfileを読み込む
    data = list(csv_reader) #csvfileをリスト化

    file.close()
    return data

# PN_Tableのデータを読み込む
def PN_Table_file_open():
    global PN_Table_data # 単語とPN値を格納する辞書
    file_p = open('PN_Table.txt', encoding='shift_jis') #pntableを読み込む

    # 改行を取り除く必要がある？
    for i in file_p:
        i = i.rstrip().split(':') # 改行コードを削除rstrip()し':'で区切る
        PN_Table_data.setdefault(i[0], float(i[3]))

    file_p.close()

# ここでPN値を計算する
# 戻り値はコメントとPN値のリスト
def PN_Calc(comment):
    global word_list
    PN_point = 0 # PN値
    cnt = 0
    score = 0

    # 形態素解析を行う
    m = MeCab.Tagger()
    s = m.parse(comment)
    s = s.split('\n')

    for i in s:
        i = re.split('[\t,]', i)
        if len(i) == 1: # EOSと''をカット
            break

        # PNTableの辞書に単語が含まれていない場合にエラーがでるのでtry
        try:
            # 単語がPNTableに含まれていればscoreに加算 cntを＋１
            score += PN_Table_data[i[7]]
            cnt += 1
        except:
            pass


    if score != 0:
        # PN値 = ツイートの合計スコア / でてきた単語の数
        PN_point = score / cnt


    return [comment, PN_point]


if __name__ == '__main__':
    border = -0.3 # ポジティブとネガティブの境目 (適当)
    time_data = []
    PN_data =[]
    comment = []
    result = {}  # ツイートとそのPN値を格納するリスト
    PN_Table_data = {} # 単語とPN値の辞書

    comment_data = csv_file_open()
    PN_Table_file_open()

    for j in range(len(comment_data)):

        time_data.append(comment_data[j-1][1])

    with open('Tweetdata.csv', 'w') as f:    #newline=''を追加した
        writer = csv.writer(f)
        for i in comment_data:
            tmp = PN_Calc(i[0]) # i[0]にはtextが入っている
            comment.append(tmp[0])
            PN_data.append(tmp[1])

        for k in range(len(comment_data)):
            writer.writerow([comment[k-1],time_data[k-1],PN_data[k-1]])


    f.close()

    # result.setdefault(tmp[0], tmp[1]) # tmp[0]はツイート tmp[1]はPN値




    # print('ポジティブ')
    # for k, v in sorted(result.items(), key=lambda x: -x[1]): # 降順出力
    #     if v > border:
    #         print(k,v)
    #
    # print('\n--------------------\n')
    # print('ネガティブ')
    # for k, v in sorted(result.items(), key=lambda x: x[1]): # 昇順出力
    #     if v <= border:
    #         print(k,v)
