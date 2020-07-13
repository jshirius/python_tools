def get_hsv_report(rgb_image, plot_show = False, statistics_show=False):
        """hsv票色系の対応
        Args:
            rgb_image(obj): rgbイメージ画像
            plot_show(bool): hsv票色系のグラフをプロットするか
            statistics_show(bool):標準偏差を出力するか(処理が思い)

        Returns:
           hsv票色系のパーセントタイルの値

        """
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV) # hsv票色系に変換
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
    
    plt.figure(figsize=(8, 5))
    
    #色相
    if(plot_show == True):
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
    