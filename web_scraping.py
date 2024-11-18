import requests
from bs4 import BeautifulSoup
import csv

# Define headers (important for bypassing some website restrictions)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
}

# URL to scrape
URL = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"

# Fetch HTML content
response = requests.get(URL, headers=HEADERS)
response.raise_for_status()  # Raise an exception if there's an HTTP error

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract product details (Adjust selectors based on Amazon's HTML)
products = soup.find_all('div', class_='s-result-item')

# Create a list to store scraped data
product_data = []

# Loop through each product
for product in products:
    # Initialize each field to None to avoid missing fields issues
    product_name, price, rating, seller = None, None, None, None

    # Try to extract each field with updated selectors
    try:
        product_name = product.find('span', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-4')
        product_name = product_name.text.strip() if product_name else "N/A"
    except AttributeError:
        product_name = "N/A"

    try:
        price = product.find('span', class_='a-price-whole')
        price = price.text.strip() if price else "N/A"
    except AttributeError:
        price = "N/A"

    try:
        rating = product.find('span', class_='a-icon-alt')
        rating = rating.text.strip() if rating else "N/A"
    except AttributeError:
        rating = "N/A"

    try:
        seller = product.find('span', class_='a-size-base-plus')
        seller = seller.text.strip() if seller else "N/A"
    except AttributeError:
        seller = "N/A"

    product_data.append({
        'Product Name': product_name,
        'Price': price,
        'Rating': rating,
        'Seller Name': seller
    })

# Write scraped data to CSV file
with open('scraping.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Product Name', 'Price', 'Rating', 'Seller Name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_data)

print("Data scraped and saved to scraping.csv")
