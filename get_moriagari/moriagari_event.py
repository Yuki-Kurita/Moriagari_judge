# -*- coding: utf-8 -*-
import MeCab

f = open('moriagari_data18.txt','r')
data = f.read()
moriagari_list = data.split(',')
key_person = '西野'
list = []
feature_vector = {}

for i in range(len(moriagari_list)):
    if moriagari_list[i].find(key_person) != -1:
        list.append(moriagari_list[i])

comment = ','.join(list)
mecab = MeCab.Tagger()
mecab.parse('')
node = mecab.parseToNode(comment)
while node:
    surface = node.surface
    feature_vector[surface] = feature_vector.get(surface, 0) + 1 # 辞書に単語を追加
    node = node.next

print(sorted(feature_vector.items(), key=lambda x: -x[1]))
