import cv2
from matplotlib import pyplot as plt
import numpy as np

def get_hsv_report(rgb_image, plot_show = False, statistics_show=False):
    """hsv票色系の対応
        Args:
            rgb_image(obj): rgbイメージ画像
            plot_show(bool): hsv票色系のグラフをプロットするか
            statistics_show(bool):標準偏差を出力するか(処理が思い)

        Returns:
           hsv票色系のパーセントタイルの値
    """
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV) # hsv票色系に変換
    h,s,v = cv2.split(hsv) # 各成分に分割
    
    def get_percentile_list(k, datas):
        #パーセントタイルを 5,50,95パーセントとする
        #パーセントタイルを利用して、輝度より明るい、暗い画像を判定などに利用する
        percentile = [5,50,95]
        out_datas = {}
        for i in percentile:
            value = np.percentile(np.array(datas), i)
            #out_datas.append(value)
            s = k + "_"+str(i) 
            out_datas[s] = value
        return out_datas
    
    out_dict = {}

   
    #色相
    if(plot_show == True):
        plt.figure(figsize=(8, 5))
        plt.hist(h.ravel(),256,[0,256], color="red", alpha=0.7, histtype="step", label="Hue")
    data = get_percentile_list("h_per",h.ravel())
    out_dict.update(data)
    
    if(statistics_show == True):
        out_dict['h_pstdev'] =  statistics.pstdev(h.ravel()/255)
    
    #彩度
    if(plot_show == True):
        plt.hist(s.ravel(),256,[0,256], color="green",  alpha=0.7, histtype="step", label="Saturation")
    data = get_percentile_list("s_per",h.ravel())
    out_dict.update(data)
    if(statistics_show == True):
        out_dict['s_pstdev'] =  statistics.pstdev(s.ravel()/255)
    
    #輝度
    if(plot_show == True):
        plt.hist(v.ravel(),256,[0,256], color="blue",  alpha=0.7, histtype="step",label="Value")
        plt.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=10)
        plt.show()
        
    data = get_percentile_list("v_per",v.ravel())
    out_dict.update(data)
    if(statistics_show == True):
        out_dict['v_pstdev'] =  statistics.pstdev(v.ravel()/255)
    
    return out_dict
    

def gamma_correction(image,gamma):  
    
    """ガンマ補正を利用して、画像を明るくしたり暗くしたりする


    Args:
        image(obj): イメージ画像
        gamma(float): ガンマ値  0〜1までは、暗くする、1以上は明るくする
        
    Returns:
       ガンマ補正後のイメージ画像

    """
    # 整数型で2次元配列を作成[256,1]  
    lookup_table = np.zeros((256, 1), dtype = 'uint8')  
    for loop in range(256):  
        # γテーブルを作成  
        lookup_table[loop][0] = 255 * pow(float(loop)/255, 1.0/gamma)  

    # lookup Tableを用いて配列を変換 
    image_gamma = cv2.LUT(image, lookup_table) 
    
    return image_gamma
    # 変換後のファイルを保存  
    


def get_rgb_report(rgb_image, plot_show = False, plot_title= "rgb",  statistics_show=False):
    """brgのヒストグラム・レポートを表示する
        Args:
            rgb_image(obj): rgbイメージ画像
            plot_show(bool): ヒストグラムのグラフをプロットするか
            statistics_show(bool):標準偏差を出力するか(処理が思い)

        Returns:
            rgb分布のパーセントタイルの値
    """
    #print(rgb_image.shape)
    r,g,b = cv2.split(rgb_image) # 各成分に分割

    def get_percentile_list(k, datas):
        #パーセントタイルを 5,50,95パーセントとする
        #パーセントタイルを利用して、RGBの偏りを判定する
        percentile = [5,50,95]
        out_datas = {}
        for i in percentile:
            value = np.percentile(np.array(datas), i)
            #out_datas.append(value)
            s = k + "_"+str(i)
            out_datas[s] = value
        return out_datas
    
    out_dict = {}

    #赤
    data = get_percentile_list("r_per",r.ravel())
    out_dict.update(data)
    if(statistics_show == True):
        out_dict['r_pstdev'] =  statistics.pstdev(r.ravel()/255)
    
    #緑
    data = get_percentile_list("g_per",g.ravel())
    out_dict.update(data)
    if(statistics_show == True):
        out_dict['g_pstdev'] =  statistics.pstdev(g.ravel()/255)
    
    #青   
    data = get_percentile_list("b_per",b.ravel())
    out_dict.update(data)
    if(statistics_show == True):
        out_dict['b_pstdev'] =  statistics.pstdev(b.ravel()/255)
    
    #ヒストグラムの描画
    if(plot_show == True):
        plt.figure(figsize=(8, 5))
        plt.title(plot_title)
        rgb_image = np.asarray(rgb_image.reshape(-1,3))
        plt.hist(rgb_image, color=["red", "green", "blue"], histtype="step", bins=128)
        plt.show()
    
    return out_dict

