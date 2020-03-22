#CSVファイルの重複文章に対してマークを付けるサンプル(英語版)
#重複文章は、doc2vecを使って検出する


from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import pandas as pd

def creat_doc2vec_model(tagged_documents):
    # size：分散表現の次元数
    # window：対象単語を中心とした前後の単語数
    # min_count：学習に使う単語の最低出現回数
    # epochs:epochs数
    # dm：学習モデル=DBOW（デフォルトはdm=1で、学習モデルはDM）
    model = Doc2Vec(documents=tagged_documents,
                    vector_size=100,
                    min_count=5,
                    window=5,
                    epochs=20,
                    dm=0)

    return model

def csv_data_duplication_mark(df, text_col ,doc_id_col, duplication_mark_col_name, duplicate_value):

    #初期値として０を設定している
    df[duplication_mark_col_name] = 0

    #前処理として余計な改行、前後の余白を取る
    tagged_documents = []
    for index, row in df.iterrows():

        sentence = row[text_col].strip()
        sentence = sentence.split()
        #ドキュメントIDはpandas内の変数とする
        tagged_documents.append(TaggedDocument(sentence, [ row[doc_id_col] ]))  # TaggedDocument型のオブジェクトをリストに格納

    #モデルを作成する
    model = creat_doc2vec_model(tagged_documents)

    print(model.docvecs.most_similar(160))

    #重複の文章かどうか判定する
    count = 0 #デバッグ様に個数を出す

    #処理用(for文の中で更新する)に
    df2 = df.copy()

    for index, row in df2.iterrows():

        #すでにマークが付いているか確認する
        #if(row[duplication_mark_col_name] > 0):
        if(df.loc[ index, duplication_mark_col_name] > 0):
            print("重複判定済み:%s" % str(df.loc[ index, doc_id_col] ))
            continue

        for p in model.docvecs.most_similar( row[doc_id_col] ):
            if(p[1] > duplicate_value):
                print(p[0]) #p[0]は doc_id_colのidに当たるもの
                
                #該当IDの列にマークを付ける(すでにマークが付いているときは更新しない)
                #マークは、重複元のID(つまりオリジナルのID)をセットしている
                df.loc[df[doc_id_col]==p[0], [duplication_mark_col_name]] = row[doc_id_col]


                count +=1
       

    print("重複検出個数は%d" % count)

    return df

#テストコード
nlp_train_df = pd.read_csv('./train.csv')
print(nlp_train_df)
df = csv_data_duplication_mark(nlp_train_df, "text", "id", "duplication_mark",  0.9993432760238647)
df.to_csv("result.csv")

#重複列を消す(条件に合うもののみ取得)
df = df[df['duplication_mark'] == 0]
df.to_csv("remove_result.csv")
