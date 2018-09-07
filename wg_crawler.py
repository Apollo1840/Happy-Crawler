# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 21:54:26 2018

@author: zoucongyu
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



class wg_crawler():
    df = None
    
    def get_surface_data(self, num_pages):
        '''
            it will update the  DataFrame which has three column: ID of the post, name of the room, link to this room
        '''
        self.df = pd.DataFrame([], columns=['ID','name','link'])
        
        if num_pages=='auto':
            num_pages = 10  # todo: get the data from web
        
        for i in range(num_pages):
            url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.{}.html'.format(i)
            
            bc=basic_crawler(url)
            soup = bc.soup 
            titles = soup.find_all('a', class_='detailansicht') # todo: from now on, the code is wrong
            for t in titles: 
                self.df.ID.append(1)
                self.df.name.append('noname')
                self.df.link.append(t['href'])  # todo : this need to correctify, 因为链接重复了


    def get_preis(self):
        '''
            This is always been called after the get_surface_data, so we have df with 3 columns:
            ID of the post, name of the room, link to this room
            After this function been called, a new column will be added to the data frame - preis
        '''
        self.df['preis'] = None
        
        for url in self.df.link:
            bc = basic_crawler(url)
            soup = bc.soup
             
            # ... #
            
            self.df['preis'].append(100)
            
    def get_loc(self):
        pass
            

        
        
    
    
    def run(self, num_pages=10):
        
        self.get_surface_data(num_pages)
        self.get_preis()
        
        self.df.to_csv('The_wg_information_in_munich.csv')
        
        






def test():
    '''
        here you can test your program.
    '''
    
    # this part is for surface page
    df = pd.DataFrame([], columns=['ID','name','link'])
    url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.1.html'
    bc=basic_crawler(url)
    soup = bc.soup 
    titles = soup.find_all('a', class_='detailansicht') # todo: from now on, the code is wrong
    for t in titles: 
        df.link.append(t['href'])  # todo : this need to correctify, 因为链接重复了
   
    
    
    

    # this part is for detail page (the link in original dataframe)
    url = 'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen-Trudering.3278644.html'
    bc=basic_crawler(url)
    soup = bc.soup
    
        




if __name__ == '__main__':
    w_c = wg_crawler()
    w_c.run()
    
    