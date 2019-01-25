# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 23:46:25 2018

@author: zouco
"""


from bc3 import BasicCrawler

# 0. run

# the first function for BasicCrawler is run

'''
  It will return the soup of url to you.
  If the input is urls, it can return soups (a list of soup).
  It will save the html file in the meantime.
  
'''

# input as urls
test_url = 'https://www.google.com'
test_urls = [test_url for _ in range(5)]



bc = BasicCrawler()
soup = bc.run(test_url)
print(soup.title.text)

soups = bc.run(test_urls)
print([soup.title.text for soups in soups])


# furthermore, you can define how do you save
bc.working_folder_ = 'my_working_folder'
bc.name_page_ = 'the_page'  # default to be the name of the crawler
bc.run(test_url, is_save_html=True)

# of course, you can disable the save html function
soup = bc.run(test_url, is_save_html=False)  # it is True by default
# the reason for that is for local bootstraping


# --------------------------------------
# 1. get_soup and save_html
# if you do not like the run API, there is a more comprehensive way to use BasicCrawler

soup = bc.get_soup(test_url)  # this is equal to bc.run(test_url, is_save_html=False)
soups = bc.get_soup(test_urls)
# or
bc.save_html(test_url)
bc.save_html(test_urls)


# --------------------------------------
# 2, adjust the BasicCrawler

# to look like human, you need to set headers. you can easily set your headers automatically
bc = BasicCrawler(headers='auto')

# or you can set it manually
bc = BasicCrawler()
bc.user_agents_= ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            ]
bc.cookies_=['CONSENT=YES+DE.zh-CN+20150622-23-0; NID=139=Xq4f-VHxFzwsiydy4mpVohpciSkLChO9jeYv1dh-HQsu5lV3Qtz4ScYWtpPBBAlv6bJ0mRiAj1YWpifB5YSBrf3B9ek2mQgKI2Uyf9J2iABQJKRJ_3WpliQ2mVz8CD35; 1P_JAR=2018-9-22-18; UULE=a+cm9sZToxIHByb2R1Y2VyOjEyIHByb3ZlbmFuY2U6NiB0aW1lc3RhbXA6MTUzNzY0MTg2MTk3NzAwMCBsYXRsbmd7bGF0aXR1ZGVfZTc6NDgyMTQwMTYwIGxvbmdpdHVkZV9lNzoxMTYxNDYxNzZ9IHJhZGl1czozNjU4MDA='
             ]
bc.generate_headers()
# then headers will be set

# you can also use IP proxy service to change IP dynamically
bc = BasicCrawler(proxies=[{'https': '1.0.0.0','http':'1.0.0.0'}])

# or simpliy:
bc = BasicCrawler(proxies='auto')
# But! this function is not working just by BasicCrawler. 
# you need to buy IP proxy service in Mipu.com and set your service IP by
bc.api_ID_='869291819078202384'
bc.num_proxies_=10
bc.generate_proxies()

# or
bc = BasicCrawler(proxies='auto', api_ID_='869291819078202384', num_proxies=20)

# --------------------------------------
# 3, local working flow

# assume we already got html files locally
# and those htmls is scraping by this crawler, which means we got .note in this crawler 

# we can use .run() or .get_soup() easily:

bc = BasicCrawler()
bc.keep_note = True
bc.save_html(test_urls)

soup = bc.run(test_urls, is_local=True)
soups = bc.get_soup(test_urls, is_local=True)
# [soup.title.text for soup in soups]

# how to produce note for next BasicCrawler?
bc = BasicCrawler()
bc.keep_note = True
bc.save_html(test_urls)
bc.write_tombstone()

bc2 = BasicCrawler()
bc.read_tombstone('1598_5_note.json')
soups = bc.run(test_urls, is_local=True)
# [soup.title.text for soup in soups]

#----------------------------------------------
# aggragate the crawler with the tasks

class TitleCrawler(BasicCrawler):
    def __init__(self):
        super().__init__()
    
    def work_on(self, urls, is_local=False, save_csv=False):
        return self.get_df(urls, self.getWebTitle, save_csv=save_csv, is_local=is_local)
        
    @staticmethod
    def getWebTitle(soup):
        '''
            get the web title of the soup
        '''
        
        # input as soup, output as what you want as a list or tuple
        
        try:
            title = soup.title.string
        except:
            title = None
            
        return title 
        

tc = TitleCrawler()
df = tc.work_on(test_urls)
print(df)

# you can also ask it to work locally.
tc.save_html(test_urls) # or tc.read_tombstone()
 
tc.work_on(test_urls, is_local=True)


#----------------------------------------------
# BasicCrawlerGroup


from bc3 import BasicCrawlerGroup

# firstly, we can understand BasicCrawlerGroup as a faster version of BasicCrawler

crawlers = BasicCrawlerGroup(num_crawler=2)  # 2 is default
soups = crawlers.run(test_urls)
    
for soup in soups:
    print(soup.title.text)
    
# BasicCrawlerGroup can not deal with single url, number of urls must be suffient enough.

bc = BasicCrawler()
bc.working_folder_ = 'outputs\\nest'
bcg = BasicCrawlerGroup(2, bc)
soups = bcg.run(test_urls)
    
for soup in soups:
    print(soup.title.text)



# local working

# first we need to do some preparation (to get notes)
bcg = BasicCrawlerGroup(2, bc)
soups = bcg.run(test_urls, "save html")

# after that we can get the notes
bcg.read_all_tombstone()
# or bcg.read_all_tombstone("...", is_abs_path=True) 
soups =  bcg.run(test_urls, "get soup", is_local = True, has_note=True)

# or we could directly use:
soups =  bcg.run(test_urls, "get soup", is_local = True)
# it will read all tombstone automatically

for soup in soups:
    print(soup.title.text)



# aggragete bcg
    
class TitleCrawlers(BasicCrawlerGroup):
    def __init__(self):
        super().__init__()
    
    def work_on(self, urls, is_local=False, save_csv=False):
        return self.get_df(urls, self.getWebTitle, save_csv=save_csv, is_local=is_local)
    
    @staticmethod
    def getWebTitle(soup):
        '''
            get the web title of the soup
        '''
        
        # input as soup, output as what you want as a list or tuple
        
        try:
            title = soup.title.string
        except:
            title = None
            
        return title

tc = TitleCrawlers()
df = tc.work_on(test_urls)

print(df)

# locally:
tc = TitleCrawlers()
tc.run(test_urls, "save html")
df = tc.work_on(test_urls, is_local=True)

print(df)

