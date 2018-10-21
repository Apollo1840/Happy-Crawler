# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from basic_crawler import BasicCrawler

class bbcCrawler(BasicCrawler):
    ''' this class is just a branch of methods.
    '''
    
    def __init__(self):
        super(bbcCrawler, self).__init__('https://www.bbc.com/news')
    
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
    
    crawler = bbcCrawler()
    print(crawler.html)
    crawler.header_link('outputs/news.txt')
    
    
        