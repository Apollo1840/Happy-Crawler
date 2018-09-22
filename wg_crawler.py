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

# import numpy as np
import pandas as pd
import re
# import random

from basic_crawler import basic_crawler
from bs4 import BeautifulSoup
# from basic_crawler import proxy_formatter

import matplotlib.pyplot as plt
# import time


class wg_crawler():
    '''
      This is main class, it serves as the interface. 
      The functions are realised in different classes.
      
    '''
    
    df = None

    def run(self, start_page=1, end_page=10, path = 'material/'):
        # the default function, it will scrape some pages of the wg_gesucht and save the data in path
        
        self.ws = wg_spider()
        
        # get main page data (just readable)
        self.ws.get_surface_data(start_page, end_page)
        path0 = path + 'The_wg_information_in_munich_0_{}.csv'.format(end_page-start_page)
        self.ws.df.to_csv(path0, encoding='utf-8')
        
        # go to the links to get more data to readable level
        self.ws.get_details()
        path1 = path + 'The_wg_information_in_munich_1_{}.csv'.format(end_page-start_page)
        self.ws.df.to_csv(path1, encoding='utf-8')
        
        # preprocess the data for the further analysis
        wp = wg_preprocess(self.ws.df)
        self.ws.df = wp.run()
        path2 = path + 'The_wg_information_in_munich_2_{}.csv'.format(end_page-start_page)
        self.ws.df.to_csv(path2, encoding='utf-8')
        
        self.df = self.ws.df
        
            
    def plot_size_price(self, path=None):
        wa = wg_analysis(self.ws.df)
        wa.size_price(path)
    
    
    
    
class wg_spider():
    df = None
    proxy = None
    
    def get_surface_data(self, start_page=1, end_page=10, all_pages=False):
        '''
            it will update the  DataFrame which has three column: ID of the post, name of the room, link to this room
        '''
        self.df = pd.DataFrame([], columns=['title', 'link', 'room_size', 'price', 'situation'])
        titles = []
        links = []
        sizes = []
        prices = []
        situations = []
         
        self.num_pages = end_page - start_page    
        
        if all_pages:
            end_page = 100  # todo: get the data from we
            
        for i in range(start_page-1, end_page):
            print('on page {} ... '.format(i))
            
            url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.{}.html'.format(i)          
            bc = basic_crawler(url, proxy = self.proxy, safetime=(6,10))
            soup = bc.soup
            
            # print(bc.response.status_code)
            # print(bc.soup.prettify())
            
            posts = soup.find_all('div',class_='offer_list_item')
            
            for p in posts:
                title_block = p.find('h3', class_='truncate_title')
                titles.append(title_block.text.strip())
                links.append('https://www.wg-gesucht.de/' + title_block.a['href'])
                
                detail_block = p.find('div', class_= 'detail-size-price-wrapper').text
                size, price = wg_spider.detail_info2size_and_price(detail_block)
                sizes.append(size)
                prices.append(price)
                
                situation_block = p.find('span', class_='noprint')
                situations.append(situation_block['title'])
            
        self.df.title = titles
        self.df.link = links
        
        self.df.room_size = sizes
        self.df.room_size = self.df.room_size.astype('float')
        
        self.df.price = prices
        self.df.price = self.df.price.astype('float')
        
        self.df.situation = situations
        
    @staticmethod    
    def detail_info2size_and_price(detail_info):
        si = detail_info.split('|')
        size = str.split(str.strip(si[0]),' ')[0]
        price = str.split(str.strip(si[1]),' ')[0]
        return size, price

    
    def load_surface_data(self, path):
        self.df = pd.read_csv(path)
        
    
    def get_details(self):
        '''
            This is always been called after the get_surface_data, so we have df with 4 columns:
            name of the room, link to this room, size of the room and price of the room
            After this function been called, a new column will be added to the data frame - xxx
        '''
        cautions = []
        dates = []
        addresses = []
  
        for i in range(len(self.df.link)):
            
            url = self.df.link[i]
            bc = basic_crawler(url, proxy=self.proxy, safetime=(6,10))                
            soup = bc.soup
            
            if bc.response.status_code == 200 and soup is not None: 
                                          
                # get caution
                caution = wg_spider.get_caution_from_soup(soup)
                
                # get starttime
                date = wg_spider.get_date_from_soup(soup)
                
                # get address and zipcode
                address = wg_spider.get_addr_from_soup(soup)
                
            else:
                caution = None
                date = None
                address = None
            
            cautions.append(caution)
            dates.append(date)
            addresses.append(address)
            
            print('on entry {} ..'.format(i))
        
        self.df['caution'] = cautions
        self.df['date'] = dates
        self.df['address'] = addresses
    
    @staticmethod    
    def get_caution_from_soup(soup):
        table_caution = soup.find('table')
        if table_caution is None:
            return -1
                
        for row in table_caution.find_all('tr'):
            if str.strip(row.find_all('td')[0].text) == 'Kaution:':
                caution = str.strip(row.find_all('td')[1].text)
                caution = float(caution[:-1]) # exclude the euro sign
                return caution
            
        return -2
                
            
    @staticmethod    
    def get_date_from_soup(soup):
        div_date = soup.find('div', class_= 'col-sm-3')
        if div_date is None:
            return 'Error in page'
        return div_date.p.text
                
    
    
    @staticmethod
    def get_addr_from_soup(soup):
        div_address = soup.find('div', class_='mb10')
        if div_address == None:
            return 'Error in page'
        
        addressContent = div_address.find('a').text
    
        return addressContent
    
    
    def get_loc(self):
        pass
              

