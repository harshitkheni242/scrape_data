import json
import stringify
import re
import requests
from config import headers, get_mongo_connection, extract_size
from parsel import Selector
import xml.etree.ElementTree as ET
import os
import threading

# Get MongoDB collection
collection_pdp = get_mongo_connection()

# List of category URLs
category_list = [f"https://lohaco.yahoo.co.jp/sitemap_product_{i}.xml" for i in range(1, 6)]

product_links = []

os.chdir('../../')

current_directory = os.getcwd()

html_path = os.path.join(current_directory, 'lohaco_yahoo_pdp_file_save')


try:
    if not os.path.exists(html_path):
        os.makedirs(html_path)
except Exception as e:
    print(e)

filename = '/main_yahoo_category.html'
path = html_path + filename
path = path.replace("\\", "/")

for c_link in category_list:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            res = f.read()
    else:
        product_link = requests.get(c_link)
        res = product_link.text
        with open(path, 'w', encoding='utf-8') as f:
            f.write(res)

    if res:
        lss = re.findall('<loc>(.*?)</loc>', res)
        for kk in lss:
            product_links.append(kk)
    else:
        print(c_link, "wrong response")




def process_product(link, count):
    print(link)
    id = link.split("/")[-2]
    full_html_path = os.path.join(html_path, f"{id}.html")
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
            return

    tree = Selector(text=html_response)

    product_details_json = tree.xpath("//script[@type='application/ld+json']/text()").get('')



    product_details = json.loads(product_details_json)
    try:
        product_brand = product_details['brand']['name']
    except:
        product_brand = ''

    try:
        product_name = product_details['name']
    except:
        product_name = ''

    try:
       product_size = extract_size(product_name)

    except:

        product_size = ''

    try:
        description = product_details['description']

    except:
        description = ''

    try:
        price = product_details['offers']['price']
    except:
        price = ''

    try:
        price_currency = product_details['offers']['priceCurrency']
    except:
        price_currency = ''

    try:
        product_stock = tree.xpath("//p[@class='font-weight-bold text-h4 text-sm-h2 ma-0']/text()").get('')
    except:
        product_stock = ''

    try:
        product_images = [image.replace("/r/", "/n/") for image in tree.xpath("//div[@class='thumbs']/div/img/@src").getall()]
        product_first_image = product_images[0] if product_images else ''
        product_second_images = "|".join(product_images[1:]) if len(product_images) > 1 else ''
    except:
        product_first_image = ''
        product_second_images = ''

    try:
        product_rating = product_details['aggregateRating']['ratingValue']
    except:
        product_rating = ''

    try:
        item_number = link.split("/")[-2]
    except:
        item_number = ''


    # Insert into MongoDB
    collection_pdp.insert_one({
        "main_category_url": c_link,
        "product_url": link,
        "product_brand": product_brand,
        "product_name": product_name,
        "product_size": product_size,
        "product_price": price,
        "product_description": description,
        "price_currency": price_currency,
        "product_stock": product_stock,
        "product_first_image": product_first_image,
        "product_second_image": product_second_images,
        "product_rating": product_rating,
        "item_number": item_number
    })
    collection_pdp.create_index("item_number", unique=True)


# Use threading to process product links counterinsurgency
threads = []
count = 0
for link in product_links:
    if 'item' in link:
        # process_product(link, count)
        thread = threading.Thread(target=process_product, args=(link, count))
        threads.append(thread)
        thread.start()
        count += 1
#
# Wait for all threads to finish
for thread in threads:
    thread.join()

print("All products processed.")
