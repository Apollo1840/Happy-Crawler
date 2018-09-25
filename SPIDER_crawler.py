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
    
    def __init__(self):
        self.df = None

    def get_suppliers(self, material='plastics'):
        # the material name must be prefict
        
        url = 'https://www.thomasnet.com/catalogs/keyword/{}/'.format(material)
        bc = BasicCrawler()
        res = bc.get_soup(url, safetime=(1,1))
        
        companies = res.find_all('div', class_='company')
        company_names = [i.find('div', class_ = 'coname').text for i in companies]
   
        return company_names
    
    def is_suppliers_page(self, soup):
        title = soup.find('h1', class_='supplier-search-results__page-title').text
        return title.endswith('Suppliers')
    
    def get_suppliers_link_general(self, material = 'plastics'):
        
        material = 'plastics'
        s = material.replace(' ','+')
        url = 'https://www.thomasnet.com/search.html?WTZO=Find+Suppliers&cov=NA&searchx=true&what={}&which=prod'.format(s)
        
        bc = BasicCrawler()
        soup = bc.get_soup(url)
        
        if self.is_suppliers_page(soup):
            soup2 = soup
        else:
            table = soup.find('table', class_='table-striped')
            rows = table.find_all('tr')
            link = 'https://www.thomasnet.com/' + rows[0].find('td').find('a')['href']
            soup2 = bc.get_soup(link)
        
        divs = soup2.find_all('div', class_='profile-card--secondary')
        company_names = []
        company_links = []
        for div in divs:
            anchor = div.find('h2').find('a')
            company_names.append(anchor.text)
            company_links.append('https://www.thomasnet.com/' + anchor['href'])
        
        print(company_names, company_links)
        

    def get_thomasnet_supplier_link(self, supplier_name = 'Industrial Plastic Supply'):
        search_name = re.sub('[^\w]',' ', supplier_name).replace(' ','+')
        url = "https://www.thomasnet.com/search.html?WTZO=Find+Suppliers&cov=NA&searchx=true&what={}&which=prod".format(search_name)
        bc = BasicCrawler()
        res = bc.get_soup(url, safetime=(1,1))
        box = res.find('div',class_="search-list")
    
        link = None
        if box.find('h2').text == 'Suppliers by Name':
            anchor = box.find('li').find('a')
            link = 'https://www.thomasnet.com/' + anchor['href']
        
        print('Give me 3 seconds, I am scraping the information of {} ...'.format(supplier_name))
        
        return link
    
    def get_bizdetails(self, url_company = 'https://www.thomasnet.com//profile/00281106/industrial-plastic-supply-inc.html?cid=281106&cov=NA&searchpos=1&what=Industrial+Plastic+Supply&which=comp'):
        name = None
        revenue = None
        num_employee = None
        year_founded = None
        
        
        bc = BasicCrawler()
        res = bc.get_soup(url_company, safetime=(1,2))
        
        anchor = res.select('#copro_naft > div.codetail > h1')
        name = anchor[0].text
        link = anchor[0].find('a')['href']
            
        details_block = res.select('#copro_bizdetails')
        columns = details_block[0].find_all('div', class_ = 'match-height')
        
        bds = columns[1].find_all('div', class_ = 'bizdetail')
        for bd in bds:
            try:
                bd_header = str.strip(bd.find('div').text)
                if bd_header == 'Annual Sales:':
                    revenue = bd.find('li').text
                if bd_header == 'No of Employees:':
                    num_employee = bd.find('li').text
                if bd_header == 'Year Founded:':
                    year_founded = bd.find('li').text
           
            except Exception:
                 bd_header = None

        return name, link, revenue, num_employee, year_founded
    
    def run(self, material, number_suppliers=3):
        # the material name must be prefict
        
        df = pd.DataFrame()
        
        names = []
        links = []
        revenues = []
        materials = []
        num_employees = []
        year_foundeds = []
        
        
        supplier_names = self.get_suppliers(material)
        for supplier in supplier_names[:number_suppliers]:
            link = self.get_thomasnet_supplier_link(supplier)
            name, link, revenue, num_employee, year_founded = self.get_bizdetails(link)
            
            materials.append(material)
            names.append(name)
            links.append(link)
            revenues.append(revenue)
            num_employees.append(num_employee)
            year_foundeds.append(year_founded)
            
        
        df['material'] = materials
        df['name'] = names
        df['link'] = links
        df['revenue'] = revenues
        df['num_employee'] = num_employees
        df['year_founded'] = year_founded
        
        
        
        self.df = df
        print(df)
        df.to_csv('SPIDER_{}.csv'.format(material))
        return df

    
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
    #df = tc.run('plastics', number_suppliers=3)
    
    df = tc.run('chemicals', number_suppliers=4)
    

    
   
        
        
        
        
        

    