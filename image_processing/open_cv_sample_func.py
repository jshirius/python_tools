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



#使い方の例
#img1 = cv2.imread('file_name.jpg')
#img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
#data = get_hsv_report(img1,True)
#print(data)

#img1 = cv2.imread('file_name.jpg')
#img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
#data = total_image_report(img1)
#print(data)