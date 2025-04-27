# -*- coding: utf-8 -*-
#from django.urls import path
from . import views
from django.urls import path, include, re_path
from django.contrib import admin
from .analytics import analytics

urlpatterns = [
             path('home',views.home,name='home'),
             path('index',views.index,name='index'),
             path('index/datalist',views.datalist,name='datalist'),
             path('regist_storename',views.index,name='regist_storename'),
             path('form',views.form,name='form'),
             path('study',views.study,name='study'),
             #path('excel',views.form,name='excel'),
             path('admin/', admin.site.urls),
             re_path(r'mplimage.png', analytics.regression_analysis),
             ]
