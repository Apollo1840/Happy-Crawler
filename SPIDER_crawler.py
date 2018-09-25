# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 15:12:05 2018

@author: zouco
"""

from bc2 import BasicCrawler
import pandas as pd

import time

import re


class RevenueCrawler():
    
    def run(self, supplier_name):
        supplier = supplier_name.replace(' ','+') + '+wiki'
        print(supplier)
        
        bc = BasicCrawler(headers='auto')
        search_link = 'https://www.google.com/search?q={}'.format(supplier)
    
        print(search_link)
        
        soup = bc.get_soup(search_link)
        time.sleep(3)
        a = soup.find_all('h3', class_='r')[0]
        link = a.find('a')['href']
        	
        link = self.refine_wiki_link(link)
        print(link)
        if link == 'special companies':
            return self.get_revenue_for_sp(supplier_name)
      
        soup = bc.get_soup(link)
        time.sleep(3)
        
        revenue = None
        if link.startswith('https://de.wikipedia.org'):
            revenue = self.get_revenue_in_soup_de(soup)
        elif link.startswith('https://en.wikipedia.org'):
            revenue = self.get_revenue_in_soup_en(soup)
        else:
            print(link)
        
        return str.strip(revenue)
        
    def get_revenue_for_sp(self, supplier_name):
        return None
        
    

    def get_revenue_in_soup_de(self, soup):
        table = soup.select('#Vorlage_Infobox_Unternehmen')
        revenue = None
        if table:
            for row in table[0].find_all('tr'):
                try:
                    if str.strip(row.find('td').text) == 'Umsatz':
                        revenue = row.find_all('td')[1].text
                        print(revenue)
                except AttributeError:
                        pass
        return revenue 

    def get_revenue_in_soup_en(self, soup):
        table = soup.select('#mw-content-text > div > table.infobox.vcard')[0]
        revenue = None
        if table:
            for row in table.find_all('tr'):
                try:
                    if str.strip(row.find('th').text) == 'Revenue':
                        revenue = row.find('td').text
                        print(revenue)
                except AttributeError:
                        pass
        return revenue 

    def refine_wiki_link(self, link):
        if link.startswith('https://de.wikipedia.org') or link.startswith('https://en.wikipedia.org'):
            return link
        else:
            pieces = link.split('=')
            link = ''
            for piece in pieces[1:]:
                link += piece
            pieces = link.split('&')
            link = pieces[0]
            if link.startswith('https://de.wikipedia.org') or link.startswith('https://en.wikipedia.org'):
                return link
            else:
                print('\n{}\n!!! no wikipedia !!!\n'.format(link))
                return 'special companies'    
    
class ProductsCrawler():
    
    def run():
        pass



'''
def get_thomasnet_supplier_links(supplier_names=[]):

    sns = dict()
    
    bc = BasicCrawler()
    for sn in supplier_names:
        res = bc.get_soup(url="https://www.thomasnet.com/search.html?WTZO=Find+Suppliers&cov=NA&searchx=true&what={}&which=prod".format(sn))
        res = res.find_all('div',class_="search-list")
        sns[sn] = {}
        for it in res[0].find_all('li'):
            sns[sn][it.find('a').text] = it.find('a')['href']
    return sns
'''

class ThomasnetCrawler():


    def get_suppliers(self, material='plastics'):
        # the material name must be prefict
        
        url = 'https://www.thomasnet.com/catalogs/keyword/{}/'.format(material)
        bc = BasicCrawler()
        res = bc.get_soup(url, safetime=(3,5))
        
        companies = res.find_all('div', class_='company')
        company_names = [i.find('div', class_ = 'coname').text for i in companies]
   
        return company_names
    


    def get_thomasnet_supplier_link(self, supplier_name = 'Industrial Plastic Supply'):
        search_name = re.sub('[^\w]',' ', supplier_name).replace(' ','+')
        url = "https://www.thomasnet.com/search.html?WTZO=Find+Suppliers&cov=NA&searchx=true&what={}&which=prod".format(search_name)
        bc = BasicCrawler()
        res = bc.get_soup(url, safetime=(3,5))
        box = res.find('div',class_="search-list")
    
        link = None
        if box.find('h2').text == 'Suppliers by Name':
            anchor = box.find('li').find('a')
            link = 'https://www.thomasnet.com/' + anchor['href']
        
        print(link)
        
        return link
    
    def get_bizdetails(self, url_company = 'https://www.thomasnet.com//profile/00281106/industrial-plastic-supply-inc.html?cid=281106&cov=NA&searchpos=1&what=Industrial+Plastic+Supply&which=comp'):
        name = None
        revenue = None
        
        bc = BasicCrawler()
        res = bc.get_soup(url_company, safetime=(3,5))
        
        anchor = res.select('#copro_naft > div.codetail > h1')
        name = anchor[0].text
        link = anchor[0].find('a')['href']
            
        details_block = res.select('#copro_bizdetails')
        columns = details_block[0].find_all('div', class_ = 'match-height')
        
        bds = columns[1].find_all('div', class_ = 'bizdetail')
        for bd in bds:
            try:
                bd_header = str.strip(bd.find('div').text)
            except Exception:
                 bd_header = None
            
            if bd_header == 'Annual Sales:':
                revenue = bd.find('li').text
        
        return name, link, revenue
    
    def run(self, materials):
        # the material name must be prefict
        
        df = pd.DataFrame()
        
        names = []
        links = []
        revenues = []
        
        for material in materials:
            supplier_names = self.get_suppliers(material)
            link = self.get_thomasnet_supplier_link(supplier_names[0])
            name, link, revenue = self.get_bizdetails(link)
            
            names.append(name)
            links.append(link)
            revenues.append(revenue)
        
        df['name'] = names
        df['link'] = links
        df['revenue'] = revenues
        
        print(df)

    
def test():
    suppliers = [] #"Jabil", "Sanmina", "Thermo Fisher Diagnostics", "IVEK", "Randox Laboratories", "Inpeco", "Nypro", "Carclo", "Bio-Rad Laboratories"]
    
    revenues = []
    rc = RevenueCrawler()
    for supplier in suppliers:
        revenues.append(rc.run(supplier))
    
    result = pd.DataFrame()
    result['supplier']=suppliers
    result['revenue'] = revenues
    
    print(result)
    result.to_csv('SPIDER.csv')



if __name__ == '__main__':
    
    pd.set_option('max_colwidth',200)
    pd.set_option('max_columns',None) 
    
    tc = ThomasnetCrawler()
    tc.run(['plastics'])
    

    
   
        
        
        
        
        

    