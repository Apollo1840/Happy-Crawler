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

import numpy as np
import pandas as pd
import re
from basic_crawler import basic_crawler
from basic_crawler import proxy_formatter

import matplotlib.pyplot as plt
import time


class wg_crawler():
    df = None
    proxy = None
    
    def get_surface_data(self, start_page=0, end_page=10, all_pages=False):
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
            
        for i in range(start_page, end_page+1):
            
            url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.{}.html'.format(i)
            
            bc = basic_crawler(url, proxy = self.proxy)
            soup = bc.soup   
            # print(bc.response.status_code)
            # print(bc.soup.prettify())
            
            posts = soup.find_all('div',class_='offer_list_item')
            
            for p in posts:
                title_block = p.find('h3', class_='truncate_title')
                titles.append(title_block.text.strip())
                links.append('https://www.wg-gesucht.de/' + title_block.a['href'])
                
                detail_block = p.find('div', class_= 'detail-size-price-wrapper').text
                size, price = wg_crawler.detail_info2size_and_price(detail_block)
                sizes.append(size)
                prices.append(price)
                
                situation_block = p.find('span', class_='noprint')
                situations.append(situation_block['title'])
            
            print('on page {} ... '.format(i))
            time.sleep(8) # this is to avoid being catch 
            
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
        
    
    def save_data(self):
        self.df.to_csv('material/The_wg_information_in_munich_modified.csv', encoding='utf-8')
    
    # to do 
    def get_details(self):
        '''
            This is always been called after the get_surface_data, so we have df with 4 columns:
            name of the room, link to this room, size of the room and price of the room
            After this function been called, a new column will be added to the data frame - xxx
        '''
        cautions = []
        startdates = []
        addresses = []
        zipcodes = []   
        i = 0
        for url in self.df.link:
            
            bc = basic_crawler(url, proxy=self.proxy)                
            soup = bc.soup
            
            if bc.response.status_code == 200 and soup is not None: 
                                          
                # get caution
                caution = wg_crawler.get_caution_from_soup(soup)
                
                # get starttime
                startdate = wg_crawler.get_startdate_from_soup(soup)
                
                # get address and zipcode
                address, zipcode = wg_crawler.get_addr_zip_from_soup(soup)
                
                time.sleep(5)
                
            else:
                caution = None
                startdate = None
                address = None
                zipcode = None
            
            cautions.append(caution)
            startdates.append(startdate)
            addresses.append(address)
            zipcodes.append(zipcode)
            
            i = i + 1
            print('on entry {} ..'.format(i))
        
        self.df['caution'] = cautions
        self.df['startdate'] = startdates
        self.df['address'] = addresses
        self.df['zipcode'] = zipcodes
    
    @staticmethod    
    def get_caution_from_soup(soup):
        table = soup.find('table')
        if table is None:
            return -1
                
        for row in table.find_all('tr'):
            if str.strip(row.find_all('td')[0].text) == 'Kaution:':
                caution = str.strip(row.find_all('td')[1].text)
                caution = float(caution[:-1])
                return caution
            
        return -2
                
            
    @staticmethod    
    def get_startdate_from_soup(soup):
        strs = str.split(soup.find('div', class_= 'col-sm-3').p.text, ':')
        if strs is None:
            return 'Error in page'
        
        if str.strip(strs[0])=='frei ab':
            strs2 = str.split(str.strip(strs[1]), '\n')
            starttime = str.strip(strs2[0])
            return starttime
        else:
            return 'Not format'
                
    
    
    @staticmethod
    def get_addr_zip_from_soup(soup):
        
        addressDiv = soup.find('div', class_='mb10')
        addressContent = addressDiv.find('a').text.split()
            
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
            zipcode = zipCode
        else:
            zipcode = None
        
        newAddress = street + '|' + city + '|' + area
        
        return newAddress, zipcode 
    
    
    def get_loc(self):
        pass
            
    
    
    
    
    def run(self, start_page=0, end_page=10):
        
        self.get_surface_data(start_page, end_page)
        self.get_details()
        self.df.to_csv('material/The_wg_information_in_munich_{}.csv'.format(self.num_pages), encoding='utf-8')
        
        

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
    bc=basic_crawler(url)
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

        


if __name__ == '__main__':
    
    w_c = wg_crawler()
    w_c.proxy = proxy_formatter('118.178.227.171','80')
    w_c.run(end_page=2)
    print(w_c.df)
    
    # w_c.load_surface_data('material/The_wg_information_in_munich_modified.csv')
    # w_c.get_details()
    # w_c.save_data()
    
    def abc(a, *numbers, **args):
        print(a)
        print(len(numbers))
    
    
    
    # w_a = wg_analyse(w_c)
    # w_a.size_price()
    
    
    
    
    
    
    