# Happy-Crawler

There are crawlers made by HC-team. If you like them or want to see more upgrade of them, please press Star or join us (contact: zoucongyu1993@hotmail.com, wechat:zoucongyu1109) at the right up corner, thank you!

To use the crawlers just 
        
        from xxx_crawler import xxx_crawler
        xxx_c = xxx_crawler()
        xxx_c.run()

Please be careful:
Those crawlers are only designed for research purposes, no commercial usage is allowed. The user should take the fully responsibility for illegal use and intented attack.

### 1) bbc_crawler
It is good at dealing with news page.

### 2) douban_crawler
It is good at finding the hot words.

To use it, just

        from douban_crawler import douban_crawler
        d_c = douban_crawler()
        d_c.run()

It will crawl 5 pages of douban/blabla (https://www.douban.com/group/blabla//discussion?start=0), get the posts, break them down to several words, calculate the heat of the words and then save an wordCloud graph as html in material folder.

Example:

![the sample picture](https://i.screenshot.net/28dzdb4)

#### 2.1 Pages and flags

You can adjust the pages and interested flag of words.
        
        d_c.run(num_pages=5, consider_flags=['n','nr','nrt'])  # this is default value

Some basic flags are: "n" for noun，“a” for adj，“v” for verb. For more details, please see: https://blog.csdn.net/suibianshen2012/article/details/53487157

#### 2.2 Heat calculation

You can also adjust the method to calculate heat, currently it supports three different method.

        d_c.run(include_heat=False)  # this will only consider the frequency of words.
        d_c.run(adjustment = 'log')  # this is a compromise between frequency of words and the heat of post. Default is None.

#### 2.3 Get raw data

The douban_crawler also provide other possibilities to visualize the data.

        d_c.get_words_list(num_pages=5, include_heat=True)
        d_c.create_words_table(get_raw_data=True)  

It will output a csv file to material folder. This DataFrame has three columns: word, flag, heat. The heat is the heat of the origin post.

### 3) wg_crawler
It will scrape 10 pages of the website wg_gesucht.de with the filter be set as {Munich, WG}, then get a dataframe which contains information about the WG ans store it in the material folder name as 'The_wg_information_in_munich'.

The DataFrame contains 4 columns: name, link, room_size, price

To use it, just:
        
        from wg_crawler import wg_crawler
        w_c = wg_cralwer()
        w_c.run()

If you want to access the DataFrame:

        the_dataframe = w_c.df

        
#### 3.1 Relationship between room size and price
        
        w_c = wg_crawler()
        w_a = wg_analyse(w_c)   # to analyse the data, we need to first connect analyser to the crawler 
        w_a.size_price()  # It will store a image to material folder, you can set the path. with path='...'
        
The figure will look like:        
![the sample picture](https://i.screenshot.net/xq5w2f4)

## Main contributors:
Apollo1840


## Another folders:

### tutorial
There are some learning material.

A very important tool I often use is Pandas, tutorial about Pandas is in another repo of me: Data-Analysis-Tools

The coming parts are:
⋅⋅* how to login
⋅⋅* how to use req.pull
⋅⋅* more about BeautifulSoup

    
### dummy_websites
There are some simple demonstrations of html5.

### material
Useless. It stores the sample output of the crawlers.


