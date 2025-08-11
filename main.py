from scraper import scrape_ouedkniss

"""
NOTE: please read README.md  carefully before proceeding.
"""
if __name__ == "__main__":
    # example on how to run:
    result = scrape_ouedkniss(category_slug="informatique-ordinateur-portable", max_pages=10)
    #result = scrape_ouedkniss(category_slug="informatique-ordinateur-portable", max_pages=None)
    
    # max_pages=None will return the maximum possible number of pages
    print(f"Data saved to: {result}")
