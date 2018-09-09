# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 21:54:26 2018

@author: zouco
"""


# note: 也可以用中文，没必要用英语

'''
 zoucongyu: to developer:
     I suggest to use 
         bc=basic_crawler(url), soup = bc.soup 
    instead of
        res = req.get(url), BeautifulSoup(res.text)
    to be more hard to detect

''' 


import pandas as pd
from basic_crawler import basic_crawler

import matplotlib.pyplot as plt
import time


class wg_crawler():
    df = None
    
    def get_surface_data(self, num_pages):
        '''
            it will update the  DataFrame which has three column: ID of the post, name of the room, link to this room
        '''
        self.df = pd.DataFrame([], columns=['title', 'link', 'room_size', 'price'])
        titles = []
        links = []
        sizes = []
        prices = []
        
        if num_pages=='auto':
            num_pages = 10  # todo: get the data from web
        
        for i in range(num_pages):
            
            url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.{}.html'.format(i)
            
            bc=basic_crawler(url)
            soup = bc.soup   
            posts = soup.find_all('div',class_='offer_list_item')
            
            for p in posts:
                title = p.find('h3', class_='truncate_title')
                titles.append(title.text.strip())
                links.append(title.a['href'])
                
                detail = p.find('div', class_= 'detail-size-price-wrapper').text
                size, price = wg_crawler.detail_info2size_and_price(detail)
                sizes.append(size)
                prices.append(price)
            
            print('on page {} ... '.format(i))
            time.sleep(8) # this is to avoid being catch
            
        self.df.title = titles
        self.df.link = links
        self.df.room_size = sizes
        self.df.room_size = self.df.room_size.astype('float')
        self.df.price = prices
        self.df.price = self.df.price.astype('float')
        
    @staticmethod    
    def detail_info2size_and_price(detail_info):
        si = detail_info.split('|')
        size = str.split(str.strip(si[0]),' ')[0]
        price = str.split(str.strip(si[1]),' ')[0]
        return size, price
    
    # to do 
    def get_xxx(self):
        '''
            This is always been called after the get_surface_data, so we have df with 4 columns:
            name of the room, link to this room, size of the room and price of the room
            After this function been called, a new column will be added to the data frame - xxx
        '''
        xxx = []
        
        for url in self.df.link:
            time.sleep(1)
            bc = basic_crawler(url)
            soup = bc.soup
             
            # ... #
            
            xxx.append(100)
            
        self.df['xxx'] = xxx
            
    def get_loc(self):
        pass
            

    
    
    def run(self, num_pages=10):
        
        self.get_surface_data(num_pages)
        # self.get_preis()
        
        self.df.to_csv('material/The_wg_information_in_munich.csv', encoding='utf-8')
        
        

class wg_analyse():
    df = None
    
    def __init__(self, wg_crawler):
        self.df = wg_crawler.df
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
    bc=basic_crawler(url)
    soup = bc.soup
    
    
    titles = []
    links = []
    sizes = []
    prices = []
    posts = soup.find_all('div',class_='offer_list_item')
    for p in posts:
        title = p.find('h3', class_='truncate_title')
        titles.append(title.text.strip())
        links.append(title.a['href'])
        
        detail = p.find('div', class_= 'detail-size-price-wrapper').text
        size, price = detail_info2size_and_price(detail)
        sizes.append(size)
        prices.append(price)
   
    
    # this part is for detail page (the link in original dataframe)
    url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen-Trudering.3278644.html'
    bc=basic_crawler(url)
    soup = bc.soup
    
        




if __name__ == '__main__':
    w_c = wg_crawler()
    w_c.run(num_pages=2)
    w_a = wg_analyse(w_c)
    w_a.size_price()
    
    