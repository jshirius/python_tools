# -*- coding: utf-8 -*-

import mysql.connector
 
 #docker環境の場合、ローカルPCであってもhostは127.0.0.1ではない。
 #docker network inspect python-networkで、ネットワーク環境を確認して、
 #hostを設定する
#db=mysql.connector.connect(host="172.18.0.2", port="3306",  user="root", password="mysql_pass")
db=mysql.connector.connect(host="localhost", port="33306",  user="root", password="mysql_pass")
 
cursor=db.cursor()
 
cursor.execute("USE test_work")
db.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS docker_make(
                id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                fruits VARCHAR(32),
                value INT);""")
db.commit()

db.close()

#import mysql.connectorの場合は、
#１０回以上連続でsqlを実行(connectを含む)してもタスクは２つのみしか作成されなかった。
#ただし、close処理していないためか、２つのタスクは残っていた。
#closeすれば、タスクは残らなかった。

