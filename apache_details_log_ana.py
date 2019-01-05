# -*- coding: utf-8 -*-

import sys
import time
from datetime import datetime, date, time
import csv
import os

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

u"""
MATCH_API_URLにmatchするApacheのアクセスログからリクエスト日時,リクエストURL,レスポン時間(ms)を取得する
"""


"""
定数宣言
"""


#解析データをまとめるwork領域
ana_datas = []

#処理対象のAPIの文字列
MATCH_API_URL = "sampleApi/Controller/function1"

#レスポンス時間の閾値(ms)
threshold_time = 1000
        
#ログデーターを分類する    
def log_classification(inputdata):
	 #print(s_line)
	 
	 #空白でデータ分ける
	 data =  inputdata.split()

	 
	 #時間で分割
	 dtime =  data[0]
	 #年、月、日を取得する
	 temp = dtime.split("T")
	 temp2 = temp[0].split("-")
	 temp3 = temp[1].split(":")
	 year = int(temp2[0])
	 month = int(temp2[1])
	 day = int(temp2[2])
	 
	 #時、分を取得する
	 hour = int(temp3[0])
	 minute =  int(temp3[1])
	 sec =  temp3[2]
	 sec = int(sec[:2])
	
	 #時間型のオブジェクトに変換する 
	 dtime = datetime(year, month, day, hour, minute,sec)
	 
	 
	 #リクエストURLで分割
	 url = data[8]

	 
	 #レスポンスタイム取得(us)
	 #msに変換する
	 res_time = int(data[12]) // 1000

	
	 dict =  {"time":dtime, "request_path":url ,"res_time": res_time}
	 return dict

#解析データを追加する
def append_ana_data(data):
	
	#すでに登録されているところがあるかチェック
	ana_datas.append(data)

def make_csv():
	
	
	# ファイルオープン
	f = open('detail_output.csv', 'w')
	writer = csv.writer(f, lineterminator='\n')

	# カラム名を出力
	csvlist = []
	#リクエスト日時,リクエストURL,レスポン時間(ms)
	csvlist.append("リクエスト日時")
	csvlist.append("リクエストURL")
	csvlist.append("レスポンス時間(ms)")

	
	# 出力
	writer.writerow(csvlist)
	
	#数字のキーによる並べ替え
	for v in sorted(ana_datas, key=lambda x:x['time']):

		#閾値を比較して本当に追加するか判定
		if(v["res_time"]  < threshold_time):
			continue

		csvlist = []
		csvlist.append(v["time"])
		csvlist.append(v["request_path"])
		csvlist.append(v["res_time"])
		writer.writerow(csvlist)


	# ファイルクローズ
	f.close()	

def make_pyplot():
	
	timeList = []
	resTimeList = []
	
	for v in sorted(ana_datas, key=lambda x:x['time']):
		timeList.append(v["time"])
		resTimeList.append(v["res_time"])

	
	df = pd.DataFrame({
	    'date': pd.to_datetime(timeList)
        ,'res_time': resTimeList
	})
	
	df = df.set_index('date')
	plt.scatter(df.index, df['res_time'])

	plt.xticks(rotation=10)
	#plt.show()
	plt.savefig("plot.png")

def apache_log_main(path):
    read_count = 0
    with open(path) as f:
        for s_line in f:
            read_count = read_count + 1
			
			#文字列に「MATCH_API_URL」があること
            rtn = MATCH_API_URL in s_line
            if(rtn == False):
                continue
			
    		#ログデータを分類する
            data = log_classification(s_line)
            append_ana_data(data)
			#print read_count


if __name__ == '__main__':

	#解析対象のログのファイル名を取得する
	param = sys.argv
    #print(param)
	if (len(param) < 3):
		print("第1引数に閾値(ms) 第2引数以降に解析対象のログファイルを指定してください")
		quit()

	#閾値の設定
	threshold_time =  int(param[1])
	
	for i in range(2,len(param)):
		path = param[i]
		if(os.path.exists(path) == True):		
			print ("現在処理中のファイル名:" + path)
		else:
			print ("存在しないファイルです。ファイル名:" + path)
			continue
		apache_log_main(path)
	
	
	#CSVに出力する
	make_csv()
	
	#グラフを描画する
	make_pyplot()