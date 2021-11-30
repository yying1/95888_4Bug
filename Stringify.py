from ReviewDataCleaning import review_cleaning
from SellersInfo import search

# get review in string format for the product
def stringify(upc, name):
	return search(upc, name), review_cleaning()

def main():
	sellers, reviews = get_review()

if __name__ == "__main__":
	main()