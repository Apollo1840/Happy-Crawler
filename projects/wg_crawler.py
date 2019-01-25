# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 21:54:26 2018

@author: zouco
"""


# note: 也可以用中文，没必要用英语
import pandas as pd

from bc3 import BasicCrawler
from bc3 import BasicCrawlerGroup


class wgc_ActionSet():
    
    @staticmethod
    def get_surface_data_df(soup):
        df = pd.DataFrame()
        columns = ["Name","link","room_size","price","situation","wanted"]
        if soup:
            posts = soup.find_all('div',class_='offer_list_item')    
            for p in posts:
                title_block = p.find('h3', class_='truncate_title')
                title = title_block.text.strip()
                
                link = 'https://www.wg-gesucht.de/' + title_block.a['href']
                
                detail_block = p.find('div', class_= 'detail-size-price-wrapper').text
                room_size, price = wgc_ActionSet.detail_info2size_and_price(detail_block)
                
                situation_block = p.find('span', class_='noprint')
                situation = situation_block['title']
                
                wanted_tags = p.find_all('img', class_='noprint')
                wanted_list = '|'
                for tag in wanted_tags:
                    wanted_list += '{}|'.format(tag['alt'])
                
                df = df.append(pd.Series([title, link, room_size, price, situation, wanted_list], index=columns), ignore_index=True)
        return df
    
    
    @staticmethod
    def get_detail_data(soup):
        detail_data = []
        detail_data.append(wgc_ActionSet.get_caution(soup))
        detail_data.append(wgc_ActionSet.get_date(soup))
        detail_data.append(wgc_ActionSet.get_addr(soup))
        return detail_data
        
    @staticmethod    
    def get_caution(soup):
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
    def get_date(soup):
        div_date = soup.find('div', class_= 'col-sm-3')
        if div_date is None:
            return 'Error in page'
        if div_date.p is None:
            return None
        return div_date.p.text
                
    
    
    @staticmethod
    def get_addr(soup):
        div_address = soup.find('div', class_='mb10')
        if div_address == None:
            return 'Error in page'
        
        addressContent = div_address.find('a').text
    
        return addressContent
            
        
    @staticmethod    
    def detail_info2size_and_price(detail_info):
        si = detail_info.split('|')
        size = str.split(str.strip(si[0]),' ')[0]
        price = str.split(str.strip(si[1]),' ')[0]
        return size, price
    

class WgCrawler(BasicCrawlerGroup, wgc_ActionSet):
    
    def work_on(self, startPage, endPage):
        
        urls = ['https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.{}.html'.format(i) for i in range(startPage-1,endPage)]
        
        # get basic(surface infomation on main pages)
        for bc in self.crawlers:
            bc.probe = WgCrawler.probe_main_page
        
        self.save_html(urls)
        df = self.get_df(urls, self.get_surface_data_df, func_type="df", is_local=True)
        df.to_csv("general_info({}-{}).csv".format(startPage, endPage))
        
        # -----------------------------------------------
        # get detailed infomation is post page
        for bc in self.crawlers:
            bc.probe = WgCrawler.probe_post_page
            
        self.save_html(df.link)
         
        df_detail = self.get_df(df.link, self.get_detail_data, is_local=True)
        df_detail.columns = ["caution","date","address"]
         
        result = pd.concat([df, df_detail],axis=1)
        result.to_csv("final_result({}-{}).csv".format(startPage, endPage))
        return result
     
    @staticmethod
    def probe_main_page(soup):
       posts = soup.find_all('div',class_='offer_list_item')
       boolean = (len(posts) >= 10)
       if not boolean:
           print('wrong main page')
       return boolean
   
    @staticmethod
    def probe_post_page(soup):
        div_address = soup.find('div', class_='mb10')
        boolean = (div_address is not None)
        if not boolean:
           print('wrong post page')
        return boolean


if __name__ == "__main__":
    wc = WgCrawler(safetime=(3,5))
    wc.work_on(1,5)
    