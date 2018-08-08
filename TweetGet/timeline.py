# -*- coding: utf-8 -*-

import json
from requests_oathlib import OAth1Session
import datetime, time, sys

CK = '0tuIALJ31qJedQsl9QxuQZwNs' # consumerKey
CS = 'yL4150z1a264dCqtjcMdRiwFrhcYmbIvPXVib057VQSiPKBDLI' # consumerSecret
AT = '2386648844-jEXNWv0lLkt6AvrgR1DKqdw4S6y8YyzA4tRqyXA' # accessToken
AS = 'yaZ77zPogen2J01bBn3o1G9JloeQMDb4W7xCRyDeCkDqq' # accessTokenSecret

session = OAuth1Session(CK, CS, AT, AS)

url = 'https://api.twitter.com/1.1/search/tweets.json'
res = session.get(url, params = {'q':u'沖縄旅行', 'count':10})

#--------------------
# ステータスコード確認
#--------------------
if res.status_code != 200:
    print ("Twitter API Error: %d" % res.status_code)
    sys.exit(1)

#--------------
# ヘッダー部
#--------------
print ('アクセス可能回数 %s' % res.headers['X-Rate-Limit-Remaining'])
print ('リセット時間 %s' % res.headers['X-Rate-Limit-Reset'])
sec = int(res.headers['X-Rate-Limit-Reset'])\
           - time.mktime(datetime.datetime.now().timetuple())
print ('リセット時間 （残り秒数に換算） %s' % sec)

#--------------
# テキスト部
#--------------
res_text = json.loads(res.text)
for tweet in res_text['statuses']:
    print ('-----')
    print (tweet['created_at'])
    print (tweet['text'])
