import os
import re
import requests
import json
import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup as bs4
from urllib2 import urlopen
from pandas.io.json import json_normalize



username=raw_input("Enter the username of the profile you need : ")

# The path for the Browser was specified , I used the chrome driver for the linux
browser = webdriver.Chrome('./chromedriver')
browser.get('https://www.instagram.com/'+username)
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Finding all the posts in specified user
links=[]
source = browser.page_source
data=bs4(source, 'html.parser')
body = data.find('body')
script = body.find('span')
for link in script.findAll('a'):
    if re.match("/p", link.get('href')):
        links.append('https://www.instagram.com'+link.get('href'))

# For each post we scrap the image and store in a dataframe
result=pd.DataFrame()
for i in range(len(links)):
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

result = result.drop_duplicates(subset = 'shortcode')
result.index = range(len(result.index))

# Save image as an jpeg image file

for i in range(len(result)):
    r = requests.get(result['display_url'][i])
    with open(username+result['shortcode'][i]+".jpg", 'wb') as f:
        f.write(r.content)





