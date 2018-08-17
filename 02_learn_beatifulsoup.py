# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

with open('test.html') as f:
    soup = BeautifulSoup(f,'lxml')
  
print(soup.prettify())

print(soup.title)         # <title>dfa</title>
print(soup.title.text)    # dfa

article = soup.find('div', class_='footer')    
print(article.prettify())
article.h2.a.text

article.find('iframe', class_='youtube-player')['src']  # src is the attribute of tag
