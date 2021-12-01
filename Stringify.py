from ReviewDataCleaning import review_cleaning
from SellersInfo import search
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import re
import requests, json
from requests.structures import CaseInsensitiveDict
import http.client, urllib.request, urllib.parse, urllib.error, base64
from ReviewDataCleaning import review_cleaning
from SellersInfo import search
from CheckAmazonReview import get_name

# get review in string format for the product
def stringify(asin):
    upc, ean = getAPI(asin)
    name = get_name(asin)
    print(name)
    return search(upc, name), review_cleaning(asin)

def getAPI(asin):
    url = "https://v3.synccentric.com/api/v3/products/search"

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer sIFe5XuTMF3k3gCYNx3iQvYd11r79oBmqkMUJ8Jba5qHocDYa61FAduCNYu0"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    
    data = "identifier[]=" + asin + "&type=asin&locale=US&fields[]=asin&fields[]=upc&fields[]=ean"
    
    resp = requests.post(url, headers=headers, data=data)
    
    jsonResponse = resp.json()
    upc = jsonResponse['data'][0]['attributes']['upc']
    ean = jsonResponse['data'][0]['attributes']['ean']
    
    print("upc: " + upc)
    print("ean: " + ean)
    
    return upc, ean

def main():
	sellers, reviews = stringify("B08N5KWB9H")
	for s in sellers:
		print(s)

	print("=====================================================")

	for r in reviews:
		print(r)

if __name__ == "__main__":
	main()