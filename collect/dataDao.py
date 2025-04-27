# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 10:38:00 2023

@author: kawai taichi
"""
from .models import data
from .models import standard_data
import datetime

class dataDao():
    def __init__(self):
        self.url = ""
        self.my_array = []
        
    #データベースにデータを格納
    def insert_data(self,date,storeName,data_arr):
        #日付から曜日を取得
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        # 曜日を取得 (0=月曜日, 6=日曜日)
        weekday = date_obj.weekday()
        
        # 曜日を文字列で取得
        weekday_str = date_obj.strftime("%A")
        for i in range(1,len(data_arr)):
            if len(data_arr[i])==9:
                obj = data(storeName=storeName,
                       date=date,
                       week=weekday_str,
                       modelName=data_arr[i][0],
                       number = data_arr[i][1],
                       game = data_arr[i][2],
                       difference = data_arr[i][3],
                       BB = data_arr[i][4],
                       RB = data_arr[i][5],
                       allprobability = data_arr[i][6],
                       BBprobability = data_arr[i][7],
                       RBprobability = data_arr[i][8])
                obj.save()
    
    def test_data(self,name):
        #selected_data = data.objects.filter(date=(date1, date2))
        selected_data = data.objects.filter(storeName=name) 
        return selected_data
    
    def select_data(self,date1,date2):
        selected_data = data.objects.filter(date__range=(date1, date2))
        return selected_data
    
    def check_data(self,date3,name):
        check_data = data.objects.filter(date=date3,storeName=name)
        print("checkdao")
        return check_data
    
    def standard_data(self,name):
        #selected_data = data.objects.filter(date=(date1, date2))
        selected_data = standard_data.objects.filter(storeName=name) 
        return selected_data
    
    def standard_Alldata(self):
        #selected_data = data.objects.filter(date=(date1, date2))
        selected_data = standard_data.objects.all() 
        return selected_data