class wg_preprocess():
    
    def __init__(self, df):
        self.df = df
    
    def run(self):
        self.clean()
        self.get_addr_details()
        self.get_date_details()
        
        return self.df
    
    def save_data(self):
        self.df.to_csv('material/The_wg_information_in_munich_modified.csv', encoding='utf-8')
            
    def clean(self):
        df2 = self.df.dropna()
        df2 = df2.loc[df2.caution != -2, :]
        df2 = df2.loc[df2.caution != -1, :]
        df2 = df2.loc[df2.address != 'Error in page', :]
        df2 = df2.loc[df2.address != 'Not format', :]
        
        self.df = df2.drop_duplicates()
        
    
    def get_addr_details(self):
        self.df['street'] = self.df.address.apply(wg_preprocess.transform_addr, return_id=0)
        self.df['zipcode'] = self.df.address.apply(wg_preprocess.transform_addr, return_id=1)
        self.df['city'] = self.df.address.apply(wg_preprocess.transform_addr, return_id=2)
        self.df['area'] = self.df.address.apply(wg_preprocess.transform_addr, return_id=3)

        del self.df['address']
    
    
    @staticmethod
    def transform_addr(addressContent, return_id=0):
        street, zipcode, city, area = None, None, None, None
        
        # find PLZ
        blocks = [content.strip() for content in addressContent.split()]
        for content in blocks:
            if re.match('[0-9]{5}', content):
                zipcode = content
                break
        
        # find others
        addr_content = [row.strip() for row in addressContent.split('\n')]
        addr_content = list(filter(None, addr_content)) # normally it contains 2 rows
        if len(addr_content) >= 2:
            street = addr_content[0]
            
            second_part = addr_content[1].split(' ')
            if len(second_part)>=3:
                city = second_part[1]
                area = second_part[2]
            else:
                city = second_part[0]
        
        result = [street, zipcode, city, area]
        return result[return_id]
    
    def get_date_details(self):
        self.df['start_date'] = self.df.date.apply(wg_preprocess.transform_date, return_id=0)
        self.df['end_date'] = self.df.date.apply(wg_preprocess.transform_date, return_id=1)
        del self.df['date']
    
    @staticmethod
    def transform_date(dateContent, return_id=0):
        start_date, end_date = None, None
        
        pieces = wg_preprocess.information_to_pieces(dateContent, second_level=':')
    
        if pieces[0] == 'frei ab':
            start_date = pieces[1]
        if len(pieces) == 4 and pieces[2] == 'frei bis':
            end_date = pieces[3]
            
        result = [start_date, end_date]
        return result[return_id]
    
    @staticmethod
    def information_to_pieces(text, first_level='\n', second_level=' '):
        pieces = []
        for content in text.split(first_level):
            words = content.split(second_level)
            for word in words:
                word = word.strip() 
                if word:
                    pieces.append(word)
        return pieces
        

        
        
        
        
        
    def get_addr_details_2(self):
        def transform_addr(addressContent):
            addressContent = addressContent.split()
            
            # Check if the address information is complete
            # Maybe refator it to a check-function
            if len(addressContent) < 5:
                if len(addressContent[1]) < 5:
                    street = addressContent[0] + addressContent[1]
                    zipCode = addressContent[2]
                    city = addressContent[3]
                else:
                    street = addressContent[0]
                    zipCode = addressContent[1]
                    city = addressContent[2]
                    area = addressContent[3]
            else:
                street = addressContent[0] + addressContent[1]
                zipCode = addressContent[2]
                city = addressContent[3]
                area = addressContent[4]
            
            if re.match('[0-9]{5}', zipCode):
                pass
            else:
                zipCode = None
            
            return street + '|' + zipCode + '|' + city + '|' + area
        
        self.df['addressContent'] = self.df.address.apply(transform_addr)
        df_addr = pd.DataFrame([ac.split('|') for ac in self.df.addressContent], 
                                columns = ['street','zipcode','zipcode','area'])
        
        self.df = pd.concat([self.df, df_addr], axis = 0)
        
        del self.df.addressContent
        del self.df.address
    
    

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


def make_wg_gesucht_offline(start_page=1, end_page=10):
    
    for i in range(start_page-1, end_page):
        url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.{}.html'.format(i)          
        bc = basic_crawler(url, safetime=(6,10))
        bc.save_html('main_page_{}'.format(i))
       
        soup = bc.soup   
        posts = soup.find_all('div',class_='offer_list_item')
        os.mkdir('material/main_page_{}'.format(i))
        for j in range(len(posts)):
            title_block = posts[j].find('h3', class_='truncate_title')
            link = 'https://www.wg-gesucht.de/' + title_block.a['href']
            
            bc = basic_crawler(link, safetime=(6,10))            
            bc.save_html('main_page_{}/post_page{}'.format(i,j))
            
            print('on page {} for entry {}...\n'.format(i,j))


if __name__ == '__main__':
    
    pd.set_option('max_colwidth',200)
    pd.set_option('max_columns',None) 
    
    w_c = wg_crawler()
    # w_c.proxy = proxy_formatter('118.178.227.171','80')
    w_c.run(end_page=2)
    w_c.plot_size_price()
    
    
    
    
    
    
    