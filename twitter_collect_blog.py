# -*- coding: utf-8 -*-
#ツイッターまとめ用のブログ作成ツール

from datetime import datetime
import csv
import sys
from selenium import webdriver
import pandas as pd
from time import sleep
import twitter
from urllib.parse import urlencode
from twitter_api_setting import * #twitter apiの設定
from janome.tokenizer import Tokenizer
import codecs


##########################
#設定関連
##########################




csv_file_name = "matome_twitter.csv"





#感情ファイルの辞書を作成する
def read_pn_di():
    dic_pn = {}
    
    f = open('semantic_orientations_of_words.txt')
    lines = f.readlines() # 1行を文字列として読み込む(改行文字も含まれる)
    
    for line in lines:
        #フォーマット
        #見出し語:読み(ひらがな):品詞:感情極性実数値
        columns = line.split(':')
        dic_pn[columns[0]] = float(columns[3])
    f.close

    return dic_pn

#単語感情極性対応表データを取得する
dic_pn = read_pn_di()
t = Tokenizer()


#twitterAPI
def twitter_matome(summary_id, target_keyword):

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
        out_dic['summary_id'] = summary_id
  
        out_puts.append(out_dic)
    
    return out_puts


def create_summary_data(summary_id, search_keyword, tweet_list):
    #案件ごとの概要のカラム
    #summary_columns = ["summary_id", 'search_keyword','semantic_value','most_common' ,'tweet_cnt']

    semantic_value = 0
    semantic_count = 0
    words = []
    for sentence in tweet_list:
        sentence = sentence['rs_summary']
        tokens = t.tokenize(sentence)
        
        for token in tokens:
            # 品詞を取り出し
            partOfSpeech = token.part_of_speech.split(',')[0]
    
            #感情分析(感情極性実数値より)
            if( partOfSpeech in ['動詞','名詞', '形容詞', '副詞']):
                if(token.surface in dic_pn):
                    data = token.surface + ":" + str(dic_pn[token.surface])
                    print(data)
                    semantic_value = dic_pn[token.surface] + semantic_value
                    semantic_count = semantic_count + 1
                    words.append(token.surface)

    #if partOfSpeech == u'名詞'  or  partOfSpeech == u'形容詞' :
                #print (token.surface)
            
        
        #if len(words) > 0:
        #    mixi_diary_words.extend(words)
        
    data = "分析した単語数:" +  str(semantic_count) +  " 感情極性実数値合計:" + str(semantic_value) + " 感情極性実数値平均値:" + str(semantic_value / semantic_count)
    print(data)

 
    #折角なので文字数も求めてみる
    from collections import Counter
    c =  Counter(words)
    common = c.most_common()

    summary_dict = {}
    summary_dict['summary_id'] = summary_id
    summary_dict['search_keyword'] = search_keyword
    v = semantic_value / semantic_count
    summary_dict['semantic_value'] = str(f'{v:.02f}')
    summary_dict['tweet_cnt'] = len(tweet_list)

    #回数は5まで
    datas = ""
    for index, word in enumerate(common):
        if(index ==5):
            break
        data = "「%s %d回」" % (word[0], word[1])
        datas = datas + data + " "

    datas = datas.strip()
    summary_dict['most_common'] = datas
    

    return summary_dict


def create_tweet_area(search_keyword ,adlink, tweet_df):
    out_put = ".##%sの感想メインのツイート\n" % search_keyword

    out_put = out_put + "[html]\n"
    out_put = out_put + "<hr>\n"
    
    for index, row in  tweet_df.iterrows():
        #名前(リンクあり)
        link = "<a href='%s'  target='_blank' >%s</a>" % (row['rs_link'], row['rs_title'])

        #ツイート本文
        data = link + "<br>\n\n" + "<p>" + row['rs_summary'] + "</p>"
        if(len(adlink) > 0):
            if (index % 17 == 0): #17個目ごとにアフィリエイトリンクを貼る
                data = data + "<p>" + adlink + "</p>"
        data = data + "<hr>\n\n"
        out_put = out_put + data


    #広告を入れる
    if(len(adlink) > 0):
        data = "<p>" + adlink + "</p>"
        out_put = out_put + data


    out_put = out_put + "\n[/html]\n"
    return out_put

