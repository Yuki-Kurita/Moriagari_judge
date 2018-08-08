import MeCab
import re
import csv

# csvファイルを読み込む
# 戻り値は ツイートのデータのリスト
def tweet_file_open():
    file = open('csvsample.csv', encoding="utf-8") # csvファイルは文字化けするのでutf-8にエンコード

    csv_reader = csv.reader(file)
    data = list(csv_reader)

    file.close()
    return data

# PN_Tableのデータを読み込む
def PN_Table_file_open():
    global PN_Table_data # 単語とPN値を格納する辞書
    file_p = open('PN_Table.txt', 'r')

    # 改行を取り除く必要があるな？
    for i in file_p:
        i = i.rstrip().split(':') # 改行コードを削除し':'で区切る
        PN_Table_data.setdefault(i[0], float(i[3]))

    file_p.close()

# ここでPN値を計算する
# 戻り値はツイートとPN値のリスト
def PN_Calc(tweet):
    global word_list
    PN_point = 0 # PN値
    cnt = 0
    score = 0

    # 形態素解析を行う
    m = MeCab.Tagger()
    s = m.parse(tweet)
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


    return [tweet, PN_point]





if __name__ == '__main__':
    border = -0.3 # ポジティブとネガティブの境目 (適当)

    result = {}  # ツイートとそのPN値を格納するリスト
    PN_Table_data = {} # 単語とPN値の辞書

    tweet_data = tweet_file_open() # ツイートデータを取得
    PN_Table_file_open() # PN_Tableを取得


    for i in tweet_data:
        tmp = PN_Calc(i[5])# i[5]にはtextが入っている
        result.setdefault(tmp[0], tmp[1]) # tmp[0]はツイート tmp[1]はPN値


    print('ポジティブツイート')
    for k, v in sorted(result.items(), key=lambda x: -x[1]): # 降順出力
        if v > border:
            print(k,v)

    print('\n--------------------\n')
    print('ネガティブツイート')
    for k, v in sorted(result.items(), key=lambda x: x[1]): # 昇順出力
        if v <= border:
            print(k,v)
