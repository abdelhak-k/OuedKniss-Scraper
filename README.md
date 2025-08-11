# OuedKniss Scraper
A Python based web scraper for extracting product listings from OuedKniss.com through their GraphQL API. This tool allows you to collect announcements data and save it into a csv file, it's flexible to any type of products you're trying to get data about.

## Features

- Robust API Integration: Uses OuedKniss GraphQL API for reliable data extraction
- Flexible Data Extraction: Configurable between minimal and comprehensive data collection
- Flexible changes: Change constants through settings.py 
- Error Handling & Retry Logic: Handles connection errors
- Automatic Pagination: Scrapes multiple pages automatically
- Dynamic Specifications: Automatically detects and includes product-specific specifications
- CSV Export: Exports data to timestamped CSV files


## Requirements

- Python 3.6+
- Required packages: **requests>=2.32.3**

## Installation

1. Clone this repository:
```bash
git clone https://github.com/abdelhak-k/OuedKniss-Scraper.git
cd ouedkniss-scraper
```

* **optional: create virtual env**

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## How to use

### Finding Category Slugs

To find the category slug for the products you want to scrape:

1. Go to [www.ouedkniss.com](https://www.ouedkniss.com)
2. Navigate to the category you're interested in
3. Look at the URL in your browser address bar
4. The category slug is usually the part after the domain and before `/1`

**URL Format**: `https://www.ouedkniss.com/categorySlug/1`

**Examples**:
- URL: `https://www.ouedkniss.com/pieces_detachees/1` → Category slug: `pieces_detachees`

if this method did not work you should browser the developer tools and check the payload manually under the operation searchQuery.


### Usage Examples

#### Basic Usage
```python
# Scrape only first 5 pages
result = scrape_ouedkniss("informatique-ordinateur-portable",max_pages=5)
```

#### Scrape all the possible Pages
```python
# all possible laptop related pages 
result = scrape_ouedkniss("informatique-ordinateur-portable")
```
**Running the scraper**:
```bash
python main.py
```
#### Output File

Data is automatically saved to a CSV file:
```
ouedkniss_<category_slug>_YYYYMMDD_HHMMSS.csv
```
#### Example Output

```csv
reference,title,description,price_preview,created_at,city,spec_Marque,spec_Modèle,spec_RAM
REF123,Laptop Dell Inspiron,Gaming laptop in excellent condition,85000 DA,2025-08-10T14:30:22Z,Alger,Dell,Inspiron 15,8GB
REF124,MacBook Pro,Professional laptop for developers,250000 DA,2025-08-10T13:45:10Z,Oran,Apple,MacBook Pro,16GB
```



### Data Extraction Mode
```python
TYPE = "MINI"  # Options: "MINI" or "ALL"
```

- **MINI**: Extracts essential fields only (reference, title, description, price_preview, created_at, city, product specs)
- **ALL**: Extracts comprehensive data including store info, media, variants ... absolutly everything
- **Customizing Data Fields (specific portion of features)**:
1. Add your new mode to `TYPE` options in `settings.py`
2. Create corresponding processing logic in `process.py` and `utils.py`
3. Create DataProcessor, CSVManager classes and create a new get_payload_post query in utils; just unwanted things from get_payload_post_all and fix DataProcessor and CSVManager accordingly
4. Update the field definitions accordingly



### Rate Limiting & Best Practices

- **Respect the API**: The default `WAIT_TIME = 0.1` is recommended to avoid overwhelming the server
- **Monitor your requests**: Large categories may have 20,000+ items - plan accordingly
- **Handle interruptions**: The scraper is designed to retry failed requests automatically
- **Check file sizes**: Comprehensive scraping can generate large CSV files



## Troubleshooting
### Missing Data
If some fields are empty this is normal behavior beacuse some fields may not be available for certain categories and not all products have all specifications. 

### Large Memory Usage
For categories with many items:
- Consider scraping in smaller batches using `max_pages`
- Monitor your system's memory usage
- Large datasets are processed in memory before CSV writing

## File Structure

```
ouedkniss-scraper/
├── main.py           # Entry point
├── scraper.py        # Main scraping logic
├── fetch_api.py      # API request handlers
├── process.py        # Data processing (MINI+ALL mode)
├── utils.py          # Utilities
├── settings.py       # Configuration file
├── requirements.txt  # Dependencies
└── README.md       
```



## Legal & Ethical Considerations

- This scraper uses OuedKniss's public GraphQL API
- Respect the website's terms of service
- Use reasonable rate limits to avoid overwhelming their servers
- Consider the ethical implications of data collection
- Ensure compliance with local data protection laws
### Disclaimer

This scraper is not affiliated with or endorsed by OuedKniss.com. Use responsibly and in accordance with the website's terms of service.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.


