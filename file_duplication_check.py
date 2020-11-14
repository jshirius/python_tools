#ファイルの重複を検出する

import os
import glob
import pandas as pd

#コマンド入力部

#重複の検出
#ファイルの先頭が「.」は除外で確認


file_list = glob.glob("/Users/name/Pictures/**", recursive=True)
#file_list = glob.glob("/Volumes/LACIE/photo/**", recursive=True)
#/Volumes/LACIE/photo/2016/
#情報をdictに格納する
file_info_list = []
for file_path in file_list:
    #ファイルの情報を取得する
    file_info = {"dir":"" , "file_name":"", "extension":"","file_size":0}
    
    #拡張子が空白は除外
    extension = os.path.splitext(file_path)
    file_info["extension"] = extension[1]
    if(len(extension[1]) == 0):
        continue
    
    #ディレクトリ名とファイル名
    file_name = os.path.split(file_path)
    file_info["dir"] = file_name[0]
    file_info["file_name"] = file_name[1]

    #ファイルサイズ
    file_info['file_size'] = os.path.getsize(file_path)
    
    file_info_list.append(file_info)

#print(file_list)
df = pd.DataFrame(file_info_list)


#拡張子の一覧を出す
print("拡張子の一覧を取得する")
u = df['extension'].unique()
print(u)

#ファイル名の重複check
df['duplicated_file_name'] = df.duplicated(subset='file_name')

#ファイルサイズ
df['duplicated_file_size'] = df.duplicated(subset='file_size')

print("重複サイズの重複")
print(df.duplicated(subset='file_size').value_counts()[True])
df.to_csv("photo_infos.csv"  ,encoding='utf-8-sig')