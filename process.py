import csv

# if you want to add or remove features you need to manually add/delete in the following places:
# utils.get_payload_post and inside our classes change processed_data, base_fieldnames

class DataProcessorAll:
    def process_announcement(self, raw_data, all_spec_labels=None):
        if not raw_data:
            return None
        
        # Extract all basic informations
        # NOTE: YOU can remove the unwanted columns
        # do it by removing the unwanted features from the processed_data dict and from the qeury in get_payload_post function
        processed_data = {
            # Basic announcement info
            "id": raw_data.get("id"),
            "reference": raw_data.get("reference"),
            "title": raw_data.get("title"),
            "slug": raw_data.get("slug"),
            "description": raw_data.get("description"),
            "creation_date": raw_data.get("createdAt"),
            "status": raw_data.get("status"),
            "street_name": raw_data.get("street_name"),
            
            # Price information
            "price": raw_data.get("price"),
            "price_preview": raw_data.get("pricePreview"),
            "old_price": raw_data.get("oldPrice"),
            "old_price_preview": raw_data.get("oldPricePreview"),
            "price_type": raw_data.get("priceType"),
            "price_unit": raw_data.get("priceUnit"),
            "exchange_type": raw_data.get("exchangeType"),
            
            # Delivery and contact info
            "has_delivery": raw_data.get("hasDelivery"),
            "delivery_type": raw_data.get("deliveryType"),
            "has_phone": raw_data.get("hasPhone"),
            "has_email": raw_data.get("hasEmail"),
            "quantity": raw_data.get("quantity"),
            
            # Category information
            "category_id": raw_data.get("category", {}).get("id") if raw_data.get("category") else None,
            "category_name": raw_data.get("category", {}).get("name") if raw_data.get("category") else None,
            "category_slug": raw_data.get("category", {}).get("slug") if raw_data.get("category") else None,
            
            # Location information
            "city": None,
            "city_id": None,
            "region": None,
            "region_id": None,
            
            # User information
            "user_id": raw_data.get("user", {}).get("id") if raw_data.get("user") else None,
            "username": raw_data.get("user", {}).get("username") if raw_data.get("user") else None,
            "user_display_name": raw_data.get("user", {}).get("displayName") if raw_data.get("user") else None,
            "avatar_url": raw_data.get("user", {}).get("avatarUrl") if raw_data.get("user") else None,
            
            # Store information
            "is_from_store": raw_data.get("isFromStore"),
            "store_id": None,
            "store_name": None,
            "store_slug": None,
            "store_description": None,
            "store_image_url": None,
            "store_follower_count": None,
            "store_announcements_count": None,
            "store_status": None,
            
            # Media information
            "default_media_url": None,
            "default_media_type": None,
            "media_count": 0,
            
            # Additional features
            "is_comment_enabled": raw_data.get("isCommentEnabled"),
            "no_adsense": raw_data.get("noAdsense"),
            "external_url": raw_data.get("orderExternalUrl"),
            "messenger_link": raw_data.get("messengerLink"),
            "show_analytics": raw_data.get("showAnalytics"),
            "variants_count": 0
        }
        
        # Extract city and region information
        if raw_data.get("cities") and len(raw_data["cities"]) > 0:
            city_data = raw_data["cities"][0]
            processed_data["city"] = city_data.get("name")
            processed_data["city_id"] = city_data.get("id")
            
            if city_data.get("region"):
                processed_data["region"] = city_data["region"].get("name")
                processed_data["region_id"] = city_data["region"].get("id")
        
        # Extract store information
        if raw_data.get("store"):
            store_data = raw_data["store"]
            processed_data["store_id"] = store_data.get("id")
            processed_data["store_name"] = store_data.get("name")
            processed_data["store_slug"] = store_data.get("slug")
            processed_data["store_description"] = store_data.get("description")
            processed_data["store_image_url"] = store_data.get("imageUrl")
            processed_data["store_follower_count"] = store_data.get("followerCount")
            processed_data["store_announcements_count"] = store_data.get("announcementsCount")
            processed_data["store_status"] = store_data.get("status")
        
        # Extract media information
        if raw_data.get("defaultMedia"):
            processed_data["default_media_url"] = raw_data["defaultMedia"].get("mediaUrl")
            processed_data["default_media_type"] = raw_data["defaultMedia"].get("mimeType")
        
        if raw_data.get("medias"):
            processed_data["media_count"] = len(raw_data["medias"])
        
        # Extract variants count
        if raw_data.get("variants"):
            processed_data["variants_count"] = len(raw_data["variants"])
        
        # Add spec columns (initialize all with None)
        if all_spec_labels:
            for label in all_spec_labels:
                processed_data[f"spec_{label}"] = None
        
        # Fill in actual spec values
        if raw_data.get("specs"):
            for spec in raw_data["specs"]:
                label = spec["specification"]["label"]
                value = spec["valueText"][0] if spec["valueText"] else None
                processed_data[f"spec_{label}"] = value
        
        return processed_data
    
    def collect_all_specs(self, announcements_data):
        """Collect all unique specification labels from all announcements"""
        all_specs = set()
        
        for raw_data in announcements_data:
            if raw_data and raw_data.get("specs"):
                for spec in raw_data["specs"]:
                    label = spec["specification"]["label"]
                    all_specs.add(label)
        
        return all_specs

