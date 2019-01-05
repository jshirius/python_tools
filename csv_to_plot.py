# -*- coding: utf-8 -*-

import sys
import time
from datetime import datetime, date, time
import csv
import os

import pandas as pd
import matplotlib
#matplotlib.use('Agg') pngに書き出すときはONにする
import matplotlib.pyplot as plt

X_COLUMN_NAME = "xname"
Y_COLUMN_NAME = "c"

u"""
CSVから時系列データを読み込んでグラフを作成する
注意事項
X軸は時系列になっていること
"""

if __name__ == '__main__':

	#解析対象のログのファイル名を取得する
	param = sys.argv
    #print(param)
	if (len(param) < 2):
		print("第1引数にCSVファイルのパス第2引数以降に解析対象のログファイルを指定してください")
		quit()

	path = param[1]
	df = pd.read_csv(path, encoding="utf_8")
	

	#時系列のグラフに変換する
	df[X_COLUMN_NAME] = pd.to_datetime(df[X_COLUMN_NAME])
	df = df.set_index(X_COLUMN_NAME)
	plt.scatter(df.index, df[Y_COLUMN_NAME])

	plt.xticks(rotation=10)
	plt.show()
	#plt.savefig("plot.png")
	
