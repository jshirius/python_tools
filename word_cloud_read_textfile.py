
# coding: utf-8



'''
文章データから、形態素解析するサンプル。
取り出した語句についてWordCloudで可視化までする
'''

import re
import pickle
import sys
from janome.tokenizer import Tokenizer
import codecs
import mysql.connector
from wordcloud import WordCloud


#文章データテキストファイルから読み込みます
param = sys.argv
if (len(param) == 0):
    print ("Usage: $ python " + param[0] + " number")
    quit()

f = codecs.open(param[1],'r',)
src_txt = f.read()
f.close()

#セパレータを「。」とする。
seperator = "。"
mixi_diary_origin = src_txt
mixi_diary_origin = re.sub("[｜ 　「」\n]", "", mixi_diary_origin) # | と全角半角スペース、「」と改行の削除


mixi_diary_list = mixi_diary_origin.split(seperator)  # セパレーターを使って文章をリストに分割する
mixi_diary_list = [x+seperator for x in mixi_diary_list]  # 文章の最後に。を追加

#この時点でデータの準備が終わりです
#ここから形態素分析に入ります
t = Tokenizer()

mixi_diary_words = []  #形態素分析したあとに出てきた語句を格納するリスト(この例では、名詞、形容詞のみの語句を取っています)
for sentence in mixi_diary_list:
    
    tokens = t.tokenize(sentence)
    words = []
    for token in tokens:
        # 品詞を取り出し
        partOfSpeech = token.part_of_speech.split(',')[0]
 
        if partOfSpeech == u'名詞'  or  partOfSpeech == u'形容詞' :
            #print (token.surface)
            words.append(token.surface)
    
    if len(words) > 0:
        mixi_diary_words.extend(words)
    


# In[2]:

#ここからWordCloudの処理
#mixi_diary_wordsは、WordCloudで使えるように2次元の配列(行列)になっているので、1次元の配列(ベクトル)に変換する
text = ""
for x in mixi_diary_words:
    text = text + x + " "

wordcloud = WordCloud(background_color="white",
    font_path="/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",
    width=800,height=600).generate(text)

#画像ファイルに保存する
wordcloud.to_file("./wordcloud_data.png")

#文字数をカウントする


# In[3]:

#折角なので文字数も求めてみる
from collections import Counter
c =  Counter(mixi_diary_words)
d = c.most_common()

print(d)
# In[ ]:



