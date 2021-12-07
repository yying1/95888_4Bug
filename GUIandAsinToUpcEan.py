#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter as tk

from tkinter.scrolledtext import ScrolledText
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re
import requests
from requests.structures import CaseInsensitiveDict
import http.client, urllib.request, urllib.parse, urllib.error, base64
from ReviewDataCleaning import review_cleaning
from SellersInfo import search
from CheckAmazonReview import get_name

class MainWindow:
    def __init__(self, window):
        self.lbl = Label(window, text="Amazon URL here: ")
        self.lbl.pack(ipadx = 10, ipady = 10, fill = 'x')
        
        self.txtfld = Entry(window)
        self.txtfld.pack(ipadx = 10, ipady = 10, fill = 'x')
        
        self.btn = Button(window, text = "Show Recommendations", command = self.checkValid)
        self.btn.pack(ipadx = 10, ipady = 10, fill = 'x')
        
        self.message = Label(window, text = "")
        self.message.pack(ipadx = 10, ipady = 10, fill = 'x')
                
        self.recommends = ScrolledText(
            master = window, 
            wrap = WORD,
            height = 5
        )
        
        self.reviews = ScrolledText(
            master = window, 
            wrap = WORD,
        )
                
    # Check if input URL is valid
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
    
    # Get product ASIN
    def getAsin(self, url):
        asin = re.search(r'/[dg]p/([^/?]+)', url, flags=re.IGNORECASE)
        if asin:
            print(asin.group(1))
            myMessage = "ASIN: " + asin.group(1)
            self.message.config(text = myMessage)
            self.stringify(asin.group(1))
        else:
            self.message.config(text = "Input url is not valid")
    
    # Get product UPC and EAN
    def getAPI(self, asin):
        url = "https://v3.synccentric.com/api/v3/products/search"

        headers = CaseInsensitiveDict()
        headers["Authorization"] = "Bearer sIFe5XuTMF3k3gCYNx3iQvYd11r79oBmqkMUJ8Jba5qHocDYa61FAduCNYu0"
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        
        data = "identifier[]=" + asin + "&type=asin&locale=US&fields[]=asin&fields[]=upc&fields[]=ean"
        
        resp = requests.post(url, headers=headers, data=data)
        
        jsonResponse = resp.json()
        if "errors" in jsonResponse:
            upc = ""
            ean = ""
        else:
            upc = jsonResponse['data'][0]['attributes']['upc']
            ean = jsonResponse['data'][0]['attributes']['ean']
        
        return upc, ean

    # Get sellers and reviews information in string format for final output
    def stringify(self, asin):
        upc, ean = self.getAPI(asin)
        name = get_name(asin)

        sellers = "No Alternative Sellers Available"
        reviews = "No Reviews Available Online"

        sellers_data = search(upc, name)
        reviews_data = review_cleaning(asin)
        
        if len(sellers_data) == 0:
            for s in sellers_data:
                sellers += s + "\n\n"

        if len(reviews_data) == 0:
            for r in reviews_data:
                reviews += r + "\n\n"
        
        self.recommends.delete('1.0', 'end')
        self.recommends.insert('end', sellers)
        self.recommends.pack(expand = Y, fill = BOTH)
        self.recommends.update()
        
        self.reviews.configure(state = 'normal')
        self.reviews.delete('1.0', 'end')
        self.reviews.insert('end', reviews)
        self.reviews.pack(expand = Y, fill = BOTH)
        self.reviews.update()
        self.reviews.configure(state = 'disabled')
        
window = tk.Tk()
myWindow = MainWindow(window)
window.title('Electronics Recommender')
window.geometry("1200x800")
window.mainloop()
