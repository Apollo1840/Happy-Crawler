# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 12:15:56 2018

@author: zouco
"""

# -*- coding: utf-8 -*-
'''
  todo:  add for loop， track the change of some specific words

'''




import jieba
import jieba.posseg
# "n"是名词，“a”是形容词，“v”是动词，“d”是副词，“x”是非语素词
# https://blog.csdn.net/suibianshen2012/article/details/53487157

import requests as req
from bs4 import BeautifulSoup
from basic_crawler import basic_crawler

import numpy as np
import pandas as pd
from pyecharts import WordCloud

import time

class rent_crawler(basic_crawler):
    
    
    def __init__(self):
        url = 'https://www.kaiyuan.info/forum-92-1.html'
        super(rent_crawler, self).__init__(url)
        self.temp_soup = None
        self.post_titles = []
        self.historical_post_titles = []
        self.post_heat = []
        self.words = [] # each item i, i[0] is word, i[1] is flag, i[2] is heat
        self.words_refine = []    

        self.list_of_drop_words = ['人', 
                                   '人物', 
                                   '大家', 
                                   '帖子', 
                                   '时候', 
                                   '鹅', 
                                   '鹅们', 
                                   '全国', 
                                   '图', 
                                   '料',
                                   '集',
                                   '楼']
    
    def get_posts(self, include_heat=False):
        '''
            this function will enumerate the post titles of temp_soup 
            and store it in self.post_titles with modification mode.
            if include_heat, it will also store the number of responses in self.post_heat.
        '''
        self.post_titles = []
        self.post_heat = []
        
        tbody = self.temp_soup.find('table', class_='olt')
        trs = tbody.find_all('tr')
               
        for tr in trs[1:]:
            title = tr.td.a['title']
            self.post_titles.append(title)
            if include_heat:
                heat = tr.find_all('td')[2].text  
                self.post_heat.append(heat)      
                         
    def get_words(self, include_heat=False, tags_off=False):
        
        self.get_posts(include_heat)
        
        if tags_off:
            # tags_off can get preciser result
            for p_title in self.post_titles:
                words_in_p_title = jieba.cut(p_title, cut_all=False, HMM=True)
                self.words_refine.extend(words_in_p_title)  
        else:   
            for i in range(len(self.post_titles)):
                if self.post_titles[i] not in self.historical_post_titles:
                    words_in_p_title = jieba.posseg.cut(self.post_titles[i], HMM=True)
                    for w in words_in_p_title:
                        if include_heat:
                            self.words.append([w.word, w.flag, self.post_heat[i]])
                        else:
                            self.words.append([w.word, w.flag, 1])
                            
        self.historical_post_titles.extend(self.post_titles)

    def get_words_list(self, num_pages=5, include_heat=True):
        self.historical_post_titles = []
        for id_page in range(num_pages):
            time.sleep(1)
            url = 'https://www.douban.com/group/blabla//discussion?start={}'.format(num_pages-id_page)
            c = basic_crawler(url)
            self.temp_soup = c.soup
            del c
            self.get_words(include_heat)
            print(id_page)
        # print(self.historical_post_titles)
                
        
    def create_words_table(self, num_pages=5, include_heat=True, adjustment=None): 
        # preprocess the raw data
        df_wl = pd.DataFrame(self.words) 
        df_wl.columns = ['words','flag','heat']
        df_wl.heat = df_wl.heat.astype('float')
        
        # df_wl.to_csv('raw_data.csv')
        
        if include_heat:
            if adjustment=='log':
                df_wl.heat = np.log(df_wl.heat)
        
        # df_wl.to_csv('raw_data2.csv')
        
        df_wlh = df_wl.groupby(['words','flag'])['heat'].agg([np.sum])
        df_wlh.reset_index(inplace=True)
        df_wlh.columns = ['words','flag','heat']
        # df_wlh.to_csv('raw_data3.csv')
        return df_wlh
        
   
    
    def run(self, num_pages=5, consider_tags=['n','nr','nrt'], include_heat=True, adjustment=None):  
        
        # "n"是名词，“a”是形容词，“v”是动词，“d”是副词，“x”是非语素词
        # https://blog.csdn.net/suibianshen2012/article/details/53487157
        
        self. get_words_list(num_pages, include_heat)
        df_wl = self.create_words_table(num_pages, include_heat, adjustment)
        df_part = df_wl.loc[df_wl.flag.isin(consider_tags),:]
        df_part = df_part.loc[~df_part.words.isin(self.list_of_drop_words),:]

        print(df_part.shape[0])
    
        graph_title = "The hot words in douban/blabla within {} pages at {}".format(num_pages, time.asctime( time.localtime(time.time())))
        wordcloud_2 = WordCloud(title=graph_title, title_pos='center', width=1600, height=800)
        wordcloud_2.add("", list(df_part.words), df_part.heat, word_size_range=[10, 50],
                  shape='diamond')
        
        wordcloud_2.render("material/Hot_words_cloud.html")
        






def test():
    '''
        this part of program is just playing ground of the programmer
    '''
    
    url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.0.html'
    res = req.get(url)
    soup = BeautifulSoup(res.text)
    titles = soup.find_all('a', class_='detailansicht')
    for t in titles:
        print(t['href'])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def is_post_title_related(title):
        if '慕尼黑' in title:
            if '求' in title or '寻租' in title:
                return False
            else:
                return True
        else:
            return False
    
    for i in range(10):
        url = 'https://www.kaiyuan.info/forum-92-{}.html'.format(i)
        soup=BeautifulSoup(req.get(url).text, 'lxml')
        # print(soup.prettify())
        post_titles = soup.find_all('a', class_='s xst')
        # print(post_titles)
        for pt in post_titles:
            if is_post_title_related(pt.text):
                print(pt.text)
                print(pt['href'])
                print('\n')
        
        
        url = pt.text
        url = 'https://www.kaiyuan.info/thread-1160790-1-1.html'
        bc = basic_crawler(url)
        soup = bc.soup
        soup.prettify()
        main_content = soup.find('td', class_='t_f').text
        print(main_content)
        
        # complex situation:
        # 1, picture
        # 2, table 
        
    trs = tbody.find_all('tr')
        
    for tr in trs[1:]:
            post_titles.append(tr.td.a['title'])
            post_heat.append(tr.find_all('td')[2].text)
    for i in range(len(post_titles)):
                words_in_p_title = jieba.posseg.cut(post_titles[i], HMM=True)
                for w in words_in_p_title:
                    words_h.append([w.word, w.flag, post_heat[i]])      
    
    df_wl = pd.DataFrame(words_h) 
    print(df_wl)
    df_wl.columns = ['words','flag','heat']
    df_wl.heat.astype('int',inplace=True)
    max(df_wl.heat)
    df_wl.loc[df_wl.heat==max(df_wl.heat),:]
    df_wlh = df_wl.groupby(['words','flag'])['heat'].agg([np.sum])
    print(df_wlh)
    df_wlh.reset_index(inplace=True)
    print(df_wlh)
    print(df_wlh.shape)
    df_wlh.columns = ['words','flag','heat']
    
    pd.set_option('display.max_rows', None)
    df=pd.read_csv('raw_data.csv')
    print(df.loc[df.flag.isin(['n','nr','nrt']),:].sort_values(['heat','words']))
    print(df.loc[df.flag.isin(['n','nr','nrt']),:].sort_values(['words']))
        
    

if __name__ == '__main__':
    
    dc = douban_crawler()
    dc.run(num_pages=10, adjustment='normal')






