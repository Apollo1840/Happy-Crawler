# -*- coding: utf-8 -*-
import requests as req
from bs4 import BeautifulSoup


# soups

with open('test.html') as f:
    soup = BeautifulSoup(f,'lxml')
    # xml, lxml, html5lib, html.parser

url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&ch=&tn=baidu&bar=&wd=dfa&rn=&oq=&rsv_pq=a7246c1300025490&rsv_t=092ex%2FruTBHT1VcUREMUMZ8qBJApW1bFLTvPb2lwYzLcoiHdCbaBm9i%2BBmM&rqlang=cn'
hea = hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
res = req.get(url, headers = hea)
soup2 = BeautifulSoup(res.text, 'lxml')
    

# how to use soup

# soup
print(soup.prettify())

print(soup.title)         # <title>dfa</title>
print(soup.title.text)    # dfa

article = soup.find('div', class_='footer')    
print(article.prettify())
article.h2.a.text

article.find('iframe', class_='youtube-player')['src']  # src is the attribute of tag


for article in soup.find_all('div', class_='footer'):
    print(article.h2.a.text)
    
    
# soup2
    
soup2.prettify()

a = soup2.select('div[class~=c-container] > h3 > a')
# article.select('rso > div > div > div:nth-child(3) > div > div > h3 > a')  # CSS selector
# CSS_selector = '#tabs > a:nth-child(2)'

print(a)    

a = soup2.select('div.c-container > h3 > a')
for i in a:
    print(i.text)            