class CSVManagerALl:
    
    def __init__(self, filename, all_spec_labels=None):
        self.filename = filename
        
        # Define all base fieldnames for complete data extraction
        base_fieldnames = [
            # Basic announcement info
            "id", "reference", "title", "slug", "description", "creation_date", 
            "status", "street_name",
            
            # Price information
            "price", "price_preview", "old_price", "old_price_preview", 
            "price_type", "price_unit", "exchange_type",
            
            # Delivery and contact info
            "has_delivery", "delivery_type", "has_phone", "has_email", "quantity",
            
            # Category information
            "category_id", "category_name", "category_slug",
            
            # Location information
            "city", "city_id", "region", "region_id",
            
            # User information
            "user_id", "username", "user_display_name", "avatar_url",
            
            # Store information
            "is_from_store", "store_id", "store_name", "store_slug", 
            "store_description", "store_image_url", "store_follower_count", 
            "store_announcements_count", "store_status",
            
            # Media information
            "default_media_url", "default_media_type", "media_count",
            
            # Additional features
            "is_comment_enabled", "no_adsense", "external_url", "messenger_link", 
            "show_analytics", "variants_count"
        ]
        
        # Add spec columns with prefix to avoid conflicts
        if all_spec_labels:
            spec_fieldnames = [f"spec_{label}" for label in sorted(all_spec_labels)]
            self.fieldnames = base_fieldnames + spec_fieldnames
        else:
            self.fieldnames = base_fieldnames
            
        self.csvfile = None
        self.writer = None
    
    def open(self):
        self.csvfile = open(self.filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        self.writer.writeheader()
        print(f"CSV file initialized: {self.filename}")
        print(f"Total columns: {len(self.fieldnames)}")
    
    def write_rows(self, data_list):
        if not data_list or not self.writer:
            return 0
        
        written_count = 0
        for data in data_list:
            if data:
                self.writer.writerow(data)
                written_count += 1
        
        self.csvfile.flush()
        return written_count
    
    def close(self):
        if self.csvfile:
            self.csvfile.close()
            print(f"CSV file closed: {self.filename}")

class DataProcessorMini:
    def process_announcement(self, raw_data, all_spec_labels=None):
        if not raw_data:
            return None
        
        # Extract only the essential fields
        processed_data = {
            "reference": raw_data.get("reference"),
            "title": raw_data.get("title"),
            "description": raw_data.get("description"),
            "price_preview": raw_data.get("pricePreview"),
            "created_at": raw_data.get("createdAt"),
            "city": None
        }
        
        # Extract city information
        if raw_data.get("cities") and len(raw_data["cities"]) > 0:
            processed_data["city"] = raw_data["cities"][0].get("name")
        
        # Add spec columns (initialize all with None)
        if all_spec_labels:
            for label in all_spec_labels:
                processed_data[f"spec_{label}"] = None
        
        # Fill in actual spec values
        if raw_data.get("specs"):
            for spec in raw_data["specs"]:
                label = spec["specification"]["label"]
                value = spec["valueText"][0] if spec["valueText"] else None
                processed_data[f"spec_{label}"] = value
        
        return processed_data
    
    def collect_all_specs(self, announcements_data):
        """Collect all unique specification labels from all announcements"""
        all_specs = set()
        
        for raw_data in announcements_data:
            if raw_data and raw_data.get("specs"):
                for spec in raw_data["specs"]:
                    label = spec["specification"]["label"]
                    all_specs.add(label)
        
        return all_specs

class CSVManagerMini:
    
    def __init__(self, filename, all_spec_labels=None):
        self.filename = filename
        
        # Define only the essential base fieldnames
        base_fieldnames = ["reference", "title", "description", "price_preview", "created_at", "city"]
        
        # Add spec columns with prefix to avoid conflicts
        if all_spec_labels:
            spec_fieldnames = [f"spec_{label}" for label in sorted(all_spec_labels)]
            self.fieldnames = base_fieldnames + spec_fieldnames
        else:
            self.fieldnames = base_fieldnames
            
        self.csvfile = None
        self.writer = None
    
    def open(self):
        self.csvfile = open(self.filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        self.writer.writeheader()
        print(f"CSV file initialized: {self.filename}")
        print(f"Total columns: {len(self.fieldnames)}")
        print(f"First 10 columns: {', '.join(self.fieldnames[:10])}")
    
    def write_rows(self, data_list):
        if not data_list or not self.writer:
            return 0
        
        written_count = 0
        for data in data_list:
            if data:
                self.writer.writerow(data)
                written_count += 1
        
        self.csvfile.flush()
        return written_count
    
    def close(self):
        if self.csvfile:
            self.csvfile.close()
            print(f"CSV file closed: {self.filename}")

