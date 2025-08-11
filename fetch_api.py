import requests
import time
from settings import *
from utils import get_payload_search

if TYPE=="MINI":
    from utils import get_payload_post_mini as get_payload_post
else:
    from utils import get_payload_post_all as get_payload_post

class OuedKnissAPI:
    def __init__(self):
        self.api_url = API_URL
        self.headers = HEADER


    def get_announcement_ids_from_pages(self, category_slug, max_pages=None):
        """        
        max_pages: Maximum number of pages to scrape (None = all pages)
        """
        if not max_pages:
            payload = get_payload_search(category_slug, 1)
            try:
                response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=30)
                paginator = response.json()["data"]["search"]["announcements"]["paginatorInfo"]
                max_pages = paginator.get("lastPage", 1)
                # the api returns the lastPage, which can be used to indicate the max_pages we can fetch
            except Exception as e:
                print("could not fetch the first page, please retry")
                print(e)

        all_ids = set()
        
        print(f"Starting to scrape pages with {COUNT} items per page...")
        for page in range(1,max_pages+1):        
            print(f"Fetching page {page}...")
            
            payload = get_payload_search(category_slug, page)
            
            # retry up to TRIES time for a page requests otherwise we skip it
            for attempt in range(TRIES):  
                try:
                    response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=15)
                    break
                except Exception as e:
                    print(e)
                    print(f"error on page {page} (attempt {attempt + 1}/{TRIES}): {e}")
                    
                    if attempt < 2:
                        print(f"Retrying in {WAIT_TIME_RETRY} seconds...")
                        time.sleep(WAIT_TIME_RETRY)
                    else:
                        print(f"Failed to fetch page {page} after {TRIES} attempts")
                        continue

            if response.status_code != 200:
                print(f"Error {response.status_code} on page {page}: {response.text}, page skiped")
                # if we couldn't fetch that page ids we just skip the page
                continue
            
            try:
                data = response.json()
                announcements = data["data"]["search"]["announcements"]["data"]
                
                if not announcements:  # No results on this page
                    print(f"No results found on page {page}")
                    continue                

                # Extract IDs from current page
                for announcement in announcements:
                    all_ids.add(announcement["id"])
                
                
                # Get pagination info
                paginator = data["data"]["search"]["announcements"]["paginatorInfo"]
                last_page = paginator.get("lastPage", 1)
                has_more = paginator.get("hasMorePages", False)
                
                print(f"Page {page}/{last_page}")
                print(f"Total IDs collected so far: {len(all_ids)}")
                
                # Check stopping conditions
                if not has_more:
                    print("No more pages available - reached end")
                    break
            
                time.sleep(WAIT_TIME)  # Rate limiting between page requests
                
            except (KeyError, TypeError) as e:
                print(f"Error processing page {page}: {e}")
                
        
        print(f"\nPagination completed!")
        print(f"Total pages scraped: {page - 1}")
        print(f"Total unique IDs collected: {len(all_ids)}")
        return all_ids


    def get_announcement_details(self, ann_id):
        payload = get_payload_post(ann_id)
        
        for attempt in range(TRIES):
            try:
                response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=10)
                
                if response.status_code != 200:
                    print(f"Error fetching details for ID {ann_id}: {response.status_code}")
                    return None
                
                return response.json()["data"]["announcement"]
                
            except Exception as e:
                print(e)
                print(f"Connection error for ID {ann_id} (attempt {attempt + 1}/{TRIES}): {e}")
                if attempt < TRIES - 1:
                    print(f"Retrying in {WAIT_TIME_RETRY} seconds...")
                    time.sleep(WAIT_TIME_RETRY)
                else:
                    print(f"Failed to fetch ID {ann_id} after {TRIES} attempts")
                    return None

