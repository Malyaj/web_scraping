#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time
import random
import urllib.request
import os


url = "https://other-wordly.tumblr.com/"
location = r"D:\Users\703143501\Downloads"
os.chdir(location)



def get_soup(url_in):   # returns the soup of the webpage
    page = requests.get(url_in)
    soup = BeautifulSoup(page.content,"html.parser")
    return soup

### a shorter alternative
def get_soup(url):
    '''return the soup of a url'''
    return BeautifulSoup(requests.get(url).content, 'html.parser')


def timeit(function):
    def timed(*args, **kw):
        ts = time.time()
        result = function(*args, **kw)
        te = time.time()
        print(f"Time elapsed: {round(te-ts)} seconds to run function {function.__name__} with arguments: {args}")
        #print(f"Function: {function.__name__} Time elapsed: {te-ts} seconds")
        return result
    return timed


@timeit
def get_soup(url):
    '''return the soup of a url'''
    return BeautifulSoup(requests.get(url).content, 'html.parser')


soup = get_soup(url)


all_image_tags = soup.find_all('img')


#all_image_tags[0].get_attribute_list('src')
#[x for x in dir(all_image_tags[0]) if 'attr' in x]
all_image_tags[0].attrs.get('src')


@timeit
def download_image(url, name, format = 'jpg'):
    #name = random.randrange(1,100)
    fullname = '.'.join([name, format])
    urllib.request.urlretrieve(url,fullname)


download_urls = [e.attrs.get('src') for e in all_image_tags]
names = ['img_' + str(i).rjust(4, '0') for i in range(len(download_urls))]


for url, name in zip(download_urls, names):
    try:
        download_image(url, name)
        print(f"Image {name} downloaded succesfully!")
    except:
        print(f"Image {name} NOT downloaded, skipping ahead ....")
