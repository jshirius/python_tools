
# coding: utf-8



'''
文章データから、形態素解析して、文字列に対して感情分析を実施する

単語感情極性対応表は、以下のものを使わせていただきました。

参考資料：
高村大也, 乾孝司, 奥村学
"スピンモデルによる単語の感情極性抽出", 情報処理学会論文誌ジャーナル, Vol.47 No.02 pp. 627--637, 2006.
http://www.lr.pi.titech.ac.jp/~takamura/pndic_ja.html
'''

import re
import sys
from janome.tokenizer import Tokenizer
import codecs


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



#文章データテキストファイルから読み込みます
param = sys.argv
if (len(param) == 0):
    print ("Usage: $ python " + param[0] + " number")
    quit()

f = codecs.open(param[1],'r',)
src_txt = f.read()
f.close()


#単語感情極性対応表データを取得する
dic_pn = read_pn_di()




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

semantic_value = 0
semantic_count = 0
for sentence in mixi_diary_list:
    
    tokens = t.tokenize(sentence)
    words = []
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
 #if partOfSpeech == u'名詞'  or  partOfSpeech == u'形容詞' :
            #print (token.surface)
        words.append(token.surface)
    
    if len(words) > 0:
        mixi_diary_words.extend(words)
    
data = "分析した単語数:" +  str(semantic_count) +  " 感情極性実数値合計:" + str(semantic_value) + " 感情極性実数値平均値:" + str(semantic_value / semantic_count)
print(data)

    

#折角なので文字数も求めてみる
from collections import Counter
c =  Counter(mixi_diary_words)
d = c.most_common()

print(d)
# In[ ]:



