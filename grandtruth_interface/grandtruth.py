# -*- coding: utf-8 -*-
import csv
import datetime

if __name__ == "__main__":
    i = 1
    start = datetime.datetime.today()
    with open('kurita_test_前半.csv', 'w') as f:    #書き込み作業 P値
        writer = csv.writer(f,lineterminator='\n')

        while(True):


            print ('＝＝＝raw_inputを使って文字入力＝＝＝')
            print ('盛り上がり : 1, ニュートラル : 2 盛り下がり : 3')
            input_test = input('>>>  ')

            now = datetime.datetime.today()
            keika = now - start

            if len(input_test) == 0:
                continue

            else:
                input_test_word = int(input_test)



            if input_test_word == 1:
                print('盛り上がり')
                writer.writerow([1,0,0,keika])
            elif input_test_word == 2:
                print('ニュートラル')
                writer.writerow([0,1,0,keika])
            elif input_test_word == 3:
                print('盛り下がり')
                writer.writerow([0,0,1,keika])

            else:
                print('入力ミス')

    f.close