def total_image_report(rgb_image):
    """イメージの特徴レポートを出す
        Args:
            rgb_image(obj): rgbイメージ画像

        Returns:
            画像の特徴量
    """
    
    #hsv票色系のデータ
    data_dicts = get_hsv_report(rgb_image)
    
    #rgbの情報
    data = get_rgb_report(rgb_image)
    data_dicts.update(data)
    
    #ボケの数値
    p = cv2.Laplacian(rgb_image, cv2.CV_64F).var()
    data_dicts['blur'] = p
    
    return data_dicts



def boxs_image_split_summary(src_img, boxs, src_img_show=False, rgb_show=False, hsv_show = False, save_path=""):
    """
    ・boxで囲まれた画像をファイルに出力する
     ファイル名＝画像name_X_Ypot
    ・フラグでヒストグラム、HSVを出す
    ・サマリーのRGBの分布を書く
    ・サマリーのHSVの分布を書く
    →削除すべき背景を見つける
    """
    #サマリ用のRGB
    rgb_image_sum = np.empty([2, 3])
    hsv_image_sum = np.empty([2, 3])
    rgb_image = np.asarray(img.reshape(-1,3))

    for box in boxs:
        box = [int(i) for i in box]

        img_harf = img[ box[1] : box[3] , box[0]: box[2] ]  #配列の意味 [　横の範囲,  縦(高さ)の範囲]
        
        #画像保存
        if(len(save_path)>0):
            bgr_img = cv2.cvtColor(img_harf, cv2.COLOR_RGB2BGR)
            #ファイル名
            basename_without_ext = os.path.splitext(os.path.basename(save_path))[0]
            dirname = os.path.dirname(save_path)
            add_name = "x_%d_y_%d"% ( box[0],  box[1])
            s = f'{dirname}/{basename_without_ext}_{add_name}.jpg'
            cv2.imwrite(s, bgr_img)
        
        #RGBイメージの保存
        rgb_image = np.asarray(img_harf.reshape(-1,3))
        rgb_image_sum = np.append(rgb_image_sum, rgb_image, axis=0)

         # hsv票色系に変換
        hsv_harf = cv2.cvtColor(img_harf, cv2.COLOR_BGR2HSV)
        hsv_harf = np.asarray(hsv_harf.reshape(-1,3))
        hsv_image_sum = np.append(hsv_image_sum, hsv_harf, axis=0)
        
        #ラベルを描画する
        if(src_img_show == True):
            fig, ax = plt.subplots(1, 1, figsize=(8, 8))
            ax.imshow(img_harf)
            
        #RGBのヒストグラムを書く
        if( rgb_show==True ):
            open_cv_sample_func.get_rgb_report(img_harf, plot_show= True)
        
        
        #HSVのヒストグラムを書く
        if(hsv_show == True):
            open_cv_sample_func.get_hsv_report(img_harf, plot_show= True)
            
    return rgb_image_sum, hsv_image_sum

def plot_rgb_hsv_image(image_path, image_id):
    #rgb_hsv画像をプロットする
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxs,_ = get_boxs(train_df, image_id)
    rgb_image_sum,hsv_image_sum =   boxs_image_split_summary(img, boxs, src_img_show=True, rgb_show=True, hsv_show = True, save_path = "./out_image/0a181bbb4")

    
    plt.figure(figsize=(12, 9))
    plt.hist(rgb_image_sum, color=["red", "green", "blue"], histtype="step", bins=128)
    plt.title("rgb_summary")
    plt.show()    
    
    plt.figure(figsize=(12, 9))
    plt.hist(hsv_image_sum,256,[0,256], color=["red", "green", "blue"], alpha=0.7, histtype="step", label=["Hue","Saturation","Value"])
    plt.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=10)
    plt.title("hsv_summary")
    plt.show()

#使い方の例
#img1 = cv2.imread('file_name.jpg')
#img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
#data = get_hsv_report(img1,True)
#print(data)

#img1 = cv2.imread('file_name.jpg')
#img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
#data = total_image_report(img1)
#print(data)

#plot_rgb_hsv_imageの使い方
#plot_rgb_hsv_image("./train/0a181bbb4.jpg", "0a181bbb4")