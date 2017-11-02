# -*- coding: utf-8 -*-
"""
Scraping part details from Amazon.com
"""

from tkinter import *
from tkinter import ttk
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def search_terms_split(search_string_list):
    ls = search_string_list.split(sep = ',')
    lr = [each.strip() for each in ls]
    s = list(set(lr))
    if s.__contains__(''):
        s.remove('')
    return s

def query_widget():
       def fn_search(*args):
           try:
               val = str(query.get())
               query_string.set(val)
               time.sleep(1)
               root.destroy()
               return val
           except ValueError:
                   pass
       root = Tk()
       root.title("Amazon_POC")
       mainframe = ttk.Frame(root, padding="3 3 12 12")
       mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
       mainframe.columnconfigure(0, weight=1)
       mainframe.rowconfigure(0, weight=1)
       query = StringVar()
       query_string = StringVar()
       query_entry = ttk.Entry(mainframe, width=50, textvariable=query)
       query_entry.grid(column=2, row=1, sticky=(W, E))
       button_title = "search and quit"
       ttk.Button(mainframe, text=button_title, command=fn_search).grid(column=3, row=3, sticky=W)
       query_entry.focus()
       root.bind('<Return>', fn_search)
       root.mainloop()
       query_string_var = query_string.get()
       return query_string_var


def data_for_list_of_parts(search_string):  
    # returns data for one search string
    def get_soup(url_in):   # returns the soup of the webpage
        page = requests.get(url_in)
        soup = BeautifulSoup(page.content,"html.parser")
        return soup
    def search_yield(search_string):    # returns list of ASINs if search returns results, else None
        url_base = "https://www.amazon.com/s/url=search-alias%3Daps&field-keywords="
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
        url_base = "https://www.amazon.com/s/?url=search-alias%3Daps&field-keywords="
        #keyword = "WR23X10179"
        page_url, search_result_asins = url_base + keyword, []
        soup = get_soup(page_url)
        search_page_results = soup.find_all('li', {'class':'s-result-item celwidget '})
        for each in search_page_results:
            search_result_asins.append(each['data-asin'])
        return search_result_asins
    def create_url(ASIN,page_no = 1, increment = 10):   #returns the first page of the ASIN search results
        base, ref, utf, index = "https://www.amazon.com/gp/offer-listing/", "/ref=olp_page_", "?ie=UTF8&startIndex=", (page_no -1) * increment
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
    
    ASIN_list = search_yield(search_string)
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
            dict_product_info[each] = pd.DataFrame({'Sellers':sellers,'Prices':prices,'ASIN_Number':each})

    return dict_product_info

## end of main function
search_string_list = query_widget()
search_list = search_terms_split(search_string_list)    #search_list should be used for tab names

filename = "Data_amazon_com"
file_format = '.xlsx'
writer = pd.ExcelWriter(filename + file_format, engine='xlsxwriter')

for e in search_list:
    search_data = data_for_list_of_parts(e)
    print(e)
    print(search_data)
    if not any(search_data):
        print("No result")
    i = 0
    for each in search_data:
        search_data[each].to_excel(writer, sheet_name = e,startcol = i)
        i += 4
writer.save()
    
#file = "D:/Users/Public/Documents/Python Scripts/" + filename + file_format
#os.startfile(file)

