###########################################################
#分析などで汎用的に使えるpythonコードのまとめ
###########################################################


#Dataの確認を一気に行う
def description(df):
    summary = pd.DataFrame(df.dtypes,columns=['dtypes'])
    summary = summary.reset_index()
    summary['Name'] = summary['index']
    summary = summary[['Name','dtypes']]
    summary['Missing'] = df.isnull().sum().values    
    summary['Uniques'] = df.nunique().values
    summary['First Value'] = df.iloc[0].values
    summary['Second Value'] = df.iloc[1].values
    summary['Third Value'] = df.iloc[2].values
    return summary
    

'''Function to reduce the DF size'''
# source: https://www.kaggle.com/kernels/scriptcontent/3684066/download

def reduce_mem_usage(df):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.        
    """
    start_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    
    return df



#df(それぞれ1列とする)を２つわたし、差分のdfを作成する
def df_word_counter_diff(df_1, df_1_column_name, output_df_1_column_name, df_2, df_2_column_name, output_df_2_column_name):

    df_1_2 = pd.DataFrame()

    #df_1側の処理をする
    tweet_list = []
    for data in tqdm(df_1[df_1_column_name]):
        d = data.split()
        tweet_list.extend(d)

    a = Counter(tweet_list)
    a = a.most_common()
    a = dict(a)
    keys = [k for k, v in a.items()]
    values = [v for k, v in a.items()]
    df_1_2['word_name'] = keys
    df_1_2[output_df_1_column_name] = values
    

    #df_2側の処理をする
    tweet_list = []
    for data in tqdm(df_2[df_2_column_name]):
        d = data.split()
        tweet_list.extend(d)

    b = Counter(tweet_list)
    b = b.most_common()
    b = dict(b)
    df_1_2[output_df_2_column_name]  = 0

    for k, v in b.items():
        data = df_1_2[ df_1_2.word_name == k ] 
        
        if(len(data) > 0):
            #print(data)
            df_1_2.loc[data.index , output_df_2_column_name] = v
        else:
            #行の追加
            s = pd.Series([k, 0, v], index=df_1_2.columns, name='FOUR')
            df_1_2 = df_1_2.append(s)

    return df_1_2
    #if( tweet_0_1_df[ tweet_0_1_df.word_name == k ]  == True):


#状況をトラッキング
def update_tracking(
                    run_id, field, value, csv_file="./tracking.csv",
                    integer=False, digits=None, nround=6,
                    drop_broken_runs=False):
    """
        Tracking function for keep track of model parameters and
        CV scores. `integer` forces the value to be an int.
        """
    try:
        df = pd.read_csv(csv_file, index_col=[0])
    except:
        df = pd.DataFrame()
    if drop_broken_runs:
        df = df.dropna(subset=['1_f1'])
    if integer:
        value = round(value)
    elif digits is not None:
        value = round(value, digits)
    df.loc[run_id, field] = value  # Model number is index
    df = df.round(nround)
    df.to_csv(csv_file)

update_tracking(run_id, 'col_name', 'data')
