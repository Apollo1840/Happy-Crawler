# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 21:54:26 2018

@author: zouco
"""


# note: 也可以用中文，没必要用英语

'''
 zoucongyu: to developer:
     I suggest to use 
         bc=BasicCrawler(url), soup = bc.soup 
    instead of
        res = req.get(url), BeautifulSoup(res.text)
    to be more hard to detect

''' 

# import numpy as np
import pandas as pd
# import re
import os
# import random

from bc2 import BasicCrawler
# from BasicCrawler import proxy_formatter

# import matplotlib.pyplot as plt
import time

from bs4 import BeautifulSoup


from wg_crawler import WgSpider
from wg_crawler import WgPreprocess
# from wg_crawler import WgAnalysis

from math_tools import cut_range
import threading

class WgCrawler():
    '''
      This is main class, it serves as the interface. 
      The functions are realised in different classes.
      
    '''
    
    def run(self, start_page=1, end_page=10, num_processes=1, path = 'material/', data_exists=False):
        
        self.df = pd.DataFrame()
        
        tasks = cut_range(start_page, end_page+1, num_processes)
        # print(tasks)
        
        thread_list = []
        for task in tasks:
            if len(task) > 0:
                t = threading.Thread(target=self.mining, args=(list(task)[0], list(task)[-1], data_exists))
                thread_list.append(t)
                t.start()
                time.sleep(1)
        
        for t in thread_list:
            t.join()
        
        wp = WgPreprocess(self.df)
        self.df = wp.run()
        
        path = path + 'The_wg_information_in_munich_{}.csv'.format(end_page-start_page)
        self.df.to_csv(path, encoding='utf-8')
        
    def mining(self, start_page=1, end_page=10, data_exists=False):
        if not data_exists:
            make_wg_gesucht_offline(start_page=start_page, end_page=end_page)
        
        ws = WgSpider_local()
        ws.get_surface_data(start_page, end_page)
        ws.get_details()
        
        self.df = pd.concat([self.df, ws.df],axis=0)
    
    def run_simple(self, start_page=1, end_page=10, path = 'material/', data_exists=False, save_data=True):
        # the default function, it will scrape some pages of the wg_gesucht and save the data in path
        if not data_exists:
            make_wg_gesucht_offline(start_page=start_page, end_page=end_page)
        
        self.ws = WgSpider_local()
        
        # get main page data
        self.ws.get_surface_data(start_page, end_page)
        
        if save_data:
            path0 = path + 'The_wg_information_in_munich_0_{}.csv'.format(end_page-start_page)
            self.ws.df.to_csv(path0, encoding='utf-8')
        
        # go to the links to get more data to readable level
        self.ws.get_details()
        
        if save_data:
            path1 = path + 'The_wg_information_in_munich_1_{}.csv'.format(end_page-start_page)
            self.ws.df.to_csv(path1, encoding='utf-8')
        
        # preprocess the data for the further analysis
        wp = WgPreprocess(self.ws.df)
        self.ws.df = wp.run()
        
        if save_data:
            path2 = path + 'The_wg_information_in_munich_2_{}.csv'.format(end_page-start_page)
            self.ws.df.to_csv(path2, encoding='utf-8')
        
        self.df = self.ws.df
        
    
          
    
class WgSpider_local(WgSpider):
    df = None
    proxy = None
     
    def load_soup_main(self,i):
        soup = WgSpider_local.load_local_html_as_soup('material/main_page_{}.html'.format(i))
        return soup
        
    def load_soup_post(self,i):
        page = i//20
        post = i%20
        soup = WgSpider_local.load_local_html_as_soup('material/main_page_{}/post_page{}.html'.format(page,post))
        return soup
    
    @staticmethod
    def load_local_html_as_soup(path):
        with open(path, 'rb') as f:
            soup = BeautifulSoup(f,'html5lib')
        return soup



def make_wg_gesucht_offline(start_page=1, end_page=10, proxies='auto'):
    
        for i in range(start_page-1, end_page):
                  
            bc = BasicCrawler(proxies=proxies)
    
            url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.{}.html'.format(i)            
            bc.probe = lambda soup: WgSpider.probe_main_page(soup)
            soup = bc.get_soup(url)    
            bc.save_html('main_page_{}'.format(i))
                
             
            posts = soup.find_all('div',class_='offer_list_item')
            os.mkdir('material/main_page_{}'.format(i))
            for j in range(len(posts)):
                print('on page {} for entry {}...\n'.format(i,j))
                title_block = posts[j].find('h3', class_='truncate_title')
    
                url = 'https://www.wg-gesucht.de/' + title_block.a['href']
                bc.probe = lambda soup: WgSpider.probe_post_page(soup)
                bc.get_soup(url) # only get_soup has probe 
                bc.save_html('main_page_{}/post_page{}'.format(i,j))
                        
def test():
    '''
        here you can test your program.
    '''
    
    # make_wg_gesucht_offline(start_page=2, end_page=2)
    ws = WgSpider_local()
    ws.get_surface_data(end_page=2)
    ws.get_details()

    wp = WgPreprocess(ws.df)
    ws.df = wp.run()
    print(ws.df)

    wc = WgCrawler()
    wc.run(end_page=2, data_exists=True)
    print(wc.df)
    
    
    
    


if __name__ == '__main__':
    
    pd.set_option('max_colwidth',200)
    pd.set_option('max_columns',None) 
    
    t0 = time.time()
    
    wc = WgCrawler()
    wc.run_simple(end_page=12)
    print(wc.df)
    
    print('spend {}s'.format(time.time()-t0))
    

    
    
    
    