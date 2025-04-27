# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 14:18:09 2023

@author: kawai taichi
"""

import requests
import re
import pandas as pd
from fractions import Fraction
from openpyxl import Workbook

# アナスロからスロットのデータを取得する
class getdata():
    def __init__(self):
        self.url = ""
        self.my_array = []

    def culcurate(self,url):
        # URLからHTMLを取得
        self.url = url
        print(url)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                   "Referer": "https://ana-slo.com/%e3%83%9b%e3%83%bc%e3%83%ab%e3%83%87%e3%83%bc%e3%82%bf/%e6%9d%b1%e4%ba%ac%e9%83%bd/arrow%e6%b1%a0%e4%b8%8a%e5%ba%97-%e3%83%87%e3%83%bc%e3%82%bf%e4%b8%80%e8%a6%a7/"}
        response = requests.post(self.url,headers)
        s = response.text
        print("anaslo data",s)
        # スライスを使って部分文字列を取得する
        sss = s[s.find('<h4>全データ一覧</h4>'):s.find('機種別データピックアップ')]

        yyy = re.sub(r'<p>.+?</p>', '', sss)
        xxx = re.sub(r'<.+?>', '/', yyy)
        zzz = xxx.split("/\n/\n/\n/")
        new_arr = []
        for i in zzz:
            temp_arr = i.split("/")
            temp_arr = [x.replace("\n", "") for x in temp_arr]
            while "" in temp_arr:
                temp_arr.remove("")
            new_arr.append(temp_arr)

        new_arr1 = []
    
        for i in range(1,len(new_arr)):
                temp_arr1 = []
                if i > 1:
                    for j in range(len(new_arr[i])):
                        if j == 2 or j == 3:
                            temp_arr1.append(int(new_arr[i][j].replace(",", "")))
                        elif j == 7 or j == 9 or j == 11:
                            continue
                        elif j == 6 or j == 8 or j == 10:
                            if float(new_arr[i][j+1]) == 0:
                                temp_arr1.append(float(new_arr[i][j+1]))
                                j+=1                 
                            else:                 
                                temp_arr1.append(round(1/(float(new_arr[i][j])/float(new_arr[i][j+1])),2))
                        else:
                            temp_arr1.append(new_arr[i][j])
                else:
                    for j in range(len(new_arr[i])):
                         temp_arr1.append(new_arr[i][j])
                new_arr1.append(temp_arr1)
        
        self.my_array = new_arr1
        return new_arr1
    
    def makeExcel(self,my_array):
        # Excelファイルの作成
        wb = Workbook()
        ws = wb.active
      
        # 配列の内容をExcelファイルに書き込む
        for row in my_array:
            ws.append(row)
      
        # Excelファイルを保存する
        wb.save('my_file.xlsx')

    



    