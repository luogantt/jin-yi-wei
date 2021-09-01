# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Tue Aug 31 14:38:36 2021

# @author: ledi
# """




import time
import parsel
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import requests
from lxml import etree
import datetime

from bs4 import BeautifulSoup
import pandas as pd

url = 'https://accounts.douban.com/passport/login?source=group'

browser = webdriver.Chrome()

wait = WebDriverWait(browser, 50)

browser.get(url)

time.sleep(30)

import time

data=[]
for pa in range(10000):
    
    kkt=25*pa
    url='https://www.douban.com/group/707669/discussion?start='+str(kkt)
    # url = 'https://www.douban.com/group/707669/'
    
    browser.get(url)
    
    page = browser.page_source
    
    print(page)
    
    soup = BeautifulSoup(page, "lxml")
    
    # soup = BeautifulSoup(html, "lxml")
    # 查找所有class属性为hd的div标签下的a标签的第一个span标签
    # soup = BeautifulSoup(html, "lxml")
    # 查找所有class属性为hd的div标签
    div_list = soup.find_all('td', class_='title')
    
    
    
    # import time
    # data=[]
    
    dd=pd.read_html(page)[1].values
    time.sleep(3)
    for k in range(len(div_list)):
        print(div_list[k])
        c=str(div_list[k].a).split()
        
        print(c)
        print(len(c))
        print('############')
        c1=c[2].split('=')
        c2=c1[1].split('"')
        
        temp=[c2[1],c[-2],dd[:,2][k]]
        
        
        # temp_html= requests.get(temp[0], headers=headers).text
        
        
        try:
            browser.get(temp[0])
            temp_html = browser.page_source
            
            soup = BeautifulSoup(temp_html, "lxml")
    
            coment_list = soup.find_all('p', class_='reply-content')
            coment_list=[k.contents for k in coment_list]
            et_html = etree.HTML(temp_html)
            # # 查找所有class属性为hd的div标签下的a标签的第一个span标签
            
        
            post_time= et_html.xpath("""//*[@id="topic-content"]/div[2]/h3/span[2]""")
            this_time=[each.text.strip() for each in   post_time]
                                 
    
            
            
            
            kkp=temp+this_time+coment_list
            data.append(kkp)
            print(kkp)
            
            
    
            time.sleep(0.1)
        except :
            pass
        
        
# import numpy as np      
# w2=np.array(data)

w2=data
m=len(w2)

title_words=[]
import jieba

import re
simple_punctuation = '[’!"#$%&\'()*+,-/:;<=>?@[\\]^_`{|}~，《。》｜,\n]'

# cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")

cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]") # 匹配不是中文


stop_list=[]
with open('./stop_words.txt', "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  #去掉列表中每一个元素的换行符
        stop_list.append(line)


for k in range(m):
    
    temp=w2[k][4:]
    
    
    for j in temp:
        
        
        
        if len(j)>0:
            
            for m in j:
                this_title=cop.sub( '',str(m))
        
                title_cut=jieba.cut( this_title,cut_all=True)
                title_cut1=[ k for k  in list(title_cut)  if k not in stop_list]
                title_words.append(title_cut1)

ttp=[]

for k in title_words:
    ttp.extend(k)
    
from collections import Counter

word_counts=dict(Counter(ttp))


import jieba  #分词
from wordcloud import WordCloud  #词云
from PIL import Image   #图片处理
import numpy as np  #将图片变成数组
import collections  #计数器
from matplotlib import pyplot as plt  #绘图
import sqlite3  #数据库

import jieba
import wordcloud
# 构建并配置词云对象w
w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='msyh.ttf')

# 调用jieba的lcut()方法对原始文本进行中文分词，得到string
# txt = '同济大学（Tongji University），简称“同济”，是中华人民共和国教育部直属，由教育部、国家海洋局和上海市共建的全国重点大学，历史悠久、声誉卓著，是国家“双一流”、“211工程”、“985工程”重点建设高校，也是收生标准最严格的中国大学之一'
# txtlist = jieba.lcut(txt)
string = " ".join(ttp)

# 将string变量传入w的generate()方法，给词云输入文字
w.generate(string)

# 将词云图片导出到当前文件夹
w.to_file('data92.png')



tdata=[]


for k in data:
    tdata.append([k[:4],k[4:]])

tdata1=pd.DataFrame(tdata)

tdata1.to_excel('tdata92.xlsx')


word_counts1=pd.Series(word_counts)

word_counts1=word_counts1.sort_values(ascending=False)

word_counts2=pd.DataFrame()
word_counts2['words']=word_counts1.index
word_counts2['count']=word_counts1.values

word_counts2.to_excel('word_counts2.xlsx')

############################################################







