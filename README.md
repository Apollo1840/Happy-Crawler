# Happy-Crawler

There are crawlers made by HC-team.

To use the crawlers just 
        
        from xxx_crawler import xxx_crawler
        xxx_c = xxx_crawler()
        xxx_c.run()
    
### 1) bbc_crawler
It is good at dealing with news page.

### 2) douban_crawler
It is good at finding the hot words.

To use it, just

        from douban_crawler import douban_crawler
        d_c = douban_crawler()
        d_c.run()

It will crawl 5 pages of douban/blabla (https://www.douban.com/group/blabla//discussion?start=0) and save an wordCloud graph as html in material folder.

![WordCloud](https://screenshot.net/zh/28dzdb4)


You can adjust the pages and interested flag of words.
        
        d_c.run(num_pages=5, consider_tags=['n','nr','nrt'])  # this is default value

You can also ajust the method to calculate heat, currently it supports three different method.

        d_c.run(include_heat=False)  # this will only consider the frequency of words.
        d_c.run(adjustment = 'log')  # this is a compromise between frequency of words and the heat of post.

douban_crawler also provide other possibilities to visualize the data.

        d_c.get_words_list(num_pages=5, include_heat=True)
        d_c.create_words_table(get_raw_data=True)  

It will output a csv file to material folder. This DataFrame has three columns: word, flag, heat. The heat is the heat of the origin post.
    
## Another folders:

### tutorial
There are some learning material.
    
### dummy_websites
There are some simple demonstrations of html5.

### material
Useless. It stores the sample output of the crawlers.


