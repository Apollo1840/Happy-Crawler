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

import numpy as np
import pandas as pd
import re
import random

from basic_crawler import BasicCrawler
from basic_crawler import proxy_formatter

from wg_crawler import WgSpider
from wg_crawler import WgPreprocess

import matplotlib.pyplot as plt
import time

from bs4 import BeautifulSoup

class wg_crawler():
    '''
      This is main class, it serves as the interface. 
      The functions are realised in different classes.
      
    '''
    
    def run(self, start_page=1, end_page=10, path = 'material/'):
        # the default function, it will scrape some pages of the wg_gesucht and save the data in path
        
        self.ws = wg_spider()
        
        # get main page data
        self.ws.get_surface_data(start_page, end_page)
        path0 = path + 'The_wg_information_in_munich_0_{}.csv'.format(end_page-start_page)
        self.ws.df.to_csv(path0, encoding='utf-8')
        
        # go to the links to get more data to readable level
        self.ws.get_details()
        path1 = path + 'The_wg_information_in_munich_1_{}.csv'.format(end_page-start_page)
        self.ws.df.to_csv(path1, encoding='utf-8')
        
        # preprocess the data for the further analysis
        wp = wg_preprocess()
        self.ws.df = wp.run(self.ws.df)
        path2 = path + 'The_wg_information_in_munich_2_{}.csv'.format(end_page-start_page)
        self.ws.df.to_csv(path2, encoding='utf-8')
        
            
    def plot_size_price(self, path=None):
        wa = wg_analysis(self.ws.df)
        wa.size_price(path)
 
    
class wg_analysis():
    df = None
    
    def __init__(self, df):
        self.df = df
        plt.style.use('ggplot')
    
    def size_price(self, path = None):
        plt.plot(self.df.room_size, self.df.price, 'o')
        
        plt.xlabel('Room size (m²)')
        plt.ylabel('Price (euro)')
        title = 'Relationship between room size and price'
        plt.title(title)
        if path:
            plt.savefig(path)
        else:
            plt.savefig('material/{}.jpg'.format(title))
        
        plt.show()




def test():
    '''
        here you can test your program.
    '''
    
    'panel panel-default  list-details-ad-border offer_list_item'
    
    # this part is for surface page
    def detail_info2size_and_price(detail_info):
        si = detail_info.split('|')
        size = str.split(str.strip(si[0]),' ')[0]
        price = str.split(str.strip(si[1]),' ')[0]
        return size, price
    
    
    df = pd.DataFrame([], columns=['name','link'])
    url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.1.html'
    bc=BasicCrawler(url)
    soup = bc.soup
    
    
    titles = []
    links = []
    sizes = []
    prices = []
    posts = soup.find_all('div',class_='offer_list_item')
    for p in posts:
        people = p.find('span', class_='noprint')
        print(people['title'])
        
        title = p.find('h3', class_='truncate_title')
        titles.append(title.text.strip())
        links.append(title.a['href'])
        
        detail = p.find('div', class_= 'detail-size-price-wrapper').text
        size, price = detail_info2size_and_price(detail)
        sizes.append(size)
        prices.append(price)
   
    
    # this part is for detail page (the link in original dataframe)
    url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen-Trudering.3278644.html'
    url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen-Schwabing-West.6873455.html'
    bc=BasicCrawler(url)
    soup = bc.soup
    
    address = soup.select('div.col-sm-4.mb10 > a')
    print(address)
    
    strs = str.split(soup.find('div', class_= 'col-sm-3').p.text, ':')
    if str.strip(strs[0])=='frei ab':
        strs2 = str.split(str.strip(strs[1]), '\n')
        starttime = str.strip(strs2[0])
        print(starttime)

    
    
    table = soup.find('table')
    table
    for row in table.find_all('tr'):
        if str.strip(row.find_all('td')[0].text) == 'Kaution:':
            caution = str.strip(row.find_all('td')[1].text)
            caution = float(caution[:-1])
            print(caution)
            
    
    
    
#    table > tbody > tr:nth-child(4) > td:nth-child(1)'
    
    w_c.df       
    w_c.df.columns
    
    w_c.df.groupby('zipcode').price.mean()
    w_c.df.caution.value_counts()
    w_c.df.zipcode.value_counts()
    
    df2 = w_c.df.loc[w_c.df.caution != -2, :]
    
    
    df2.caution.value_counts()



def information_to_pieces(text, first_level='\n', second_level=' '):
    pieces = []
    for content in text.split(first_level):
        words = content.split(second_level)
        for word in words:
            word = word.strip() 
            if word:
                pieces.append(word)
    return pieces
 

def test_on_post_page_locally():
    from wg_crawler_local import wg_spider_local
    
    page = 0
    post = 4
    
    soup = wg_spider_local.load_local_html_as_soup('material/main_page_{}/post_page{}.html'.format(page,post))

    div_date = soup.find('div', class_= 'col-sm-3')
    if div_date is None:
        print('Error in page')
    
    pieces = information_to_pieces(div_date.p.text, second_level=':')
    
    
    if pieces[0] == 'frei ab':
        start_date = pieces[1]
    if len(pieces) == 4 and pieces[2] == 'frei bis':
        end_date = pieces[3]
        
    
        def get_date_details(self):
        start_dates = []
        end_dates = []
        
        dateList = list(self.df.date)
        for i in range(self.df.shape[0]):
            dateContent = dateList[i]
            start_date, end_date = wg_preprocess.transform_date(dateContent)
            start_dates.append(start_date)
            end_dates.append(end_date)
        
        self.df['start_date'] = start_dates
        self.df['end_date'] = end_dates
        
        del self.df['date']
        
        
    
    print(pieces)
    if str.strip(strs[0])=='frei ab':
        strs2 = str.split(str.strip(strs[1]), '\n')
        starttime = str.strip(strs2[0])
        print(starttime)
    


        


if __name__ == '__main__':
    
    pd.set_option('max_colwidth',200)
    pd.set_option('max_columns',None) 
    
    w_c = wg_crawler()
    # w_c.proxy = proxy_formatter('118.178.227.171','80')
    w_c.run(end_page=2)
    print(w_c.df)
    
    # w_c.load_surface_data('material/The_wg_information_in_munich_modified.csv')
    # w_c.get_details()
    # w_c.save_data()
  
    # w_a = wg_analyse(w_c)
    # w_a.size_price()
    
    
    
    
    
    
    