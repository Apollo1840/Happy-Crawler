# -*- coding: utf-8 -*-
'''
  todo:  add the name of pic, and for loop

'''




import jieba
import jieba.posseg
# "n"是名词，“a”是形容词，“v”是动词，“d”是副词，“x”是非语素词
# https://blog.csdn.net/suibianshen2012/article/details/53487157

import requests as req
from bs4 import BeautifulSoup

import numpy as np

import pandas as pd
from pyecharts import WordCloud

import time

hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
 
url = 'https://www.douban.com/group/blabla/'
urls = [url+'/discussion?start={}'.format(i) for i in range(20)]


words = []
words_s = []

info_page = 0
for url in urls:
    
    time.sleep(1)
    res = req.get(url, headers = hea)
    soup = BeautifulSoup(res.text, 'lxml')

    # print(soup.prettify())

    tbody = soup.find('table', class_='olt')
    trs = tbody.find_all('tr')

    for tr in trs[1:]:
        head = tr.td.a['title']
        word_in_head = jieba.cut(head, cut_all=False, HMM=True)
        words.extend(word_in_head)

    for tr in trs[1:]:
        head = tr.td.a['title']
        words_s.extend(jieba.posseg.cut(head,HMM=True))
    
    info_page +=1
    print(info_page)

print(len(words_s))
    
# pd.set_option('display.max_rows', None)

df_wl = pd.Series([i.word for i in words_s]).value_counts()
df_wl = pd.DataFrame(df_wl)
df_wl = df_wl.reset_index()
df_wl.columns = ['words','freq']

data = np.array([[i.word for i in words_s],[i.flag for i in words_s]])
df_match = pd.DataFrame(data.T)
df_match.columns = ['words','flag']
df_match = df_match.drop_duplicates()

df_wl = pd.merge(df_wl, df_match, on='words',how='left')
# rows increase because df_match is not unique

df_part = df_wl.loc[df_wl.flag.isin(['n','nr','nrt']),:]
names = list(df_part.words)
values = df_part.freq

wordcloud_2 = WordCloud(width=1600, height=800)
wordcloud_2.add("", names, values, word_size_range=[20, 50],
              shape='diamond')
    
wordcloud_2.render()






