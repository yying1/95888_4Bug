#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.client, urllib.request, urllib.parse, urllib.error, json
from bs4 import BeautifulSoup as bs
import requests

# API keys for the following api calls
API_KEY = "f946662395f94c73ac066c940f8fe796"

# search a list of sellers by product upc
def search(upc, name):

    # include headers and api call params
    headers = {
        'ApiGenius_API_Key': API_KEY,
    }
    
    params = urllib.parse.urlencode({
        'upc': upc,
        'api_key': '{}',
    })
    
    # connect to api and return a dict of sellers
    try:
        conn = http.client.HTTPSConnection('api.apigenius.io')
        conn.request("GET", "/products/lookup?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        
        # handle empty upc or empty results
        try:
            data = clean_seller_data(data["items"]["pricing"])
            return data
        except Exception as e:
            return searchByName(name)
            
    except Exception as e:
        print(e)
    
    return ""
        
# search a list of sellers by product name
def searchByName(name):

    # include headers and api call params
    headers = {
        'ApiGenius_API_Key': API_KEY,
    }
    
    params = urllib.parse.urlencode({
        'keyword': name,
        'title': '',
        'mpn': '',
        'category': '',
        'brand': '',
        'api_key': '',
    })
    
    # connect to api and return a dict of sellers
    try:
        conn = http.client.HTTPSConnection('api.apigenius.io')
        conn.request("GET", "/products/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        return clean_seller_data(data["items"]["pricing"])
    except Exception as e:
        print(e)
    
    return ""

# take in a list of dict repsents different sellers and return only the valid ones in string format
# Validate sellers data by checking if the product is in stock and if its a U.S. seller
def clean_seller_data(sellers):
    clean_dta = list()
    for seller in sellers:
        # Game Stop does not have 404 page but does not allow scrapping
        if "GameStop" in seller["seller"]:
            clean_dta.append(seller)
            continue
        if "ca" in seller["seller"] or "CAD" in seller["currency"] or "CAD" in seller["shipping"] or "GBP" in seller["currency"]:
            continue
        page = requests.get(seller["link"])
        soup = bs(page.text, "html.parser")

        count = 0
        for r in soup.find_all("p") + soup.find_all("div"):
            if "$" in r.getText():
                count += 1
                break;

        if count == 0:
            continue

        clean_dta.append(seller)

    return to_string(clean_dta)

# take in a list dict objects represents sellers and output a list of string
def to_string(dta):
    data_str = list()
    for d in dta:
        data_str.append(f"{d['title']}\nFrom: {d['seller']}\nURL: {d['link']}\nPrice: {d['price']}")
    return data_str

        
def main():
    data = search("194252590362")

    for d in clean_seller_data(data):
        print(d)

if __name__ == "__main__":
    main()