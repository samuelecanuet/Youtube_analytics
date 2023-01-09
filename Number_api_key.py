# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 20:43:28 2023

@author: samue
"""
import json


with open('historique/watch-history.json', 'r', encoding="utf8") as f:
  data = json.load(f)


number_vid = len(data)

if len(data) >= 10*9500:
    print("The number of request ask for your data set it is over the limit. \n Please minimize the data list. Reedit the programme Youtube_analytics.py in consequence")
else:
    print("You have to create {} APIs keys.".format(int(len(data)/9500)+1))