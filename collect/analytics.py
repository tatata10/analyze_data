# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 16:54:49 2023

@author: kawai taichi
"""

from .dataDao import dataDao
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression # 線形回帰モデル
from sklearn.metrics import mean_squared_error # 平均二乗誤差
#from flask import Flask, make_response
import io
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB# 分類器の学習
import random
import os
import csv
import datetime
from sklearn.preprocessing import LabelEncoder


class analytics():
    def __init__(self):
        self.result1 = ""
        self.my_array = []
        
    #並びでどの程度設定を入れるかを見つける
    def regression_analysis(self, date1, date2):
        #回帰分析をするデータをデータベースから取得する
        dao = dataDao()
        data_arr = dao.select_data(date1, date2)
        model = LinearRegression() # モデルのインスタンスを作成
        # DataFrameを作成
        #df = pd.DataFrame(data_arr[1:], columns=[data_arr[0,0],data_arr[0,1],data_arr[0,2],data_arr[0,3],data_arr[0,4],data_arr[0,5],data_arr[0,6],data_arr[0,7],data_arr[0,8],data_arr[0,0]])
        # データセットの読み込み
        #boston = load_boston()
        X = []
        y = []
        for i in range(0,len(data_arr)):
            j = i+1
            if j<len(data_arr):
                X.append(data_arr[i].difference) # 部屋数
                y.append(data_arr[j].difference) # 住宅価格
                
        X = np.array(X) # リストをNumPyの配列に変換
        y = np.array(y) # リストをNumPyの配列に変換
            
        # データの可視化
        plt.scatter(X, y) # 散布図をプロット
        fig = plt.gcf() # 現在のfigureオブジェクトを取得
        plt.xlabel("左の台") # x軸のラベル
        plt.ylabel("その隣の台") # y軸のラベル
        
        
        canvas = FigureCanvasAgg(fig) # キャンバスオブジェクトを作成
        response = HttpResponse(content_type='image/png') # レスポンスオブジェクトを作成
        canvas.print_png(response) # PNG形式でグラフを出力し、レスポンスに書き込む
        
         # 線形回帰モデルの作成
        
        model.fit(X.reshape(-1, 1), y) # モデルにデータを学習させる
                
# =============================================================================
#         # 図をpngデータとしてバッファに保存する
#         buf = io.BytesIO() # バッファの作成
#         plt.savefig(buf, format="png") # バッファにpngデータとして保存
#         plot_data = buf.getvalue() # バッファからバイナリデータを取得
# =============================================================================
        
       
        
        # 回帰係数と切片を表示
        print("Coef:", model.coef_) # 回帰係数（傾き）
        print("Intercept:", model.intercept_) # 切片
        
        # 回帰直線を描画
        
        
        plt.plot(X, model.predict(X.reshape(-1, 1)), color="red") # 回帰直線をプロット
        plt.xlabel("Rooms") # x軸のラベル
        plt.ylabel("Price") # y軸のラベル
        #plt.show()
        
        # モデルの評価（平均二乗誤差）
        mse = mean_squared_error(y, model.predict(X.reshape(-1, 1))) # 平均二乗誤差を計算
        #print("MSE:", mse) # 平均二乗誤差を表示
        
        return model,mse
    
    #設定投入台をランダムフォレストで予測する
    def predict_analytics(self, date1, date2):
        #回帰分析をするデータをデータベースから取得する
        dao = dataDao()
        data_arr = dao.select_data(date1, date2)
        
        print(data_arr)
        data_value = data_arr.values("storeName","date","modelName","number","game","difference","BB","RB","allprobability",
        "BBprobability","RBprobability") # 辞書のリストに変換
        print(data_value)
        # DataFrameを作成
        df = pd.DataFrame(data_value)
        print("df",df)
        
        analytics.make_csv(df)
        
        # 特徴量とラベルに分割
        X = df.drop(["date","modelName","game","difference","BB","RB","allprobability",
        "BBprobability","RBprobability"], axis=1) # 台番号(number)以外を特徴量とする
        y = df[["number"]] # 台番号(number)をラベルとする
        
        #特徴量の確認
        print(X.head())
        
        #ターゲットの確認
        print(y.head())
        
        # カテゴリカルデータのエンコーディング
        label_encoder = LabelEncoder()
        X['modelName'] = label_encoder.fit_transform(X['modelName'])
        X['曜日'] = label_encoder.fit_transform(X['曜日'])
        
        # ランダムフォレストモデルの作成と学習
        model = RandomForestClassifier()
        model.fit(X, y)
        
        # 次回の予測を行う
        # test.csvは次回にボールを入れる前に確認した箱の状態を保存したファイルとする
        # カラムはbox1, box2, ball1, ball2, ..., weekday, dateとする
        test = pd.read_csv("test.csv")
        
        # ボールの数が変わっているかどうかをチェックする
        if len(test.columns) == len(df.columns): # ボールの数が変わっていない場合
            # 予測値を出力
            pred = model.predict(test.drop(["box1", "box2"], axis=1)) # box1とbox2以外のカラムを入力とする
            print(pred)
        else: # ボールの数が変わっている場合
            # ボールの数を取得する
            n_balls = len(test.columns) - 4 # weekdayとdateを除いたカラムの数がボールの数
            
            # 新しい特徴量を作成する
            new_X = test.copy() # testデータをコピーする
            new_X["n_balls"] = n_balls # ボールの数を新しいカラムとして追加する
            
            # 予測値を出力
            pred = model.predict(new_X.drop(["box1", "box2"], axis=1)) # box1とbox2以外のカラムを入力とする
            print(pred)
        
        return pred
    
    #設定を確率ベクトルで予測する
    def predict_setting(self, date1, date2):
        #回帰分析をするデータをデータベースから取得する
        dao = dataDao()
        data_arr = dao.select_data(date1, date2)
        standard_arr = dao.standard_data()
        
# =============================================================================
#         data_value = data_arr.values("storeName","date","modelName","number","game","difference","BB","RB","allprobability",
#         "BBprobability","RBprobability") # 辞書のリストに変換
#         # DataFrameを作成
#         df = pd.DataFrame(data_value)
# =============================================================================
        
        for i in data_arr:
            # standard_dataから取得したデータ
            st_data = dao.standard_data(i.name)
            if st_data[0].allprobability == 0 & st_data[0].BBprobability == 0 & st_data[0].RBprobability == 0:
                return
            elif st_data[0].RBprobability == 0:
                p1 = [1/st_data[0].allprobability,1/st_data[0].BBprobability,]
                p2 = [1/st_data[1].allprobability,1/st_data[1].BBprobability,]
                p3 = [1/st_data[2].allprobability,1/st_data[2].BBprobability,]
                p4 = [1/st_data[3].allprobability,1/st_data[3].BBprobability,]
                p5 = [1/st_data[4].allprobability,1/st_data[4].BBprobability,]
                p6 = [1/st_data[5].allprobability,1/st_data[5].BBprobability,]
                
            elif st_data[0].RBprobability == 0:
                p1 = [1/st_data[0].allprobability,1/st_data[0].BBprobability,1/st_data[0].RBprobability,]
                p2 = [1/st_data[1].allprobability,1/st_data[1].BBprobability,1/st_data[1].RBprobability,]
                p3 = [1/st_data[2].allprobability,1/st_data[2].BBprobability,1/st_data[2].RBprobability,]
                p4 = [1/st_data[3].allprobability,1/st_data[3].BBprobability,1/st_data[3].RBprobability,]
                p5 = [1/st_data[4].allprobability,1/st_data[4].BBprobability,1/st_data[4].RBprobability,]
                p6 = [1/st_data[5].allprobability,1/st_data[5].BBprobability,1/st_data[5].RBprobability,]
                
            elif st_data[0].allprobability != 0 & st_data[0].BBprobability != 0 & st_data[0].RBprobability != 0:
                p1 = [1/st_data[0].allprobability,1/st_data[0].BBprobability,1/st_data[0].RBprobability,]
                p2 = [1/st_data[1].allprobability,1/st_data[1].BBprobability,1/st_data[1].RBprobability,]
                p3 = [1/st_data[2].allprobability,1/st_data[2].BBprobability,1/st_data[2].RBprobability,]
                p4 = [1/st_data[3].allprobability,1/st_data[3].BBprobability,1/st_data[3].RBprobability,]
                p5 = [1/st_data[4].allprobability,1/st_data[4].BBprobability,1/st_data[4].RBprobability,]
                p6 = [1/st_data[5].allprobability,1/st_data[5].BBprobability,1/st_data[5].RBprobability,]
                
                # アナスロから取得したデータ
                data = np.array([data_arr.allprobability,data_arr.BB,data_arr.RB])
                
                # アナスロから取得したデータ
                data = np.array([data_arr.allprobability,data_arr.BB])
            elif st_data[0].allprobability != 0 & st_data[0].BBprobability != 0 & st_data[0].RBprobability != 0:
                p1 = [1/st_data[0].allprobability,1/st_data[0].BBprobability,1/st_data[0].RBprobability,]
                p2 = [1/st_data[1].allprobability,1/st_data[1].BBprobability,1/st_data[1].RBprobability,]
                p3 = [1/st_data[2].allprobability,1/st_data[2].BBprobability,1/st_data[2].RBprobability,]
                p4 = [1/st_data[3].allprobability,1/st_data[3].BBprobability,1/st_data[3].RBprobability,]
                p5 = [1/st_data[4].allprobability,1/st_data[4].BBprobability,1/st_data[4].RBprobability,]
                p6 = [1/st_data[5].allprobability,1/st_data[5].BBprobability,1/st_data[5].RBprobability,]
            
            # ベクトルの内積を計算
            similarity = [np.dot(data, p) for p in [p1, p2, p3,p4,p5,p6]]
            
            # 最も類似度が高いくじを選択
            most_similar = np.argmax(similarity) + 1
            
            if i.game < 1000:             
                most_similar = 1
            elif i.difference > 2000:
                if most_similar <6:
                    most_similar += 1
            elif i.difference < 2000:
                if most_similar > 1:
                    most_similar -= 1
                    
            obj = data(setting = most_similar)
            obj.save()
            
    #設定の投入傾向をつかむ
    def predict_trend(self, date1, date2):
        #回帰分析をするデータをデータベースから取得する
        dao = dataDao()
        data_arr = dao.select_data(date1, date2)
        
        i = 0
        # 下の１日のデータを配列に入れる
        date_list = []
        # １日の全てのデータを入れる
        date_data = []
        predate = ""
        #日付ごとにわけて配列に格納
        for data in data_arr:
            print(vars(data))
            print(data.modelName)
            print(data.date)
            if data.date != predate:
                date_list.append(date_data)
            else :
                date_data.append(data)
                print("一日のデータ",data)
                
            predate = data.date
            
        print("全てのデータ",date_list)
        # 一日ごとのデータの確認する
        
        # 次の日の当たり台を予測
        def marcif(self, date1, date2):
            # サンプルデータ（過去の手の履歴）
            history = ['グー', 'チョキ', 'パー', 'グー', 'グー', 'チョキ', 'パー', 'グー', 'チョキ', 'パー']
            
            # マルコフ連鎖の遷移行列を作成
            transition_matrix = {
                'グー': {'グー': 0, 'チョキ': 0, 'パー': 0},
                'チョキ': {'グー': 0, 'チョキ': 0, 'パー': 0},
                'パー': {'グー': 0, 'チョキ': 0, 'パー': 0}
            }
            
            # 遷移行列のカウントを更新
            for i in range(len(history) - 1):
                current_hand = history[i]
                next_hand = history[i + 1]
                transition_matrix[current_hand][next_hand] += 1
            
            # 遷移確率を計算
            for current_hand, transitions in transition_matrix.items():
                total = sum(transitions.values())
                for next_hand in transitions:
                    if total > 0:
                        transition_matrix[current_hand][next_hand] /= total
            
                # 次の手を予測する関数
            def predict_next_hand(current_hand):
                if current_hand not in transition_matrix:
                    return random.choice(['グー', 'チョキ', 'パー'])
                next_hands = list(transition_matrix[current_hand].keys())
                probabilities = list(transition_matrix[current_hand].values())
                return random.choices(next_hands, probabilities)[0]
            
            # 現在の手を入力して次の手を予測
            current_hand = 'グー'
            predicted_hand = predict_next_hand(current_hand)
            print(f'次の手の予測: {predicted_hand}')
            
            
# =============================================================================
#     取得データのcsv出力
# =============================================================================
    def make_csv(data):
        #フォルダのパス作成
        csv_dir_path = './collect/tmp/'
        if os.path.isfile(csv_dir_path):
            # フォルダ作成
            os.mkdir(csv_dir_path)
        
        dt = datetime.datetime.now()
        formatted_date = dt.strftime("%Y-%m-%d-%H-%M-%S")
        csv_filename = formatted_date + '.csv'
        print(csv_filename)
        
        data.to_csv(csv_dir_path + csv_filename, index=False,encoding='shift-jis')
            
# =============================================================================
#         with open(new_dir_path+'/sample.csv', 'w') as f:
#             writer = csv.writer(f)
#             writer.writeheader(data)
#             writer.writerows(data)
#             
#         f.close()
# =============================================================================
            
            
        
                
        
        
    
    

    

