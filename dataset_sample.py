###########################################################
#datasetのサンプル
#like文の取得方法がすぐに見つからなかったのでメモ
###########################################################

import dataset

#公式のサンプル
#https://dataset.readthedocs.io/en/latest/quickstart.html

# 対象のDBを指定
DBMS = 'mysql'
USER = 'root'
PASS = '' #本来はパスワードを設定する
HOST = '127.0.0.1:3306'
DB     = 'kaggle' 
TABLE= 'ashrae_building'
# 文字コードで悩む人へ
CHARSET = 'utf8'

db = dataset.connect('{0}://{1}:{2}@{3}/{4}?charset={5}'.format(DBMS, USER, PASS, HOST, DB, CHARSET))
table = db[TABLE]
results = table.find()

#一覧の取得
for w in results:
    print(w)

#like文をとる
#ポイントは、「table.c.」の後
#ここでは、like文の対象カラムが「primary_use」なので、「table.c.」のあとに「primary_use」を追加している
table = db[TABLE].table
statement = table.select(table.c.primary_use.like('%Office%'))
results = db.query(statement)
for w in results:
    print(w)
