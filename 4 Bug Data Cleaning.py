#!/usr/bin/env python
# coding: utf-8

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

### Read the Amazon Review Result

Data = pd.read_excel("AmazonReview.xlsx", header = 0)

AZ = pd.DataFrame(Data)

AZ.head()

AZ.dropna()

AZ.dropna(how='all')

AZ.dropna(inplace=True)

### View the Rating Column

AZ['rating']

AZ['rating'] = AZ['rating'].str.replace(' out of 5 stars', '')

print(AZ['rating'])

#### Change each rating score to categorical name

## 1.0 = Hate

## 2.0 = Do Not Like

## 3.0 = Okay

## 4.0 = Like

## 5.0 = Love

AZ['rating'] = AZ['rating'].replace(['1.0', '2.0', '3.0', '4.0', '5.0'], ['Hate', 'Do Not Like', 'Okay', 'Like', 'Love'])

print(AZ['rating'])

AZ['rating'].value_counts()

## Do the categorical variables in Count plot

plt.figure(figsize=(8,4))

fig = plt.figure()

sns.countplot(x = 'rating', data= AZ)

fig.savefig('Rating.jpg')

AZ["review"]

TS = pd.read_csv("terms.csv", header = 0)

TS.head()

## Change all to the lower case and turn to list for iterationi

# Change all to lower case and turn to list for iteration
TS['Terms'] = TS['Terms'].str.lower()
AZ['review']= AZ['review'].str.lower()
term_list_low = TS['Terms'].tolist()
all_reviews = AZ['review'].tolist()
all_ratings = AZ['rating'].tolist()

#create a list of list to keep track of the review text, rating, matched term and matched count
filtered_list = []
n = 0
for review in all_reviews:
    review_result = [review,all_ratings[n],"",0]
    for term in term_list_low:
        if term in review:
            review_result[2] = review_result[2].strip()+" "+term
            review_result[3] +=1
    filtered_list.append(review_result)
    n+=1

df_filtered_rev = pd.DataFrame(filtered_list, columns = ['Review', 'Rating', 'Matched Terms', 'Matched Count'])
df_filtered_rev.to_excel("AmazonReviewMatchResult.xlsx", index = False)

Data2 = pd.read_excel("AmazonReviewMatchResult.xlsx")

AZ2 = pd.DataFrame(Data2)

print(AZ2.head())

AZ2.isnull()

AZ2 = AZ2.dropna()

AZ2.head()

AZ2.to_excel("AmazonReviewMatchResultdrop.xlsx", index = False)

AZ2['Matched Terms'].value_counts

plt.figure(figsize=(20,10))
fig = plt.figure()

ax= sns.countplot(x = 'Match', data= TS)


ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize = 10)
plt.xlabel("Match", fontsize=15)
plt.ylabel("Count", fontsize=15)
plt.tight_layout()
plt.show()
fig.savefig('Match.jpg')
