# -*- coding: utf-8 -*-

import sys
import time
from datetime import datetime, date, time
import csv
import os

u"""
MATCH_API_URLにmatchするApacheのアクセスログからリクエスト回数、レスポンスタイムを計測する
"""
#入力フォーマット
# 該当ファイル名 
#入力

"""
定数宣言
"""

#分割する分
TIME_MIN_DIV = 5

#解析データをまとめるwork領域
ana_datas = {}

#処理対象のAPIの文字列
MATCH_API_URL = "sampleApi"

        
#ログデーターを分類する    
def log_classification(inputdata):
	 #print(s_line)
	 
	 #空白でデータ分ける
	 data =  inputdata.split()
	 #print data
	 
	 
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
	
	 #時間型のオブジェクトに変換する 
	 dtime = datetime(year, month, day, hour, minute)
	 
	 #print dtime;
	 
	 #リクエストURLで分割
	 url = data[8]
	 url = url.split("/",4)
	 #print url[3]
	 
	 #レスポンスタイム取得(us)
	 #msに変換する
	 res_time = int(data[12]) // 1000

	
	 dict =  {"time":dtime, "request_path":url[3] ,"res_time": res_time}
	
	 return dict

#時間からキーを作成する
def make_key(inputdata):
	
	#分からTIME_MIN_DIV分ごとのデータに分ける
	minute = inputdata.minute // TIME_MIN_DIV
	minute = minute * TIME_MIN_DIV

	key = ('{year}{month:02}{day:02}_{hour:02}{minute:02}'.
			format(year=inputdata.year, month=inputdata.month, day=inputdata.day, hour=inputdata.hour, minute=minute))
	#print key
	return key
	
#解析データを追加する
def append_ana_data(key, data):
	
	#すでに登録されているところがあるかチェック
	input_data = None
	url_key = data["request_path"]
	
	if(key  in ana_datas):
		#キー(日時)に対するデータ取得
		key_data = ana_datas[key]
		if(data["request_path"]  in key_data):
			#すでに登録されているデータあり
			input_data = ana_datas[key][url_key]

		
	#データの格納(更新)
	if(input_data == None):
		#初期化する
		#avr_request_time(平均レスポンス時間は、本関数を抜けてから計算する)については
		init_dict = {"time": key, "request_path": data["request_path"],"request_count":1, 
						"max_request_time":data["res_time"], "sum_request_time":data["res_time"], "avr_request_time":data["res_time"]}		
		
		url_key = data["request_path"]
		
		request_per_data = {}
		request_per_data[url_key] = init_dict
		

		#ana_datasの初期化確認
		if(key not in ana_datas):
			#初期化
			ana_datas[key] = {}
		
		
		#ana_datas[key][url_key] = request_per_data
		ana_datas[key][url_key] = init_dict
		#print ana_datas
	else:
		#データの更新
		input_data["request_count"] = input_data["request_count"]  + 1
		input_data["sum_request_time"] = input_data["sum_request_time"]  + data["res_time"]
		input_data["avr_request_time"] = input_data["sum_request_time"]  // input_data["request_count"]
		if( input_data["max_request_time"]  < data["res_time"]):
			input_data["max_request_time"]  = data["res_time"]
		#print "データ更新"
		ana_datas[key][url_key] = input_data
		#print ana_datas[key][url_key] 

def make_csv():
	
	# ファイルオープン
	f = open('output.csv', 'w')
	writer = csv.writer(f, lineterminator='\n')

	# カラム名を出力
	csvlist = []
	csvlist.append("時間帯({min}分毎)".format(min=TIME_MIN_DIV))
	csvlist.append("リクエストURL")
	csvlist.append("リクエスト回数")
	csvlist.append("最大リクエスト時間(ms)	")
	csvlist.append("合計リクエスト時間(ms)	")
	csvlist.append("平均リクエスト時間(ms)	")
	
	# 出力
	writer.writerow(csvlist)

	
	#数字のキーによる並べ替え
	for date_key, date_value in sorted(ana_datas.items()):
		
		for k, v in sorted(date_value.items()):
			csvlist = []
			csvlist.append(date_key)
			csvlist.append(k)
			csvlist.append(v["request_count"])
			csvlist.append(v["max_request_time"])
			csvlist.append(v["sum_request_time"])
			csvlist.append(v["avr_request_time"])
			writer.writerow(csvlist)


	# ファイルクローズ
	f.close()	
	

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
            key = make_key(data["time"])
            append_ana_data(key, data)
			#print read_count




if __name__ == '__main__':

	#解析対象のログのファイル名を取得する
	param = sys.argv
    #print(param)
	if (len(param) < 2):
		print ("解析対象のログファイルを指定してください")
		quit()

	for i in range(1,len(param)):
		path = param[i]
		if(os.path.exists(path) == True):		
			print "現在処理中のファイル名:" + path
		else:
			print "存在しないファイルです。ファイル名:" + path
			continue
		apache_log_main(path)
	
	
	#CSVに出力する
	make_csv()