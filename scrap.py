import os
import re
import requests
import json
import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen
from pandas.io.json import json_normalize
import time
import urllib

username =str(input("Enter your username    :"))
passwd = str(input("Enter your password     : "))
target = str(input("Enter target username   :"))
os.mkdir(target)
browser = webdriver.Chrome('./chromedriver')
browser.get('https://www.instagram.com/')
time.sleep(3)
browser.find_element_by_name("username").send_keys(username)
browser.find_element_by_name("password").send_keys(passwd)
time.sleep(3)
browser.find_element_by_css_selector(".sqdOP.L3NKy.y3zKF").click()
time.sleep(3)
browser.find_element_by_css_selector(".sqdOP.yWX7d.y3zKF").click()
time.sleep(3)
browser.find_element_by_css_selector(".aOOlW.HoLwm").click()
time.sleep(2)
browser.get('https://www.instagram.com/'+target)
time.sleep(3)
last_height = browser.execute_script("return document.body.scrollHeight")
print("Scrolling")
links=[]
while True:
    # Scroll down to the bottom.
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load the page.
    time.sleep(3)
    # Calculate new scroll height and compare with last scroll height.
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
    # Finding all the posts in specified user

    source = browser.page_source
    data=bs4(source, 'html.parser')
    body = data.find('body')
    mydiv = body.find("div", {"class": "_2z6nI"})
    for link in mydiv.findAll('a'):
        if re.match("/p", link.get('href')):
            links.append('https://www.instagram.com'+link.get('href'))
links = list(dict.fromkeys(links))
print("saving all images")
#Saving the post
j = 0
for link in links:
    j = j + 1
    browser.get(link)
    time.sleep(3)
    source = browser.page_source
    data=bs4(source, 'html.parser')
    body = data.find('body')
    
    try:
        filename = target+"/"+str(j)+".jpg"
        mydiv = body.find("img", {"class": "FFVAD"})
        s = str(mydiv)
        a = re.findall('https(.+)1080w',s)
        st = str(a).split(",")[2]
        link = st[:len(st)-3]
        link = link.replace("&amp;","&")
    except:
        filename = target+"/"+str(j)+".mp4"
        mydiv = body.find("video", {"class": "tWeCl"})
        s = str(mydiv)
        a = re.findall('https(.+)" ',s)
        a = str(a).split('src="')[1]
        a = a[:len(a)-2]
        a = a.replace("&amp;","&")
    else:
        pass
        
    urllib.request.urlretrieve(link, filename)
print("Number of post save : ",j)





