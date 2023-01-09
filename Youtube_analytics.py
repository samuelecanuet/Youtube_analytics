# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 19:42:29 2023

@author: samue
"""
import time
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
        
import json
import calendar
import matplotlib.pyplot as plt
import isodate
import googleapiclient.discovery
from PIL import Image
import sys
import csv
import urllib
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import numpy as np
from matplotlib.ticker import MaxNLocator


def change_KEY(DEVELOPER_KEY):
    api_service_name = "youtube"
    api_version = "v3"
    return googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    

###################################
list_KEY = ["Your", "APIs", "Keys"]
###################################


with open('historique/watch-history.json', 'r', encoding="utf8") as f:
  data = json.load(f)


number_vid = len(data)
dic_name = {}
dic_date = {}
dic_name_duration={}
dic_date_duration = {}

first_date = str(int(data[-1].get('time')[8:10])) + str(' ') + calendar.month_name[int(data[-1].get('time')[5:7])] + str(' ') + str(int(data[-1].get('time')[0:4]))


data = data

if len(list_KEY) < len(data)/9500:
    print("The number of key in 'list_KEY' is too small")
    print("Add API KEY in the list or reduce the list 'data'\n")
    sys.exit()


printProgressBar(0, len(data), prefix = 'Progress:', suffix = 'Complete', length = 50)
count=0
month_list=[]
year_list=[]

for i in data:
        
        count+=1
        try:
            #dic_name est un dictionnaire permettant de compter le nombre de video vu par youtuber
            name=i.get('subtitles')[0].get('name')
            channel_url=i.get('subtitles')[0].get('url')
            try:
                dic_name[(name, channel_url)] += 1
            except KeyError:
                dic_name[(name, channel_url)] = 1
                
            
            #dic_date est un dictionnaire permettant de compter le nombre de video vu sur la journée
            date = i.get('time')[0:10]
            try:
                dic_date[date] += 1
            except KeyError:
                dic_date[date] = 1
                
            #dic_date_duration est un dictionnaire permattant de compter le temps de video regardé sur la journée
            date = i.get('time')[0:10]

            #changement de clé API pour un nombre de request = 9500 (marge de 500)
            youtube = change_KEY(list_KEY[int(count/9500)])
            
            id_vid = i.get('titleUrl')[-11:]
            request = youtube.videos().list(
                part="statistics,contentDetails",
                id=id_vid
            )
            
            #récupération de la durée d'une video grâce a l'API youtube
            duration = isodate.parse_duration(request.execute().get('items')[0].get('contentDetails').get('duration')).total_seconds()/3600
            
            #exclu les videos plus longues que 5h (live)
            if duration < 5:
                try:
                    dic_date_duration[date] += duration
                except KeyError:
                    dic_date_duration[date] = duration
                    
                    
                try:
                    dic_name_duration[(name, channel_url)] += duration
                except KeyError:
                    dic_name_duration[(name, channel_url)] = duration
             
            #year_list est une liste des différentes années de visionnage
            try:
                month_list.index(date[5:7])
                year_list.index(date[:4])
                
            except ValueError:
                month_list.append(date[5:7])
                year_list.append(date[:4])
                
        except:
            None
            
        printProgressBar(count, len(data), prefix = 'Progress:', suffix = 'Complete', length = 50)
    
print('Nombre de vidéo vu depuis {} : {}\n'.format(first_date, number_vid))

count=0
youtube = change_KEY(list_KEY[-1])
fig, ax = plt.subplots(figsize=(7,5), dpi=150)
plt.xlabel('Number of hours viewed', color='grey')
ax2 = plt.gca().twiny()
ax2.set_xlabel('Number of videos viewed', color='red')
name=[]
v_list=[]
for k, v in sorted(dic_name.items(), key=lambda x: x[1], reverse=True):
    ax2.barh(count-0.1, dic_name_duration.get(k), color='grey', height=0.2)
    plt.barh(count+0.1, v, color='red', height=0.2)   
    v_list.append(v)
    
  
    request = youtube.channels().list(
                    part="statistics,snippet",
                    id=str(k[1][32:])
                )
    img_url=request.execute().get('items')[0].get('snippet').get('thumbnails').get('medium').get('url')
    im=urllib.request.urlretrieve(img_url, k[0]+'.png')

    img = Image.open("./"+k[0]+".png")
    imagebox = OffsetImage(img, zoom = 0.15)    
    ab = AnnotationBbox(imagebox, (v+0.2*v_list[0], count), frameon = False)
    ax2.add_artist(ab)
    
    name.append(k[0])
    
    count+=1
    if count > 4:
        break
plt.xlim(0,max(v_list)*1.5) 
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.yticks(np.arange(5), name)
 
#écriture d'un fichier csv des données extraites
filename = "youtube_duration_{}.csv".format(time.strftime("%Y%m%d-%H%M%S"))
with open(filename, 'w') as f:
    for key in dic_date_duration.keys():
        f.write("%s,%s\n"%(key,dic_date_duration[key]))
 
#lecture du fichier csv pour faire les graphiques
#graphique de la durée de visionnage de youtube pour chaque mois par année

date=[]
duration=[]
with open(filename, newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            date.index(row[0][:7])
            duration[-1]+=float(row[1])
        except ValueError:
            date.append(row[0][:7])
            duration.append(float(row[1]))
ylimit = max(duration)  
year_list=[]            
for year_month in date:
    try :
        year_list.index(year_month[:4])
    except ValueError:
        year_list.append(year_month[:4])

year_month_list = [[] for i in year_list]
duration_list = [[] for i in year_list]

for i in range(len(date)):
    year_month_list[year_list.index(date[i][:4])].append(date[i])
    duration_list[year_list.index(date[i][:4])].append(duration[i])
    

for i in range(len(year_month_list)):
    
    year_month_list[i].reverse()
    duration_list[i].reverse()
    
    fig = plt.figure(figsize=(13,4), dpi=150)
    plt.title(year_list[i])
    plt.ylim(0,ylimit*1.1)
    for j in range(len(year_month_list[i])):
        plt.bar(calendar.month_name[int(year_month_list[i][j][5:7])], float(duration_list[i][j]), color='red')
    plt.show()               