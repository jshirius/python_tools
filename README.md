# python_tools

pythonで作成したツール郡


■apache_log_ana.py
MATCH_API_URLにmatchするApacheのアクセスログからリクエスト回数、平均レスポンスタイムを計測するツール。計測後、csvファイルに計測結果が出力される。

apache_access.log、apache_access_2.logは、ログファイルの例。
apache_log_ana.pyは、上記のログファイルのフォーマットに合わせてコーディングしている。


使い方：
python2.7 apache_log_ana.py <計測対象のログファイル1つめ> <計測対象のログファイル2つめ> ...

python2.7 apache_log_ana.py apache_access.log apache_access_2.log 


