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

class douban_crawler(basic_crawler):
    
    
    def __init__(self):
        url = 'https://www.douban.com/group/blabla//discussion?start=0'
        super(douban_crawler, self).__init__(url)
        self.temp_soup = None
        self.post_titles = []
        self.post_heat = []
        self.words = []  # each item has .word and .flag
        self.words_refine = []
        self.words_h = [] # each item i, i[0] is word, i[1] is flag, i[2] is heat
        self.num_pages = 10
        self.consider_tags = ['n','nr','nrt']
        
        # "n"是名词，“a”是形容词，“v”是动词，“d”是副词，“x”是非语素词
        # https://blog.csdn.net/suibianshen2012/article/details/53487157
        
        self.list_of_drop_words = ['人']
    
    def get_post_titles(self):
        '''
            this function will enumerate the post titles of temp_soup 
            and store it in self.post_titles with modification mode.
        '''
        
        self.post_titles = []
        tbody = self.temp_soup.find('table', class_='olt')
        trs = tbody.find_all('tr')
        
        for tr in trs[1:]:
            self.post_titles.append(tr.td.a['title'])
    
    def get_post_heat(self):
        """
            this function will enumerate the number of response of temp_soup 
            and store it in self.post_heat with modification mode.
        """
        self.post_heat = []
        tbody = self.temp_soup.find('table', class_='olt')
        trs = tbody.find_all('tr')
        
        for tr in trs[1:]:
            heat = tr.find_all('td')[2].text  
            self.post_heat.append(heat)
               
    def get_words(self, tags_on=True):
        self.get_post_titles()
        if tags_on:
            for p_title in self.post_titles:
                words_in_p_title = jieba.posseg.cut(p_title, HMM=True)
                self.words.extend(words_in_p_title)
        else:
            for p_title in self.post_titles:
                words_in_p_title = jieba.cut(p_title, cut_all=False, HMM=True)
                self.words_refine.extend(words_in_p_title)
    
    
    def get_words_withHeat(self):
        self.get_post_titles()
        self.get_post_heat()
        for i in range(len(self.post_titles)):
                words_in_p_title = jieba.posseg.cut(self.post_titles[i], HMM=True)
                for w in words_in_p_title:
                    self.words_h.append([w.word, w.flag, self.post_heat[i]])
                
    def get_words_heat_list(self):
        
        # get the raw data
        for id_page in range(self.num_pages):
            time.sleep(1)
            url = 'https://www.douban.com/group/blabla//discussion?start={}'.format(id_page)
            c = basic_crawler(url)
            self.temp_soup = c.soup
            del c
            self.get_words_withHeat()
            print(id_page)
        
        # preprocess the raw data
        df_wl = pd.DataFrame(self.words_h) 
        df_wl.columns = ['words','flag','heat']
        df_wl.heat = df_wl.heat.astype('int')
        df_wlh = df_wl.groupby(['words','flag'])['heat'].agg([np.sum])
        df_wlh.reset_index(inplace=True)
        df_wlh.columns = ['words','flag','heat']
        return df_wlh
        
    def get_words_freq_list(self):
        
        # get the raw data
        for id_page in range(self.num_pages):
            time.sleep(1)
            url = 'https://www.douban.com/group/blabla//discussion?start={}'.format(id_page)
            c = basic_crawler(url)
            self.temp_soup = c.soup
            del c
            self.get_words()
            print(id_page)
        
        # preprocess the raw data
        df_wl = pd.Series([i.word for i in self.words]).value_counts()
        df_wl = pd.DataFrame(df_wl)
        df_wl = df_wl.reset_index()
        df_wl.columns = ['words','freq']
    
        data = np.array([[i.word for i in self.words],[i.flag for i in self.words]])
        df_match = pd.DataFrame(data.T)
        df_match.columns = ['words','flag']
        df_match = df_match.drop_duplicates()
        
        return pd.merge(df_wl, df_match, on='words',how='left')
    
    def run(self, num_pages=5, consider_tags=['n','nr','nrt']):  
        self.num_pages = num_pages
        self.consider_tags = consider_tags
        
        df_wl = self.get_words_heat_list()
        df_part = df_wl.loc[df_wl.flag.isin(self.consider_tags),:]
        df_part = df_part.loc[~df_part.words.isin(self.list_of_drop_words),:]
        
        print(df_part.shape[0])
    
        graph_title = "The hot words in douban/blabla within {} pages".format(self.num_pages)
        wordcloud_2 = WordCloud(title=graph_title, title_pos='center', width=1600, height=800)
        wordcloud_2.add("", list(df_part.words), df_part.heat, word_size_range=[20, 50],
                  shape='diamond')
        
        wordcloud_2.render("material/Hot_words_cloud.html")
        
        
    def run_word_freq(self, num_pages=5, consider_tags=['n','nr','nrt']):    
        self.num_pages = num_pages
        self.consider_tags = consider_tags
        
        df_wl = self.get_words_freq_list()
        df_part = df_wl.loc[df_wl.flag.isin(self.consider_tags),:]
        df_part = df_part.loc[~df_part.words.isin(self.list_of_drop_words),:]
        
        print(df_part.shape[0])
    
        graph_title = "The hot words in douban/blabla within {} pages".format(self.num_pages)
        wordcloud_2 = WordCloud(title=graph_title, title_pos='center', width=1600, height=800)
        wordcloud_2.add("", list(df_part.words), df_part.freq, word_size_range=[20, 50],
                  shape='diamond')
        
        wordcloud_2.render("material/Hot_words_cloud.html")



def test():
    '''
        this part of program is just playing ground of the programmer
    '''
    
    
    url = 'https://www.douban.com/group/blabla//discussion?start=0'
    soup=BeautifulSoup(req.get(url).text, 'lxml')
    
    post_titles = []
    post_heat = []
    words_h = []
    tbody = soup.find('table', class_='olt')
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

        
    

if __name__ == '__main__':
    
    dc = douban_crawler()
    dc.run(num_pages=20)






