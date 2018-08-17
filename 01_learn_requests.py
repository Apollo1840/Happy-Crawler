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


##############################################################################
# requests.post
data = {
    'entities_only':'true',
    'page':'2'
}
 
html_post = requests.post(url,data=data)