from ReviewDataCleaning import review_cleaning
from SellersInfo import searchById, searchByName

# get review in string format for the product
def get_review():
	return review_cleaning()

def main():
	get_review()

if __name__ == "__main__":
	main()