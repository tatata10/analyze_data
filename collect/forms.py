# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 14:35:41 2023

@author: kawai taichi
"""

from django import forms

class CollectForm(forms.Form):
    name = forms.CharField(label='name')
    mail = forms.CharField(label='mail')
    age = forms.IntegerField(label='age')