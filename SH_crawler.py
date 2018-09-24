# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 15:12:05 2018

@author: zouco
"""

from bc2 import BasicCrawler
import pandas as pd

import time

def refine_wiki_link(link):
    if link.startswith('https://de.wikipedia.org'):
        return link
    else:
        pieces = link.split('=')
        link = ''
        for piece in pieces[1:]:
            link += piece
        pieces = link.split('&')
        link = pieces[0]
        if link.startswith('https://de.wikipedia.org'):
            return link
        else:
            return 'https://www.google.com'
        

def get_umsatz_supplier(supplier_name):
        supplier = supplier_name.replace(' ','+') + '+wiki'
        print(supplier)
        
        bc = BasicCrawler(headers='auto')
        search_link = 'https://www.google.com/search?q={}'.format(supplier)
    
        print(search_link)
        
        soup = bc.get_soup(search_link)
        time.sleep(3)
        a = soup.find_all('h3', class_='r')[0]
        link = a.find('a')['href']
        	
        link = refine_wiki_link(link)
        print(link)
      
        soup = bc.get_soup(link)
        time.sleep(3)
        table = soup.select('#Vorlage_Infobox_Unternehmen')
        revenue = None
        if table:
            for row in table[0].find_all('tr'):
                try:
                    if str.strip(row.find('td').text) == 'Umsatz':
                        revenue = row.find_all('td')[1].text
                        print(supplier_name, revenue)
                except AttributeError:
                    pass
        
        return revenue 
    
    


if __name__ == '__main__':
    
    suppliers = ["Jabil", "Sanmina", "Thermo Fisher Diagnostics", "IVEK", "Randox Laboratories", "Inpeco", "Nypro", "Carclo", "Bio-Rad Laboratories"]
    
    revenues = []
    for supplier in suppliers:
        revenues.append(get_umsatz_supplier(supplier))
    
    result = pd.DataFrame()
    result['supplier']=suppliers
    result['revenue'] = revenues
    
    result.to_csv('SPIDER.csv')
        
        
        
        
        
    
    supplier = 'Sanmina+wiki'
    bc = BasicCrawler(headers='auto')
    search_link = 'https://www.google.com/search?q={}'.format(supplier)
    
    print(search_link)
    
    soup = bc.get_soup(search_link)
    time.sleep(3)
    a = soup.find_all('h3', class_='r')[0]
    link = a.find('a')['href']
    
    print(link)
      
    soup = bc.get_soup(link)
    time.sleep(3)
    print(soup)
    table = soup.select('#Vorlage_Infobox_Unternehmen')

    for row in table[0].find_all('tr'):
        try:
            if str.strip(row.find('td').text) == 'Umsatz':
                print(supplier,row.find_all('td')[1].text)
        except AttributeError:
            pass
    
                       
    
    #mw-content-text > div > table

import requests

def googleSearch(query):
    with requests.session() as c:
        url = 'https://www.google.co.in'
        query = {'q': query}
        urllink = requests.get(url, params=query)
        print(urllink.url)

googleSearch('Linkin Park')
soup = bc.get_soup('https://www.google.com/search?q=Bio-Rad+Park+wiki')
a = soup.find_all('h3', class_='r')

print(anchors)
anchors[0].text
print([t.find('a').text for t in a])
    