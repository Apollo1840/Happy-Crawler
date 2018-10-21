# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 19:34:04 2018

@author: zouco


This py file is for me to test the BasicCrawler. 
And it is also a good material for learner to learn to use BasicCrawler


"""

from bc3 import BasicCrawler
from bc3 import BasicCrawlerGroup

import time




def general_test():
    test_page = 'http://zoucongyu.strikingly.com'
    
    bcg = BasicCrawlerGroup(proxies='auto', headers='auto', num_crawler=2)
    
    print(len(bcg.main_crawler.proxies_list_))
    print(len(bcg.crawlers[0].proxies_list_))
    print(bcg.crawlers[0].proxies_)
    print(len(bcg.crawlers[1].proxies_list_))
    print(bcg.crawlers[1].proxies_)
    
    soup = bcg.crawlers[0].get_soup(test_page)
    print(soup.find('a'))
    
    soup = bcg.crawlers[1].get_soup(test_page)
    print(soup.find('a'))
    

def bcg_comparison_test():
    test_page= 'https://news.baidu.com'
    
    
    t1 = time.time()
    bcg = BasicCrawlerGroup(num_crawler=4, proxies='auto', safetime=(2,2))
    soups = bcg.run([test_page for i in range(40)])
    print(soups[-1].find('a'))
    t11=time.time() - t1
    print(t11)
    
    t1 = time.time()
    soups = []
    bc = BasicCrawler(proxies='auto', safetime=(2,2))
    for url in [test_page for i in range(40)]:
        soups.append(bc.get_soup(url))
    t12=time.time() - t1
    print(t12)
    print(t11)
 
    
def test_bcg_save_htmls():
    test_page= 'https://news.baidu.com'
    bcg = BasicCrawlerGroup(num_crawler=4, proxies='auto')
    bcg.run([test_page for i in range(12)], task='save html')
  
    
    
    
    
if __name__ == '__main__':
    
    
    
    
    
    
    # crawler = BasicCrawler()
    # soup = crawler.get_soup('https://www.bbc.com/news')
    # print(soup.find('a'))

    # bcg_comparison_test()
    # crawler.save_htmls(['https://news.baidu.com' for _ in range(10)])
    test_page= 'https://news.baidu.com'
    bcg = BasicCrawlerGroup(num_crawler=4, proxies='auto', safetime=(2,2))
    bcg.rename_crawlers_output()
    bcg.run([test_page for i in range(12)], task='save html')