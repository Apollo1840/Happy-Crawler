# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 17:59:23 2018

@author: zoc
"""
import requests
from bs4 import BeautifulSoup

class basic_crawler():
    '''this class will be initialize with a url.
    by default it will use utf-8 as decoder.
    
    properties:
        html:  the html text of the url
        soup:  the soup created by BeautifulSoup method
    '''
    
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    
    def __init__(self, url="https://github.com/Apollo1840/Happy-Crawler", encoding = 'utf-8'):
        self.response = requests.get(url, headers=self.header)
    
    @property
    def html(self):
        return self.response.text
    
    @property
    def soup(self):
        return BeautifulSoup(self.html, 'lxml')
    
    def run(self):
        
        information = """
        This crawler does nothing. 
        You can use bc.html to get the html text of the website.
        You can use bc.soup to get the soup by BeautifulSoup method.
        """
        
        print(information)



if __name__ == '__main__':
    crawler = basic_crawler('https://www.bbc.com/news')
    print(crawler.html)