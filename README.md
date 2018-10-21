# Happy-Crawler

There are crawlers made by HC-team. The one I want to introduce you most is the BasicCrawler.

## BasicCrawler introduction

<p align="center"> 
    <img src="https://i.screenshot.net/4wxdjc3" alt="the BC brand" width="200" height="200">
</p>

BasicCrawler is an crawler framework, which can be modified to suit your needs of different web cralwering projects. 

Compare to use requests and BeatifulSoup directly, it has following advantages:

* it has good concealment (harder to be detected and catch)
* it is very convenient for you to deploy multiple tasks. (good for data science projects)
* It has a function which can save webpage source code locally, it is very beneficial for long-term development.

So why not use BasicCrawler for your web crawlering projects?

BasicCrawlerGroup is build on BasicCrawler, which acts like mutiple crawlers working in the same time. 

It is faster, harder to been catch and more stable.

interested? want to have a try? see Navigation channel:

## Navigation

### 1. BasicCrawler -> bc3.py

BasicCrawler(a class) is in bc3.py, to use it, just copy bc3.py to your working directory and:

    from bc3 import BasicCrawler

How to use it, see this on-hand tutorial:

    bc = BasicCrawler()
    url = 'https://www.tripadvisor.com/Restaurants-g187309-Munich_Upper_Bavaria_Bavaria.html'
    soup = bc.run(url)
    print(soup.title)

This program will go to one of the tripadvisor website, and print the title of the website, and save the html file of the web.

Of course, This program does not use the any advantage of BasicCrawler.

As I said, BasicCrawler is convient to deploy multiple tasks, how can we do that? I will explain it in a more complex case. Now, our goal is:

<i>Go to one of the tripadvisor website, and get 5 restaurant names and its rating as csv file.</i>

Assume our colleagues has already prepared the urls on the tripadvisor website for you by BasicCrawler:

    bc = BasicCrawler(safetime=(1,2)) # safetime means the crawler will wait 1 or 2 seconds for next scraping, this will increase the concealment of the crawler
    url = 'https://www.tripadvisor.com/Restaurants-g187309-Munich_Upper_Bavaria_Bavaria.html'
    soup = bc.run(url, save_html=False)
    
    # this part retrieve a list of urls.
    restaurant_anchors = soup.find_all('a', class_='property_title')
    urls = ['https://www.tripadvisor.com/'+anchor['href'] for anchor in restaurant_anchors]

and he has also wroten a bs function for us:

    # define a function to find some element in the soup
    def get_name_rating(soup):
        return [soup.find('h1', class_='fr').text, soup.find('span', class_='overallRating').text]

Our task can be very easy to be solved by BasicCrawler now. 

First just use run to get the soups:

    soups = bc.run(urls[:5]) # here I only want first 5 pages

BasicCrawler will automatically detected that you want multiple soups. 

After we get the soups, we can use python list operation to get the data and use pandas to convert it to dataframe and output it as CSV file.

But in fact, with BasicCrawler, we even have a simplier way. Without getting the soups, just directly use get_df function.

    bc.get_df(urls[:5], get_name_rating)

Down, CSV file will be saved in outputs folder. But this is just one example of how to use BasicCrawler.

In real application case, it will be more complex:

* Sometimes, the website has good sense of anti-crawler, you will not get the same html as you read, because your crawler has been identified as a crawler.
* Sometimes, you dont know when your IP will be baned, so you can not let the programm run overnight task.
* Sometimes, you have huge number of websites to been scrape, you need multiple crawlers work at same time.

But BasicCrawler and BasicCrawlerGroup can solve this problem for you.

If you want to know more about BasicCrawler please go to bc3_tutorial.py.

bc3_testor.py is for our testor to test the functionality and limitness of our BasicCrawler.

### 2. Other crawlers -> projects

In this repository, we also showed some of crawlers we build and some of web crawlering projects we did in projects folder. 

If you like them or want to see more upgrade of them, please press Star at the right up corner, thank you very much!

Or join us !!! 

(contact: 2285664798@qq.com, wechat:zoucongyu1109) 

### 3. Learning material -> tutorial

It has nothing to do with BasicCrawler, just some learning material of how to build a crawler from scrath.

(A very important tool I often use is Pandas, tutorial about Pandas is in another repo of me: Data-Analysis-Tools)

The coming parts are:
* how to login
* how to use req.pull
* more about BeautifulSoup

 
## Other crawlers





## Main contributors:
Apollo1840 (contact: zoucongyu1993@hotmail.com, wechat:zoucongyu1109)

