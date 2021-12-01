#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 18:22:35 2021

@author: jchao
"""

from tkinter import *
from tkinter.scrolledtext import ScrolledText
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re
import requests, json
from requests.structures import CaseInsensitiveDict
import http.client, urllib.request, urllib.parse, urllib.error, base64
from ReviewDataCleaning import review_cleaning
from SellersInfo import search
from CheckAmazonReview import get_name

class MainWindow:
    def __init__(self, win):
        self.lbl = Label(window, text="Amazon URL here: ")
        #self.lbl.place(x = 340, y = 20)
        self.lbl.pack(ipadx = 10, ipady = 10, fill = 'x')
        
        self.txtfld = Entry(window)
        #self.txtfld.place(x = 300, y = 40)
        self.txtfld.pack(ipadx = 10, ipady = 10, fill = 'x')
        
        self.btn = Button(window, text = "Show Recommendations", command = self.checkValid)
        #self.btn.place(x = 300, y = 80)
        self.btn.pack(ipadx = 10, ipady = 10, fill = 'x')
        
        self.message = Label(window, text = "")
        #self.message.place(x = 340, y = 120)
        self.message.pack(ipadx = 10, ipady = 10, fill = 'x')
        
        self.recommends = ScrolledText(window, width = 800)
        self.recommends.pack(ipadx = 10, ipady = 10)
        self.recommends.insert(INSERT, """\
        This is a scrolledtext widget to make tkinter text read only.
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        """)
        self.recommends.configure(state = 'disabled')
        
        self.reviews = ScrolledText(window, width = 800)
        self.reviews.pack(ipadx = 10, ipady = 10)
        self.reviews.insert(INSERT, """\
        This is a scrolledtext widget to make tkinter text read only.
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        Test
        """)
        self.reviews.configure(state = 'disabled')
                
    def checkValid(self):
        url = self.txtfld.get()
        validate = URLValidator()
        try:
            validate(url)
            print("Valid url")
            self.getAsin(url)
        except ValidationError as exception:
            print("Input url is not valid")
            self.message.config(text = "Input url is not valid")
    
    def getAsin(self, url):
        asin = re.search(r'/[dg]p/([^/?]+)', url, flags=re.IGNORECASE)
        if asin:
            print(asin.group(1))
            myMessage = "ASIN: " + asin.group(1)
            self.message.config(text = myMessage)
            self.getAPI(asin.group(1))
        else:
            self.message.config(text = "Input url is not valid")
            
    def getAPI(self, asin):
        url = "https://v3.synccentric.com/api/v3/products/search"

        headers = CaseInsensitiveDict()
        headers["Authorization"] = "Bearer sIFe5XuTMF3k3gCYNx3iQvYd11r79oBmqkMUJ8Jba5qHocDYa61FAduCNYu0"
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        
        data = "identifier[]=" + asin + "&type=asin&locale=US&fields[]=asin&fields[]=upc&fields[]=ean"
        
        resp = requests.post(url, headers=headers, data=data)
        
        jsonResponse = resp.json()
        upc = jsonResponse['data'][0]['attributes']['upc']
        ean = jsonResponse['data'][0]['attributes']['ean']
        
        return upc, ean

    # get review in string format for the product
    def stringify(self, asin):
        upc, ean = getAPI(asin)
        name = get_name(asin)
        return search(upc, name), review_cleaning(asin)

    #sIFe5XuTMF3k3gCYNx3iQvYd11r79oBmqkMUJ8Jba5qHocDYa61FAduCNYu0        

window = Tk()
myWindow = MainWindow(window)
window.title('Electronics Recommender')
window.geometry("800x800")
window.mainloop()