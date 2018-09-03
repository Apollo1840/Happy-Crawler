# -*- coding: utf-8 -*-

'''
basically there are two ways to create crawler:
    1) urllib.request :  from urllib import request
        .urlretrieve
        .urlopen
            str(file.read())
            json.loads(file.read())
    
    2) requests
        response = requests.get()
        
        response.content
        response.text

1. host

    1) request
    before using the request:
            
        opener = request.build_opener()
            opener.addheaders = [
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        request.install_opener(opener)
        
    2) requests
    when use the request.get()
        
        hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        response = requests.get(url,headers = hea)

2, beatifulsoup
    the response.text can be insert into beatifulsoup
        soup = BeautifulSoup(response.text, 'html5lib')
            



'''





from urllib import request 
import json
import os

# use request in urllib to download img and csv

def download_img(url):
    return request.urlretrieve(url, 'material/sample_img.jpg')

def download_csv(url):
    file = request.urlopen(url)
    content = str(file.read())  # file.read() returns bytes
    
    with open('material/sample.csv','w') as f:
        for line in content.split('\\n'):
            f.write(line + '\n')


def download_csv_dumps(url):
    # download a csv_file website and show the content
    file = request.urlopen(url)
    J = json.loads(file.read())  # json.loads can take bit information
    json.dumps(J, indent = 2)


def simple_show_case():
    # set up a opener for urllib.request, reason unknow
    opener = request.build_opener()
    opener.addheaders = [
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    request.install_opener(opener)
    
    # download img
    url = 'http://dreamstop.com/wp-content/uploads/2013/11/Internet-dream-meaning.jpg'
    download_img(url)
    
    url = 'https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2017-financial-year-provisional/Download-data/annual-enterprise-survey-2017-financial-year-provisional-csv.csv'
    download_csv(url)
    download_csv_dumps(url)


###############################################################################
import requests as req # more useful than urllib
from bs4 import BeautifulSoup

def show_case_by_requests():
    
    # download csv
    url = 'https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2017-financial-year-provisional/Download-data/annual-enterprise-survey-2017-financial-year-provisional-csv.csv'
    response = req.get(url)
    with open('sample.csv','wb') as f:
        content = response.content   # .content is content like csv or img
        f.write(content)  
    
    # download img
    url = 'http://dreamstop.com/wp-content/uploads/2013/11/Internet-dream-meaning.jpg'
    response = req.get(url)
    with open('material/sample.jpg','wb') as f:
        content = response.content   # .content is content like csv or img
        f.write(content) 
    
    # download html file
    url = 'https://www.baidu.com/'
    response = req.get(url)
    response.encoding = 'utf-8'
    with open('material/page.html','w', encoding='utf-8') as f:
        html = response.text
        f.write(html)                # .text is html format text
    
# use 'get' in requests to get the response(html) of the website
    
def download_page(url):
    # download the website as a html file
    response = req.get(url)
    response.encoding='utf-8'
    with open('material/page.txt','w', encoding="utf-8") as f:
        f.write(response.text)
    os.rename('material/page.txt','material/page.html')


##############################################################################

def show_case_of_bs():
    print('access the internet...')
    url = 'http://www.dnvod.tv/'
    response = req.get(url)
    response.text
    
    print('proceeding...')
    soup = BeautifulSoup(response.text, 'html5lib')

    for link in soup.find_all('a'):
        # link is a bs4 element : Tag
        print(link.string)
        print(link.get('href', None))  # be careful, this is not the complete version of url
        print('\n')




if __name__ == '__main__':


        
    
        
        
        
    
    