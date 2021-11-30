#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

### Read the Amazon Review Result
def review_cleaning():
	Data = pd.read_excel("AmazonReviewResult.xlsx", header = 0)
	AZ = pd.DataFrame(Data)
	AZ.dropna(how='all', inplace=True)

	### View the Rating Column
	AZ['rating']
	AZ['rating'] = AZ['rating'].str.replace(' out of 5 stars', '')

	#### Change each rating score to categorical name

	## 1.0 = Hate

	## 2.0 = Do Not Like

	## 3.0 = Okay

	## 4.0 = Like

	## 5.0 = Love

	AZ['rating'] = AZ['rating'].replace(['1.0', '2.0', '3.0', '4.0', '5.0'], ['Hate', 'Do Not Like', 'Okay', 'Like', 'Love'])

	## Do the categorical variables in Count plot

	'''
	plt.figure(figsize=(8,4))
	fig = plt.figure()
	sns.countplot(x = 'rating', data = AZ)
	fig.savefig('Rating.jpg')
	'''

	TS = pd.read_csv("terms.csv", header = 0, names = ['Terms'])

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
	            review_result[3] += 1
	    filtered_list.append(review_result)
	    n+=1

	df_filtered_rev = pd.DataFrame(filtered_list, columns = ['Review', 'Rating', 'Matched Terms', 'Matched Count'])

	AZ2 = df_filtered_rev[df_filtered_rev['Matched Count'] != 0]

	AZ2.to_excel("AmazonReviewMatchResultdrop.xlsx", index = False)

	review_strs = list()

	# convert the dataframe to a list of string
	for index, row in AZ2.iterrows():
		rev_str = f"{row['Rating']}\n\"{row['Review']}\"\n[Matched Words: {row['Matched Terms'].strip()}]"
		review_strs.append(rev_str)

	return review_strs

	'''
	plt.figure(figsize=(20,10))
	fig = plt.figure()

	ax= sns.countplot(x = 'Matched Count', data= TS)

	ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize = 10)
	plt.xlabel("Match", fontsize=15)
	plt.ylabel("Count", fontsize=15)
	plt.tight_layout()
	plt.show()
	fig.savefig('Match.jpg')
	'''

def main():
	for i in review_cleaning():
		print(i)

if __name__ == "__main__":
	main()