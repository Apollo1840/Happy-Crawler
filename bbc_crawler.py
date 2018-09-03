# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

class Crawler001():
    '''this class will be initialize with a url.
    by default it will use utf-8 as decoder.
    
    properties:
        html:  the html text of the url
        soup:  the soup created by BeautifulSoup method
    '''
    
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    
    def __init__(self, url, encoding = 'utf-8'):
        self.response = requests.get(url, headers=self.header)
    
    @property
    def html(self):
        return self.response.text
    
    @property
    def soup(self):
        return BeautifulSoup(self.html, 'lxml')

class Crawler_bbc(Crawler001):
    ''' this class is just a branch of methods.
    '''
    
    def __init__(self):
        super(Crawler_bbc, self).__init__('https://www.bbc.com/news')
    
    def header_link(self, file_path):
        # this method will write headers and their links into the file_path you defined, like: 'material/news.txt'
        # eg:
        #   Low-carb diets 'could shorten life'
        #   https://www.bbc.com/news/health-45195474
        
        with open(file_path, 'w') as f:
            for a in self.soup.find_all('a'):
                try:
                    f.write(a.h3.text)
                    f.write('\n')
                    f.write(site_fullname(a['href'],'https://www.bbc.com'))
                    f.write('\n')
                    f.write('\n')
                except Exception:
                    pass
        


def site_fullname(href, head):
    if href.startswith('http'):
        return href
    else:
        return head + href

if __name__ == '__main__':
    
    # crawler = Crawler001('https://www.bbc.com/news')
    # print(crawler.html)
    
    crawler = Crawler_bbc()
    crawler.header_link('material/news.txt')
    
    
        