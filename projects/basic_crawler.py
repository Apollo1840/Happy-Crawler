# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 17:59:23 2018

@author: zoc
"""
import requests
from requests.exceptions import ProxyError 
from bs4 import BeautifulSoup
import os
import time
import random
import urllib

class BasicCrawler():
    '''this class will be initialize with a url.
    by default it will use utf-8 as decoder.
    
    properties:
        html:  the html text of the url
        soup:  the soup created by BeautifulSoup method
    '''
    history_ua_ = []
    
    proxies_list_ = []
    current_proxies_ = None
            
    def __init__(self, url="https://github.com/Apollo1840/Happy-Crawler", encoding = 'utf-8', safetime=(0,0),
                 headers='auto', proxies=None):
        
        time.sleep(random.randint(*safetime))
        
        if headers is None and proxies is None:
            self.response = requests.get(url)
            
        else:
            # generate headers and proxies if it is needed
            if headers is 'auto':
                    headers = BasicCrawler.generate_headers()
            
            if proxies is 'auto':
                if BasicCrawler.current_proxies_ is None:
                    proxies = BasicCrawler.generate_proxies()
                else:
                    proxies = BasicCrawler.current_proxies_
           
            # get response
            if headers is None and proxies is not None:
                try:
                    self.response = requests.get(url, proxies = proxies, timeout = 60)
                except ProxyError:
                    proxies = BasicCrawler.generate_proxies()
                    self.response = requests.get(url, proxies = proxies, timeout = 60)
              
            elif headers is not None and proxies is None:
                self.response = requests.get(url, headers = headers, timeout = 60)
                
            else:
                try:
                    self.response = requests.get(url, headers = headers, proxies = proxies, timeout = 60)
                except ProxyError:
                    proxies = BasicCrawler.generate_proxies()
                    self.response = requests.get(url, headers = headers, proxies = proxies, timeout = 60)
     

    @staticmethod
    def generate_headers():
        user_agents = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
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
        
        cookies = ['__qca=P0-1364584360-1536347334653; _ga=GA1.2.1495173256.1536347336; __gads=ID=f60351a9ba08e194:T=1536347334:S=ALNI_MbbMZMhTc_K9zjRIl9mXfULbxE6XQ; last_city=90; last_type=0; login_token=cf47e8884526baf9be015fb0e41eeba0c3d7c6b18014df8ba1de55acc997e3f7932012d; dev_ref_no=FPTbO0; PHPSESSID=vhr1qqabb6t6jn8pa27fpi5gd4; OX_plg=swf|wmp|shk|pm; last_cat=0; X-Access-Token=0e23d203c687f84fe9c414bb9b1b53de59aeed2c; X-Refresh-Token=e949824ab71397cefe823a925d64cef00ad079ad; X-Client-Id=wg_desktop_website; X-Dev-Ref-No=FPTbO0; _gid=GA1.2.1174269582.1537624058; open_websocket=yes; conversation_list=; OX_sd=3',
                'CONSENT=YES+DE.zh-CN+20150622-23-0; NID=139=Xq4f-VHxFzwsiydy4mpVohpciSkLChO9jeYv1dh-HQsu5lV3Qtz4ScYWtpPBBAlv6bJ0mRiAj1YWpifB5YSBrf3B9ek2mQgKI2Uyf9J2iABQJKRJ_3WpliQ2mVz8CD35; 1P_JAR=2018-9-22-18; UULE=a+cm9sZToxIHByb2R1Y2VyOjEyIHByb3ZlbmFuY2U6NiB0aW1lc3RhbXA6MTUzNzY0MTg2MTk3NzAwMCBsYXRsbmd7bGF0aXR1ZGVfZTc6NDgyMTQwMTYwIGxvbmdpdHVkZV9lNzoxMTYxNDYxNzZ9IHJhZGl1czozNjU4MDA=']
        
        user_agent = random.choice(user_agents)
        BasicCrawler.history_ua_.append(user_agent)
        
        headers = {'User-Agent': user_agent}
        headers.update({'Cookie': cookies[1]})
        
        return headers
    
    @staticmethod
    def generate_proxies(): 
        if len(BasicCrawler.proxies_list_) == 0:
            BasicCrawler.create_proxies_list()

        BasicCrawler.current_proxies_ = BasicCrawler.proxies_list_.pop(0)
        
        print('generate proxies')
        
        return BasicCrawler.current_proxies_
    
    @staticmethod
    def create_proxies_list():
        def spider_proxy():         
            proxy_url = 'https://proxyapi.mimvp.com/api/fetchopen.php?orderid=861222618991190326&num=10&http_type=1,2&anonymous=5&result_fields=1,2'
            req = urllib.request.Request(proxy_url)
            content = urllib.request.urlopen(req, timeout=30).read()
            proxy_list = content.decode().split("\n")
            return proxy_list
        
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
        
        print('creat list\n')
        BasicCrawler.proxies_list_ = list(filter(None, [modify_proxies(proxy) for proxy in spider_proxy()]))
    

        
    @property
    def html(self):
        return self.response.text
    
    @property
    def soup(self):
        return BeautifulSoup(self.html, 'lxml')
    
    def save_html(self, name='page'):
        self.response.encoding='utf-8'
        with open('material/page.txt','w', encoding="utf-8") as f:
            f.write(self.response.text)
        os.rename('material/page.txt','material/{}.html'.format(name))
    
    def run(self):
        
        information = """
        This crawler does nothing. 
        You can use bc.html to get the html text of the website.
        You can use bc.soup to get the soup by BeautifulSoup method.
        """
        
        print(information)
    
    
def proxy_formatter(ip,portal):
    content = 'http://{0}:{1}'.format(ip, portal)
    return {'http': content, 'https': content}


def test():
    crawler = BasicCrawler('https://www.bbc.com/news', proxies = 'auto')
    print(crawler.soup.find('a'))
    
    print(BasicCrawler.proxies_list_)
    print(len(BasicCrawler.proxies_list_))
    print(BasicCrawler.current_proxies_)
    
    for i in range(20):
        crawler = BasicCrawler('https://www.bbc.com/news', proxies = 'auto')
        print(crawler.soup.find('a'))
        print(len(crawler.proxies_list_))
        print(crawler.current_proxies_)
        print('round {}'.format(i))



if __name__ == '__main__':
    crawler = BasicCrawler('https://www.bbc.com/news')
    print(crawler.html)
    

