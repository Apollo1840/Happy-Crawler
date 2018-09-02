# -*- coding: utf-8 -*-

import jieba

import requests as req
from bs4 import BeautifulSoup

url = 'https://www.douban.com/group/blabla/'

hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
 
res = req.get(url, headers = hea)
soup = BeautifulSoup(res.text, 'lxml')

print(soup.prettify())

tbody = soup.find('table', class_='olt')
trs = tbody.find_all('tr')

words = []
for tr in trs[1:]:
    head = tr.td.a['title']
    word_in_head = jieba.cut(head, cut_all=False, HMM=True)
    print(list(word_in_head))
    words.extend(jieba.cut(head, cut_all=False, HMM=True))
    
    
import pandas as pd
pd.set_option('display.max_rows', None)
df_wl = pd.Series(words).value_counts()
# df_wl = df_wl.sample(20)
  
from pyecharts import WordCloud

names = list(df_wl.index)
values = df_wl.values

wordcloud_2 = WordCloud()
wordcloud_2.add("", names, values, word_size_range=[20, 30],
              shape='diamond')
    
wordcloud_2.render()




