# -*- coding: utf-8 -*-
import requests

# basics
url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&ch=&tn=baidu&bar=&wd=html&rn=&oq=&rsv_pq=ed3c5435000349e3&rsv_t=e124zMH%2FO8QNEKqaXYH3v8lLRXS3Ytyx2Jv63lNR6jgnvr301RnYxXiWPIg&rqlang=cn'
response = requests.get(url)
print(response.text)

# sometimes it will get different html in browser
 
# header make the surver believes the action is from browser
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
 
response = requests.get(url,headers = hea)
 
response.encoding = 'utf-8' # admit chinese
print(response.text)

if response.status_code == 200:
    print('successful!')
elif response.status_code == 404:
    print('not found!')
    

# proxy
proxies = { "http": "http://10.10.1.10:3128", "https": "http://10.10.1.10:1080"} 
requests.get("http://example.org", proxies=proxies)



import urllib
def spider_proxy():
    proxy_url = 'https://proxyapi.mimvp.com/api/fetchopen.php?orderid=867060048322190715&num=20&result_fields=1,2'
    req = urllib.request.Request(proxy_url)
    content = urllib.request.urlopen(req, timeout=30).read()
    proxy_list = content.decode().split("\n")
    
    return proxy_list

proxylist = spider_proxy()



def modify_for_requests(proxy, include_none_https = True, include_only_https = True):
    mark =str.strip(proxy.split(',')[1])    
    if mark == 'HTTP' and include_none_https:
        return { "http": 'http://' + proxy.split(',')[0]}
    elif mark == 'HTTPS' and include_only_https:
        return { 'https': 'http://' + proxy.split(',')[0]}
    elif mark == 'HTTP/HTTPS':
        return { "http": 'http://' + proxy.split(',')[0], 'https': 'http://' + proxy.split(',')[0]}
    

for proxy in proxylist:
        print(modify_for_requests(proxy))      



##############################################################################
# requests.post
data = {
    'entities_only':'true',
    'page':'2'
}
 
html_post = requests.post(url,data=data)