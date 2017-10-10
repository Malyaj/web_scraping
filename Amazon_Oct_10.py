# -*- coding: utf-8 -*-
"""
Scraping part details from Amazon.in
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_soup(url_in):   # returns the soup of the webpage
    page = requests.get(url_in)
    soup = BeautifulSoup(page.content,"html.parser")
    return soup

def search_yield(search_string):    # returns list of ASINs if search returns results, else None
    url_base = "https://www.amazon.in/s/url=search-alias%3Daps&field-keywords="
    page_url = url_base + search_string
    soup = get_soup(page_url)
    noResultsTitle = "noResultsTitle"
    try:
        no_result_tag = soup.find('h1', {'id':'noResultsTitle'})
        no_result_set = no_result_tag['id']
        if noResultsTitle in no_result_set:
            #return False
            return None
    except TypeError:
        #return True    # i.e. we have results, now extract the ASINs of the results
        ASIN_list = search_page_results(search_string)
        return ASIN_list

def search_page_results(keyword):   # returns the list of ASINs for a search query
    url_base = "https://www.amazon.in/s/?url=search-alias%3Daps&field-keywords="
    #keyword = "WR23X10179"
    page_url, search_result_asins = url_base + keyword, []
    soup = get_soup(page_url)
    search_page_results = soup.find_all('li', {'class':'s-result-item celwidget '})
    for each in search_page_results:
        search_result_asins.append(each['data-asin'])
    return search_result_asins

def create_url(ASIN,page_no = 1, increment = 10):   #returns the first page of the ASIN search results
    base, ref, utf, index = "https://www.amazon.in/gp/offer-listing/", "/ref=olp_page_", "?ie=UTF8&startIndex=", (page_no -1) * increment
    url = base + ASIN + ref + str(page_no) + utf + str(index)
    return url
    
def next_page(url_in, increment = 10):  #returns the url of the next page
    len_base, len_ASIN, len_ref = 39, 10, 14
    ASIN = url_in[len_base: len_base + len_ASIN]
    first = url_in.split("?")[0]
    page = int(first[len_base + len_ASIN + len_ref:]) + 1
    ind = (page - 1) * increment
    url_out = create_url(ASIN, page_no = page, index = ind)
    return url_out

def is_last_page(page_url):    #returns True if the page is last one, else False
    soup = get_soup(page_url)
    disabled_label, a_last = 'a-disabled', 'a-last'
    try:
        active_tag = soup.find('li',{'class':'a-last'})
        classes_active_tag = set(active_tag['class'])
        if disabled_label in classes_active_tag:
            return True
        elif a_last in classes_active_tag:
            return False
    except TypeError:
        return True

def get_data_from_page(url_page):   # returns the seller info and prices for one page ( for one ASIN)
    soup = get_soup(url_page)
    page_seller, page_price = [], []
    #page_seller
    all_h3_tags = soup.find_all('h3', {'class':'a-spacing-none olpSellerName'})
    for i in all_h3_tags:
        seller_info = i.text.strip()
        page_seller.append(seller_info)
    # Price
    all_span_price = soup.find_all('span', {'class':'a-size-large a-color-price olpOfferPrice a-text-bold'})
    for each_tag in all_span_price:
        price_info = each_tag.text.strip()
        page_price.append(price_info)
    return(page_seller, page_price)

#




### testing
search_string = 'WR23X10179'
#search_string = 'jkghjldlkfnadklgn'
ASIN_list = search_yield(search_string)
#print(ASIN_list)


dict_product_info = {}

if ASIN_list == None:
    print("No result for " + search_string)
else:
    for each in ASIN_list:
        sellers, prices = [], []
        continue_flag, page = True, create_url(each)
        while continue_flag == True:
            s, p = get_data_from_page(page)
            sellers += s
            prices += p
            if is_last_page(page):
                continue_flag = False
            else:
                continue_flag = True
                page = next_page(page)
        dict_product_info[each] = pd.DataFrame({'Sellers':sellers,'Prices':prices})














