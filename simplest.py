# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:25:33 2018

@author: zouco
"""

from urllib import request 
import json
import os

import requests as req # more useful than urllib
from bs4 import BeautifulSoup


def download_img(url):
    return request.urlretrieve(url, 'sample_img.jpg')

def download_csv(url):
    file = request.urlopen(url)
    content = str(file.read())  # file.read() returns bytes
    
    with open('sample.csv','w') as f:
        for line in content.split('\\n'):
            f.write(line + '\n')

def download_csv_as_json(url):
    # bulding
    file = request.urlopen(url)
    J = json.loads(file.read())
    json.dumps(J, indent = 2)
    
def download_page(url):
    source_code = req.get(url)
    source_code.encoding='utf-8'
    with open('page.txt','w', encoding="utf-8") as f:
        print(source_code.text)
        f.write(source_code.text)
    os.rename('page.txt','page.html')
        
    
def simple_show_case():
    # set up a opener for urllib.request, reason unknow
    opener = request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    request.install_opener(opener)
    
    # download img
    url = 'http://dreamstop.com/wp-content/uploads/2013/11/Internet-dream-meaning.jpg'
    download_img(url)
    
    url = 'https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2017-financial-year-provisional/Download-data/annual-enterprise-survey-2017-financial-year-provisional-csv.csv'
    download_csv(url)


def show_case_by_requests():
    url_1 = 'https://www.baidu.com/'
    url_2 = 'https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2017-financial-year-provisional/Download-data/annual-enterprise-survey-2017-financial-year-provisional-csv.csv'
    
    source_code_1 = req.get(url_1)
    source_code_2 = req.get(url_2)
    
    # if we want get item : file or img
    content = source_code_2.content    
    with open('sample.csv','wb') as f:
        f.write(content)
        
    # if we want html content
    html = source_code_1.text
    # but sometimes the encoding is not right
    source_code_1.encoding = 'utf-8'
    html = source_code_1.text
    with open('page.html','w', encoding='utf-8') as f:
        f.write(html)
    
    
def show_case_of_bs():
    print('access the internet...')
    url = 'http://www.dnvod.tv/'
    source_code = req.get(url)
    source_code.text
    
    print('proceeding...')
    soup = BeautifulSoup(source_code.text, 'html5lib')

    for link in soup.find_all('a'):
        # link is a bs4 element : Tag
        print(link.string)
        print(link.get('href'))  # be careful, this is not the complete version of url
        print('\n')




if __name__ == '__main__':


        
    
        
        
        
    
    