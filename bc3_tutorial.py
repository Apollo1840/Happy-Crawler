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
bc.run(test_url, save_html=True)

# of course, you can disable the save html function
soup = bc.run(test_url, save_html=False)  # it is True by default



# 1. get_soup and save_html
# if you do not like the run API, there is a more comprehensive way to use BasicCrawler

soup = bc.get_soup(test_url)  # this is equal to bc.run(test_url, save_html=False)
soups = bc.get_soup(test_urls)
# or
bc.save_html(test_url)
bc.save_html(test_urls)


# 2, adjust the BasicCrawler