twitter_collect_setting = ""

def get_collect_setting(key:str):
    print(twitter_collect_setting)
    d = twitter_collect_setting[twitter_collect_setting['key'] ==key]
    d = d.reset_index()
    d = d.loc[0]['data']
    return d

if __name__ == '__main__':

    #データ格納領域を作成する
    #twitter_df = pd.DataFrame()
    #summary_df = pd.DataFrame()

    #csvファイルから取得対象のキーワードを取得する
    twitter_collect_list_df = pd.read_csv('twitter_collect_list_prod.csv')
    twitter_collect_list_df = twitter_collect_list_df.fillna("")

    #キーリスト取得
    twitter_collect_setting = pd.read_csv('twitter_collect_setting.csv')

    #twitter api
    columns = ['id','created_at','query_key','rs_title','rs_summary','rs_link','summary_id']
    analysis_list = []
    summary_list = []
    try:
        for index, row in  twitter_collect_list_df.iterrows():
            summary_id = index + 1
            print(row['keyword'] + ":Twitterの結果の検索開始します")
            d = twitter_matome(summary_id, row['keyword'])
            if(len(d) == 0):
                continue

            analysis_list.extend(d)
            df=pd.DataFrame(analysis_list, columns=columns) 
            df['summary_id'] = summary_id
            df.to_csv(csv_file_name, encoding="utf_8_sig")

            #概要作成
            summary_data = create_summary_data(index + 1, row['keyword'], d)
            summary_data['ad'] = row['ad']
            summary_list.append(summary_data)

    except Exception as e:
        print(e)

    #ここからテキストに書き出す
    print("・・・・・・・・・・・・・・・・")
    print(summary_list)
    #print(analysis_list)

    #pandasに入れる
    twitter_df = pd.DataFrame(analysis_list) 
    summary_columns = ["summary_id", 'search_keyword','semantic_value','most_common' ,'tweet_cnt','ad']
    summary_df = pd.DataFrame(summary_list, columns = summary_columns) 
    

    print(twitter_df)
    print(summary_df)
    ####################################
    ##ここからテキストに出力するところ
    ####################################
    output_text = "[div]"
    output_text = output_text + "\n\n"

    #実行時間を取得
    dt_now = datetime.now()
    day = dt_now.strftime('%Y年%m月%d日')

    #リード文を作成する
    d = get_collect_setting('lead_sentence')
    d = d  % day
    output_text = output_text + d + "\n\n"


    #概要表示の情報
    output_text = output_text + "#プログラミングスクールの集計結果" + "\n\n"

    d = get_collect_setting('summary_cap')
    output_text = output_text + d + "\n\n"

    #概要tableを作成する
    pd.set_option("display.max_colwidth", 300)
    summary_df_html = summary_df.copy()
    summary_df_html = summary_df_html.drop("ad", axis=1)
    summary_df_html = summary_df_html.rename(columns={'summary_id':'No' , 'search_keyword': 'プログラミングスクール名','semantic_value':'感情数値','most_common':'よく使われている言葉','tweet_cnt':'ツイート回数'})

    output_text = output_text + "[html]\n"
    output_text = output_text + summary_df_html.to_html(index_names=False, index= False, justify="left",show_dimensions= False)
    output_text = output_text + "\n[/html]\n\n"

    #ツイート表示前
    output_text = output_text + "#プログラミングスクールのツイートまとめ\n\n"


    #ツイートをひたすら出力するところ
    for index, row in  summary_df.iterrows():
        #
        twitter_df_temp = twitter_df [twitter_df['summary_id'] ==row['summary_id'] ]
        data = create_tweet_area(row['search_keyword'] , row['ad'],twitter_df_temp)
        output_text = output_text + data + "\n\n"

    #まとめ
    d = get_collect_setting('end_cap')
    output_text = output_text + d + "\n"


    output_text = output_text + "\n[/div]"

    f = codecs.open('twitter_blog_output.txt', 'w', "utf_8_sig")  # 書き込みモードで開く
    f.write(output_text)  # シーケンスが引数。
    f.close()
