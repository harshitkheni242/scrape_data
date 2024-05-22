import json
import re
import requests
from config import headers, get_mongo_connection
from parsel import Selector
import xml.etree.ElementTree as ET
import os

# Get MongoDB collection
collection_pdp = get_mongo_connection()

# List of category URLs
category_list = [f"https://lohaco.yahoo.co.jp/sitemap_product_{i}.xml" for i in range(1, 6)]

product_links = []

# Create directory to store HTML files
html_path = os.path.join(os.getcwd(), "lohaco_yahoo_pdp")
try:
    if not os.path.exists(html_path):
        os.makedirs(html_path)
except Exception as e:
    print(e)

# Extract product links from XML sitemaps
for c_link in category_list:
    product_link = requests.get(c_link)
    if product_link.status_code == 200:
        root = ET.fromstring(product_link.content)
        for loc in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            product_links.append(loc.text)
    else:
        print(f"Failed to fetch {c_link}")

# Iterate through product links
count = 0
for link in product_links:
    if 'item' in link:
        full_html_path = os.path.join(html_path, f"{count}.html")

        if os.path.exists(full_html_path):
            with open(full_html_path, 'r', encoding='utf8') as f:
                html_response = f.read()
        else:
            response = requests.get(link, headers=headers)
            print(response)
            html_response = response.text
            if response.status_code == 200:
                with open(full_html_path, 'w', encoding='utf8') as f:
                    f.write(html_response)
            else:
                print("Getting Response issue... ")
                exit(0)

        tree = Selector(text=html_response)

        # Extract product details
        product_details_json = tree.xpath("//script[@type='application/ld+json']/text()").get('')
        product_details = json.loads(product_details_json)


        product_brand = product_details.get('brand', {}).get('name', '')
        product_name = product_details.get('name', '')
        description = product_details.get('description', '')
        price = product_details.get('price', '')
        price_currency = product_details.get('offers', {}).get('priceCurrency', '')

        product_stock = tree.xpath("//p[@class='font-weight-bold text-h4 text-sm-h2 ma-0']/text()").get('')

        product_images = [image.replace("/r/", "/n/") for image in tree.xpath("//div[@class='thumbs']/div/img/@src").getall()]
        product_first_image = product_images[0] if product_images else ''
        product_second_images = "|".join(product_images[1:]) if len(product_images) > 1 else ''

        item_number = link.split("/")[-2]

        # Insert into MongoDB
        collection_pdp.insert_one({
            "product_url": link,
            "product_brand": product_brand,
            "product_name": product_name,
            "product_price": price,
            "product_description": description,
            "price_currency": price_currency,
            "product_stock": product_stock,
            "product_first_image": product_first_image,
            "product_second_image": product_second_images,
            "item_number": item_number
        })

        count += 1
    else:
        print("Product Link Not Found")
