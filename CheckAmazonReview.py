#!/usr/bin/env python
# coding: utf-8
#Name: Frank Yue Ying
#Date: 2021-12-04
import requests
from bs4 import BeautifulSoup
import pandas as pd

## Note: this script extracts US customer reviews from the ASIN's review page on Amazon.Input is the URL string. Replace "B07JGL19WK" with the target ASIN. A Excel file named "AmazonReviewResult" will aslo be produced at the end.

#get_soup extract the html content from the amazon review site such as https://www.amazon.com/product-reviews/B07JGL19WK/?ie=UTF8&reviewerType=all_reviews&pageNumber=1
def get_soup(url,HEADERS):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

#get_reviews analyze the soup html text and identify each review through div tag, then extract keep elements from each review including title,date,rating and the review content as a dictionary. Finally append it to all_reviews
def get_reviews(soup,all_reviews):
    reviews = soup.find_all("div",{'data-hook':'review'})

    try: 
        for item in reviews: 
            review = {
            "title": item.find("a",{'data-hook':'review-title'}).text.strip(),
            "date": item.find("span",{'data-hook':'review-date'}).text.strip(),
            "rating": item.find("i",{'data-hook':'review-star-rating'}).text.strip(),
            "review": item.find("span",{'data-hook':'review-body'}).text.strip()
            }
            all_reviews.append(review)
    except:
        pass

#Main function to be called to extract reviews
def main_checkAmazonReview(ASIN = "B07PXGQC1Q"):
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/90.0.4430.212 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

    #List variable all_reviews will keep all of the reviews scraped for the product (including all pages)
    all_reviews= []
    #use a range loop to extract first 10 pages of review content, each page should have 10 reviews. Reviews from other countries will be ignored. It will auto-stop at the last page
    for x in range(1,11):
        soup= get_soup(f"https://www.amazon.com/product-reviews/{ASIN}/?ie=UTF8&reviewerType=all_reviews&pageNumber={x}",HEADERS)
        get_reviews(soup,all_reviews)
        if not soup.find("li",{'class':'a-disabled a-last'}):
            pass
        else:
            break

    df = pd.DataFrame(all_reviews)
    df.to_excel("AmazonReviewResult.xlsx",index = False)

    return df

#Function to get ASIN name
def get_name(ASIN = "B07PXGQC1Q"):
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/90.0.4430.212 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
    soup= get_soup(f"https://www.amazon.com/product-reviews/{ASIN}/?ie=UTF8&reviewerType=all_reviews",HEADERS)
    name = soup.find("a",{'data-hook':'product-link'}).text.strip()
    return name

if __name__ == "__main__":
    main_checkAmazonReview()
    print( get_name())
