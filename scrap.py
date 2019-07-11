from selenium import webdriver

from bs4 import BeautifulSoup as bs4
import re
from urllib2 import urlopen

import json
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np


username='sunithadevadas'
browser = webdriver.Chrome('./chromedriver')
browser.get('https://www.instagram.com/'+username)
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

links=[]
source = browser.page_source
data=bs4(source, 'html.parser')
body = data.find('body')
script = body.find('span')
for link in script.findAll('a'):
     if re.match("/p", link.get('href')):
        links.append('https://www.instagram.com'+link.get('href'))

result=pd.DataFrame()
for i in range(len(links)):
    try:
        printf("working")
        page = urlopen(links[i]).read()
        data=bs4(page, 'html.parser')
        body = data.find('body')
        script = body.find('script')
        raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
        json_data=json.loads(raw)
        posts =json_data['entry_data']['PostPage'][0]['graphql']
        posts= json.dumps(posts)
        posts = json.loads(posts)
        x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
        x.columns =  x.columns.str.replace("shortcode_media.", "")
        result=result.append(x)
       
    except:
        np.nan

result = result.drop_duplicates(subset = 'shortcode')
result.index = range(len(result.index))







import os
import requests
result.index = range(len(result.index))
directory="a"
for i in range(len(result)):
    r = requests.get(result['display_url'][i])
    with open(directory+result['shortcode'][i]+".jpg", 'wb') as f:
                    f.write(r.content)





