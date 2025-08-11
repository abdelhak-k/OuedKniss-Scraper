"""
NOTE: please read README.md  carefully before proceeding.
"""

API_URL = "https://api.ouedkniss.com/graphql"
HEADER = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}
COUNT= 60 # Number of items per page (can't be increased that's the maximum for one page), can be decreased
TRIES=3 # Retry attempts for failed requests
WAIT_TIME_RETRY=3 # seconds we wait between retries
WAIT_TIME= 0.2 # seconds between requests (recommended: 0.2 to avoid overwhelming API)

# NOTE: you can change if you're intrested in all the features got from the API or only a portion of it
TYPE= "MINI" # you can change it to "ALL" / or create new set of features you're intrested in
# GO to process.py and utils.py if you want specific features, change it at your own responsibility