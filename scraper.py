from datetime import datetime
import time
from fetch_api import OuedKnissAPI
from settings import *

# NOTE: you can change if you're intrested in all the features got from the API or only a portion of it
# change it from settings.py
if TYPE=="MINI":
    from process import CSVManagerMini as CSVManager, DataProcessorMini as DataProcessor
else:
    from process import CSVManagerMini as CSVManager, DataProcessorMini as DataProcessor


def scrape_ouedkniss(category_slug: str, max_pages:int = None) -> str:
    # Initialize components
    api = OuedKnissAPI()
    processor = DataProcessor()
    
    try:
        print("Fetching announcement IDs...")
        announcement_ids = api.get_announcement_ids_from_pages(category_slug, max_pages)
        print(f"Found {len(announcement_ids)} announcement IDs")
        
        print("Collecting announcement details...")
        all_raw_data = []
        for i, ann_id in enumerate(announcement_ids):
            print(f"Fetching {i+1}/{len(announcement_ids)}: ID {ann_id}")
            raw_data = api.get_announcement_details(ann_id)
            all_raw_data.append(raw_data)
            # Rate limiting
            time.sleep(0.1)
        
        # collect all unique spec labels; needed to add features based on the listing type
        print("Analyzing specifications...")
        all_spec_labels = processor.collect_all_specs(all_raw_data)
        print(f"Found {len(all_spec_labels)} unique specifications: {sorted(all_spec_labels)}")
        
        # Setup CSV file with all columns
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ouedkniss_{category_slug.replace('-', '_')}_{timestamp}.csv"
        csv_manager = CSVManager(filename, all_spec_labels)
        csv_manager.open()
        
        print("Processing and writing data...")
        processed_data_list = []
        
        for raw_data in all_raw_data:
            processed_data = processor.process_announcement(raw_data, all_spec_labels)
            if processed_data:
                processed_data_list.append(processed_data)
        
        written_count = csv_manager.write_rows(processed_data_list)
        csv_manager.close()
        
        # results
        print(f"Processed {written_count} announcements out of {len(announcement_ids)} total.")
        print(f"Total fields extracted: {len(csv_manager.fieldnames)}")
        return filename
        
    except Exception as e:
        print(f"Error: {e}")
        return None


