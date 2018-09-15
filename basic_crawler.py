# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 17:59:23 2018

@author: zoc
"""
import requests
from bs4 import BeautifulSoup
import os

class basic_crawler():
    '''this class will be initialize with a url.
    by default it will use utf-8 as decoder.
    
    properties:
        html:  the html text of the url
        soup:  the soup created by BeautifulSoup method
    '''
    
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    
    def __init__(self, url="https://github.com/Apollo1840/Happy-Crawler", encoding = 'utf-8'):
        self.header.update({'Cookie': 'CONSENT=YES+DE.zh-CN+20150622-23-0; SID=MwabsTJap4dJzHdpuYOc02TzBkKBjjelecrndTt_hhEPzX6F7tewHfHaq4nJFX5p2utH_w.; HSID=Ap95wmGZUi177CUc0; SSID=AuGJxTLYmRC-YSynz; APISID=AAZzlITj2128PgAk/AcfoYBSPS6BQADcmH; SAPISID=fxXfvRw4UhigXqK6/A3CxnInG7OubMCR8z; OGPC=845686784-30:19006818-1:19006913-1:19006965-1:19007018-1:19007384-1:; NID=139=jvv3YIJzKzzfBrodg-S71ZkJzpNVMj1Xq5aSE1XD-nhcpxeOMKLXsLqSKuWfsh4Sf_BDI0e_IvdLx7Bi7VFlj8GKmcv_2VgjsL18lF3YBxj2UEMuRrCI3qFRtn4xoUfGIQ5bAqsgpseTkv9JgbyYDO_fWfrDyaqU3tucOwjmBxIEoNKT8ks6CdhHx_piix77XvawHLx04OWZaaRW5FknN3lkl4g8mJ2ZvtnNzEYA59YzxJY-oBD84Ly1RQf5Dx3A7khxX7h4KVJ6KRkm2GwJLmCQpBlP5PpPb4_-cUNjuQETK5IxDXy1o-GKV1yFz0NDGKbdIuyRHO_ptT6X6KAG7QuVJ8DOp0yJ9WhrKSLZKhwI853qwuireSKk1kn_rRYcAYyHKeHh4nhaI4sJAl4CpDIv_TCJF5lvjXn37fQh; 1P_JAR=2018-9-15-8'})
        self.response = requests.get(url, headers=self.header)
    
    @property
    def html(self):
        return self.response.text
    
    @property
    def soup(self):
        return BeautifulSoup(self.html, 'lxml')
    
    def save_html(self, name='Page'):
        self.response.encoding='utf-8'
        with open('material/page.txt','w', encoding="utf-8") as f:
            f.write(self.response.text)
        os.rename('material/page.txt','material/{}.html'.format(name))
    
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