# -*- coding: utf-8 -*-
#yahoo知恵袋、Google検索、TwitterAPIから該当キーワードの情報を取得する

from datetime import datetime
import csv
import sys
from selenium import webdriver
import pandas as pd
from time import sleep
import twitter
from urllib.parse import urlencode
from twitter_api_setting import * #twitter apiの設定

##########################
#設定関連
##########################




csv_file_name = "matome_twitter.csv"


#twitterAPI
def twitter_matome(target_keyword):

    print("twitter_matome開始")
    #Twitter APIにアクセスする
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                    consumer_secret=CONSUMER_SECRET,
                    access_token_key=ACCESS_TOKEN,
                    access_token_secret=ACCESS_TOKEN_SECRET)

    query = urlencode({
        'q': target_keyword,  # 検索ワード
        'result_type': 'recent',  # recent/popular/mixed
        'count': 100  # 取得するツイート数（100が最大）
    # 'max_id':  これを利用して更に過去の情報を取れる
    })

    result = api.GetSearch(raw_query=query)
    #print(result)
    out_puts = []
    for status in result:
        out_dic ={}

        if("http:" in status.text):
            continue

        if("https:" in status.text):
            continue

        url = "https://twitter.com/%s/status/%s" %(status.user.screen_name, str(status.id))
        out_dic['id'] = status.id
        out_dic['created_at'] = status.created_at
        out_dic['query_key'] = target_keyword
        out_dic['rs_title'] = status.user.name
        out_dic['rs_link']  = url
        out_dic['rs_summary'] = status.text
        out_puts.append(out_dic)
    
    return out_puts

if __name__ == '__main__':
    

    #csvファイルから取得対象のキーワードを取得する
    twitter_collect_list_df = pd.read_csv('twitter_collect_list.csv')

    #twitter api
    columns = ['id','created_at','query_key','rs_title','rs_summary','rs_link']
    analysis_list = []
    try:
        for index, row in  twitter_collect_list_df.iterrows():
            print(row['keyword'] + ":Twitterの結果の検索開始します")
            d = twitter_matome(row['keyword'])
            analysis_list.extend(d)
            df=pd.DataFrame(analysis_list, columns=columns) 
            df.to_csv(csv_file_name, encoding="utf_8_sig")
    except Exception as e:
        print(e)


