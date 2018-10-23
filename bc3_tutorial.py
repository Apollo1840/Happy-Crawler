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

test_url = 'https://www.google.com'

bc = BasicCrawler()
soup = bc.run(test_url)
print(soup.title.text)

# input as urls
test_url = 'https://www.google.com'
test_urls = [test_url for _ in range(5)]

soups = bc.run(test_urls)
print([soup.title.text for soups in soups])


# furthermore, you can define how do you save
bc.working_folder_ = 'my_working_folder'
bc.name_page_ = 'the_page'
bc.run(test_url, is_save_html=True)

# of course, you can disable the save html function
soup = bc.run(test_url, is_save_html=False)  # it is True by default


# --------------------------------------
# 1. get_soup and is_save_html
# if you do not like the run API, there is a more comprehensive way to use BasicCrawler

soup = bc.get_soup(test_url)  # this is equal to bc.run(test_url, is_save_html=False)
soups = bc.get_soup(test_urls)
# or
bc.is_save_html(test_url)
bc.is_save_html(test_urls)


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

