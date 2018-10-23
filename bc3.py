# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 19:55:44 2018

@author: zouco

"""


import requests
from requests.exceptions import ProxyError
from requests.exceptions import SSLError
from requests.exceptions import ConnectTimeout
from bs4 import BeautifulSoup
import os
import time
import random

import threading

import pandas as pd



class BasicCrawler():
    history_ua_=[]
    
    user_agents_ = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7"
            ]
    
    cookies_ = ['__qca=P0-1364584360-1536347334653; _ga=GA1.2.1495173256.1536347336; __gads=ID=f60351a9ba08e194:T=1536347334:S=ALNI_MbbMZMhTc_K9zjRIl9mXfULbxE6XQ; last_city=90; last_type=0; login_token=cf47e8884526baf9be015fb0e41eeba0c3d7c6b18014df8ba1de55acc997e3f7932012d; dev_ref_no=FPTbO0; PHPSESSID=vhr1qqabb6t6jn8pa27fpi5gd4; OX_plg=swf|wmp|shk|pm; last_cat=0; X-Access-Token=0e23d203c687f84fe9c414bb9b1b53de59aeed2c; X-Refresh-Token=e949824ab71397cefe823a925d64cef00ad079ad; X-Client-Id=wg_desktop_website; X-Dev-Ref-No=FPTbO0; _gid=GA1.2.1174269582.1537624058; open_websocket=yes; conversation_list=; OX_sd=3',
                'CONSENT=YES+DE.zh-CN+20150622-23-0; NID=139=Xq4f-VHxFzwsiydy4mpVohpciSkLChO9jeYv1dh-HQsu5lV3Qtz4ScYWtpPBBAlv6bJ0mRiAj1YWpifB5YSBrf3B9ek2mQgKI2Uyf9J2iABQJKRJ_3WpliQ2mVz8CD35; 1P_JAR=2018-9-22-18; UULE=a+cm9sZToxIHByb2R1Y2VyOjEyIHByb3ZlbmFuY2U6NiB0aW1lc3RhbXA6MTUzNzY0MTg2MTk3NzAwMCBsYXRsbmd7bGF0aXR1ZGVfZTc6NDgyMTQwMTYwIGxvbmdpdHVkZV9lNzoxMTYxNDYxNzZ9IHJhZGl1czozNjU4MDA=']
        
    
    def __init__(self, headers=None, proxies=None, api_ID='869291819078202384', num_proxies=20, 
                 safetime=(0,0), patience = 10):
        
        # headers do not need to explain
        # api_ID and num_proxies is needed for self.generate_proxies_list()
        # proxies can be 'auto' or a proxies and a list of proxies
        # safetime: how much time should we wait until next sraping next page
        
        self.name = random.randint(1000,2000)
        
        if headers =='auto':
            self.generate_headers()            
        else:
            self.headers_ = headers
        
        # proxies_list_ get ready
        self.proxies_list_ = []
        
        # prepare for generate_proxies_list()
        self.num_proxies_ = num_proxies
        self.api_ID_ = api_ID
        self.hide_ip_ = False
        
        if proxies =='auto':
            self.generate_proxies()
        
        elif isinstance(proxies, list):
            self.proxies_list_ = proxies
            self.proxies_ = self.proxies_list_[0]
            self.num_proxies_ = len(proxies)
        
        else:
            self.proxies_ = proxies
        
        # other settings
        self.working_folder_ = 'nest'
        self.name_page_ = 'web'
        self.keep_note = False
        self.note_ = {}
        self.safetime = safetime
        self.patience = patience
        
        # ready for response
        self.response_ = None
    
    # -- interface    
        
    def run(self, urls, is_save_html=True, is_local=False):
        '''
        It will return the soup of url to you. 
        If the input is urls, it can return soups (a list of soup).
        It will save the html file in the meantime.
        
        '''
        
        if not isinstance(urls,list): urls = [urls]
        
        soups = self.get_soups(urls, is_local=is_local)             
        if is_save_html:
            self.is_save_htmls(urls)
            
        if len(soups) == 1: return soups[0]
        else: return soups
    
    
    def get_soup(self, urls, is_local=False):
        self.run(urls, is_save_html=False, is_local=is_local)
    
    
    def is_save_html(self, urls):  
        if not isinstance(urls,list): urls = [urls]
        self.is_save_htmls(urls)
    
    
    def get_df(self, urls, func, save_csv=True, path='outputs/'):
        soups = self.get_soups(urls)
        data = [func(soup) for soup in soups]
        df = pd.DataFrame(data)
        df.to_csv(path+'result.csv')
        return df   
    
    
    # -- build in function
    
    # basics:
    def get(self, url):
        
        time.sleep(random.randint(*self.safetime))
        
        exist_error = True
        while exist_error:
            try:
                response = requests.get(url, proxies = self.proxies_, headers=self.headers_, timeout = 10)
                exist_error = False
            except (ProxyError, SSLError, ConnectionError, ConnectTimeout) as e:
                if self.proxies_ is not None:
                    self.generate_proxies()
                else:
                    raise e
                        
        self.response_ = response
        return response
    
    
    def probe(self, soup):
        return True
    

    # blocks: 
    def get_soups(self, urls, is_local=False):
        soups = []
        for url in urls:
            soups.append(self.get_soup_single(url, is_local=is_local))
        return soups
    
    
    def get_soup_single(self, url, is_local=False): 
        soup = self.get_soup_trival(url)
        while not self.probe(soup) and self.patience > 0 and self.proxies_ is not None:
            self.generate_proxies()
            soup = self.get_soup_trival(url, is_local=is_local)
            self.patience -= 1
        
        if self.patience > 0:
            return soup
        else:
            print('been detected')
            raise Exception
    
    
    def get_soup_trival(self, url, is_local=False):
        if is_local:
            with open(self.note_[url], 'rb') as f:
                soup = BeautifulSoup(f,'html5lib')
        else:
            self.get(url)
            soup = BeautifulSoup(self.response_.text,'lxml')
        return soup
    

    def is_save_htmls(self, urls):
        i = 0
        self.name_page_ += str(i)
        for url in urls:
            # print(i)
            i += 1
            self.get(url)
            self.name_page_ = self.name_page_[:-1] + str(i)
            self.is_save_html_single()
     
        
    def is_save_html_single(self):
        # use get() first, note: get_soup() contains get()
        
        working_folder = 'outputs/{}'.format(self.working_folder_)
        if not os.path.exists(working_folder):
            os.makedirs(working_folder)
        save_path = '{}/{}.html'.format(working_folder, self.name_page_)    
        
        self.response_.encoding='utf-8'
        with open('outputs/page.txt','w', encoding="utf-8") as f:
            f.write(self.response_.text)
        os.rename('outputs/page.txt', save_path)
        
        if self.keep_note:
            self.note.update({self.response_.url : save_path})
    
    def generate_headers(self):
        user_agent = random.choice(self.user_agents_)
        BasicCrawler.history_ua_.append(user_agent)
        
        headers = {'User-Agent': user_agent}
        headers.update({'Cookie': self.cookies_[1]})
        
        self.headers_ = headers
        return headers
    
    
    def generate_proxies(self): 
        print('{} generate proxies'.format(self.name))
        
        while len(self.proxies_list_) <= 0:
            print('creat list\n')
            self.create_proxies_list()
            print('{} remain_ips:{}'.format(self.name, len(self.proxies_list_))) 
            
        assert len(self.proxies_list_)>0, self.name
        
        self.proxies_ = self.proxies_list_.pop(0)
        print('{} remain_ips:{}'.format(self.name, len(self.proxies_list_)))        
    
    
    def create_proxies_list(self, proxies = None, headers = None):
        # the proxies and headers here are for getting ip from website
        
        if self.num_proxies_ == None: self.num_proxies_ = 17
        if self.hide_ip_ == True and len(self.proxies_list_) > 0: proxies = self.proxies_list_[0]
        
        proxy_url = 'https://proxyapi.mimvp.com/api/fetchopen.php?orderid={}&num={}&anonymous=5&result_fields=1,2'.format(self.api_ID_, self.num_proxies_)
        
        exist_error = True
        i = 1
        while exist_error:
            try:
                response = requests.get(proxy_url, proxies=proxies, headers=headers, timeout=30)
                
                soup = BeautifulSoup(response.text, 'lxml')
                proxies_list_raw = [str.strip(p) for p in str.split(soup.find('p').text,'\r')]
                if len(proxies_list_raw) == self.num_proxies_ : exist_error = False
            except (ProxyError, SSLError, ConnectionError, ConnectTimeout):
                print('server delay')
                i += 1
                time.sleep(10**i)
                if i > 3: raise Exception
            
        def modify_proxies(proxy, include_none_https = True, include_only_https = True):
            if len(proxy.split(',')) == 2:
                mark = str.strip(proxy.split(',')[1])    
                if mark == 'HTTP' and include_none_https:
                    return { "http": 'http://' + proxy.split(',')[0]}
                elif mark == 'HTTPS' and include_only_https:
                    return { 'https': 'http://' + proxy.split(',')[0]}
                elif mark == 'HTTP/HTTPS':
                    return { "http": 'http://' + proxy.split(',')[0], 'https': 'http://' + proxy.split(',')[0]}
            else:
                return None
            
        proxies_list = [modify_proxies(proxy) for proxy in proxies_list_raw]
        
        self.proxies_list_.extend(list(filter(None, proxies_list)))
        return self.proxies_list_            
    
            

            



class BasicCrawlerGroup():
    
    def __init__(self, num_crawler=2, headers=None, proxies=None, api_ID='869291819078202384', num_proxies = 20, safetime=(0,0)):
        self.crawlers=[]
        self.main_crawler = BasicCrawler(headers=headers, proxies=proxies, api_ID=api_ID, num_proxies=num_proxies*num_crawler, safetime=safetime)
        
        main_proxies_list = cut_list(self.main_crawler.proxies_list_, num_crawler)
        # cut_list will cut the list into several parts (roughly equal length)
        
        for i in range(num_crawler):
            bc = BasicCrawler(headers=headers, proxies=main_proxies_list[i], api_ID=api_ID, num_proxies=num_proxies, safetime=safetime)
            bc.hide_ip = True
            print(bc.name)
            self.crawlers.append(bc)  
            
        print('\n ----- crawler group ready  ---- \n')  
    
    
    def run(self, urls, task='get soup'):
        def action(bc, urls):
            print('crawler {} is working now...'.format(bc.name))
            
            if task == 'get soup':
                soups.extend(bc.get_soups(urls))
            elif task == 'save html':
                bc.is_save_htmls(urls)
        
        if task == 'save html':
            self.rename_crawlers_output()

        urls_parts = cut_list(urls, len(self.crawlers))
        soups = []
        thread_list=[]
        for i in range(len(self.crawlers)):
                t = threading.Thread(target=action, 
                                     name='worker_{}'.format(i), 
                                     args=(self.crawlers[i], urls_parts[i])
                                    )
                thread_list.append(t)
                t.start()
        for t in thread_list:
            t.join()
        
        return soups
        
    
    def rename_crawlers_output(self):
        i = 0
        for crawler in self.crawlers:
            crawler.name_page_ += '_{}_'.format(i)
            i += 1
            
 
           
# math-tools
import math
import numpy as np

def cut_range(a, b, bins):
    l = range(a, b)
    le = math.ceil((b-a)/bins)
    result = []
    for i in range(bins):
        result.append(l[i*le:(i+1)*le])
    return result

def cut_list(the_list, bins):
    if len(the_list) < bins:
        return [None for _ in range(bins)]  # it is important to have None here (for proxies management)
    
    num_last = len(the_list)%bins
    if num_last !=0:
        the_last = the_list[-num_last:]
        the_list = the_list[:-num_last]
    index = np.arange(len(the_list))  
    #return [piece for piece in np.hsplit(index,bins)]
    result = [the_list[piece[0]:piece[-1]+1] for piece in np.hsplit(index,bins)]
    if num_last !=0:
        for i in range(len(the_last)):
            result[i].extend([the_last[i]])
    return result

        
    	     
if __name__ == '__main__':
    
    test_page =  'https://news.baidu.com'
    
    crawler = BasicCrawler()
    soup = crawler.run(test_page)
    print(soup.find('a'))
    
    # BasicCrawlerGroup is faster
    crawlers = BasicCrawlerGroup()
    soups = crawlers.run([test_page for _ in range(5)])
    
    for soup in soups:
        print(soup.find('a'))

 
   
    
    

       