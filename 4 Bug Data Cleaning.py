#!/usr/bin/env python
# coding: utf-8

# In[17]:


import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns


# In[18]:


### Read the Amazon Review Result

Data = pd.read_excel("AmazonReview.xlsx", header = 0)

AZ = pd.DataFrame(Data)


# In[19]:


AZ.head()


# In[20]:


AZ.dropna()


# In[21]:


AZ.dropna(how='all')


# In[22]:


AZ.dropna(inplace=True)


# In[23]:


### View the Rating Column

AZ['rating']


# In[24]:


AZ['rating'] = AZ['rating'].str.replace(' out of 5 stars', '')

print(AZ['rating'])


# In[25]:


#### Change each rating score to categorical name

## 1.0 = Hate

## 2.0 = Do Not Like

## 3.0 = Okay

## 4.0 = Like

## 5.0 = Love

AZ['rating'] = AZ['rating'].replace(['1.0', '2.0', '3.0', '4.0', '5.0'], ['Hate', 'Do Not Like', 'Okay', 'Like', 'Love'])

print(AZ['rating'])


# In[26]:


AZ['rating'].value_counts()


# In[27]:


## Do the categorical variables in Count plot

plt.figure(figsize=(8,4))

fig = plt.figure()

sns.countplot(x = 'rating', data= AZ)

fig.savefig('Rating.jpg')


# In[28]:


AZ["review"]


# In[29]:


TS = pd.read_csv("terms.csv", header = 0)

TS.head()


# In[30]:


## Change all to the lower case and turn to list for iterationi

# Change all to lower case and turn to list for iteration
TS['Terms'] = TS['Terms'].str.lower()
AZ['review']= AZ['review'].str.lower()
term_list_low = TS['Terms'].tolist()
all_reviews = AZ['review'].tolist()
all_ratings = AZ['rating'].tolist()


# In[31]:


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


# In[33]:


df_filtered_rev = pd.DataFrame(filtered_list, columns = ['Review', 'Rating', 'Matched Terms', 'Matched Count'])
df_filtered_rev.to_excel("AmazonReviewMatchResult.xlsx", index = False)


# In[35]:


Data2 = pd.read_excel("AmazonReviewMatchResult.xlsx")

AZ2 = pd.DataFrame(Data2)


# In[37]:


print(AZ2.head())


# In[38]:


AZ2.isnull()


# In[39]:


AZ2 = AZ2.dropna()


# In[41]:


AZ2.head()


# In[26]:


AZ2.to_excel("AmazonReviewMatchResultdrop.xlsx", index = False)


# In[44]:


AZ2['Matched Terms'].value_counts


# In[61]:


plt.figure(figsize=(20,10))
fig = plt.figure()

ax= sns.countplot(x = 'Match', data= TS)


ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize = 10)
plt.xlabel("Match", fontsize=15)
plt.ylabel("Count", fontsize=15)
plt.tight_layout()
plt.show()
fig.savefig('Match.jpg')


# In[ ]:





# In[ ]:




