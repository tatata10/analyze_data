from . import views
from . import webapi
from django.urls import path, include, re_path
from django.contrib import admin

urlpatterns = [
    path('', views.main, name='main'),  # 例: トップページ
    path('predict', webapi.predict, name='predict'),
]