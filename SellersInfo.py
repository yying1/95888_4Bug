#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.client, urllib.request, urllib.parse, urllib.error, json
from bs4 import BeautifulSoup as bs
import requests

API_KEY = "4db2a75e63df4a1fb66f380105e4589b"

# search a list of sellers by product upc
def searchById(upc):

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
        
        return data["items"]["pricing"]
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
        print(data)
        return data["items"]["pricing"]
    except Exception as e:
        print(e)
    
    return ""

# take in a list of dict repsents different sellers and return only the valid ones
def clean_seller_data(sellers):
    clean_dta = list()
    for seller in sellers:
        if "ca" in seller["seller"] or "CAD" in seller["currency"] or "CAD" in seller["shipping"] or "GBP" in seller["currency"]:
            continue
        page = requests.get(seller["link"])
        soup = bs(page.text, "html.parser")

        price = "{:,.2f}".format(seller["price"])
        count = 0
        for r in soup.find_all("p") + soup.find_all("div"):
            if "$" in r.getText():
                count += 1

        if count == 0:
            continue
        
        """
        if (len(soup(text="not found")) > 0 or len(soup(text="404")) > 0 or len(soup(text="not be found")) or  len(soup(text="PROBLEM")) > 0
            or len(soup(text="find the page")) or len(soup(text="no longer"))) > 0:
            continue
        """

        clean_dta.append(seller)

    return clean_dta



        
def main():
    data = searchById("194252165959")

    for d in clean_seller_data(data):
        print(d)

    """
    data = searchByName("Fire TV Stick with Alexa Voice Remote (includes TV controls), HD streaming device")
    for d in data:
        print(d)
    """

if __name__ == "__main__":
    main()