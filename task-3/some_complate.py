import os
import requests
import json
import hashlib
from scrapy import Selector
import mysql.connector
from pymongo import MongoClient

# Assuming you have initialized the database connection somewhere
# myconn = mysql.connector.connect(host="localhost", user="yourusername", password="yourpassword", database="yourdatabase")
# cursor = myconn.cursor()

# Assuming you have initialized the MongoDB client somewhere
# client = MongoClient('localhost', 27017)
# db = client['your_database']
# product_details_list = db['product_details']

url = "https://www.stockmann.com"  # URL to scrape
headers = {}  # Add headers if needed

response = requests.get(url, headers=headers)
if response.status_code == 200:
    html_path = "/home/harshit.kheni/stockmann_product_details_list"
    if not os.path.exists(html_path):
        os.makedirs(html_path)

    tree = Selector(response.text)
    domain = 'https://www.stockmann.com'
    product_list = tree.xpath("//div[@class='product-tile js-gtm-product-tile']")
    for pl in product_list:
        product_json1 = pl.xpath(".//@data-product").get('')
        product_json = pl.xpath(".//@data-power-review").get('')
        json_data1 = json.loads(product_json1)
        json_data = json.loads(product_json)
        product_link = domain + pl.xpath(".//a[@class='pdp-title']/@href").get('')
        product_brand = json_data1.get('brand', '')
        product_price = json_data1.get('price', '')
        product_name = json_data['product'].get('name', '')
        product_id = json_data['common'].get('page_id', '')
        merchant_id = json_data['common'].get('merchant_id', '')
        product_image = json_data['product'].get('image_url', '')
        product_description = json_data['product'].get('description', '')

        concatenated_data = ''.join(
            [product_name, product_link, product_brand, str(product_price), str(product_id), product_image, product_description])
        hash_id = hashlib.sha256(concatenated_data.encode()).hexdigest()


        cursor.execute('SELECT hash_id FROM product_details WHERE hash_id = %s', (hash_id,))
        existing_hash_id = cursor.fetchone()
        if existing_hash_id:
            print("Record with hash_id already exists, skipping insertion.")
        else:
            cursor.execute('SELECT product_link FROM products_list')
            product_links = cursor.fetchall()
            for pdp_url in product_links:
                response2 = requests.get(pdp_url[0], headers=headers)
                if response2.status_code == 200:
                    tree2 = Selector(text=response2.text)
                    tab_details = tree2.xpath("//div[@data-tab='tab-2']")
                    list_product_description = []
                    for row in tab_details:
                        property_names = row.xpath(".//th/div/text()").getall()
                        property_values = row.xpath(".//td/text()").getall()
                        for prop_name, prop_value in zip(property_names, property_values):
                            list_product_description.append(f'{prop_name}:{prop_value}')

                    query = ("INSERT INTO product_details "
                             "(product_url, product_name, product_price, product_description, product_other_details, product_id, hash_id) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s)")
                    data = (product_link, product_name, product_price, product_description, "|".join(list_product_description), product_id, hash_id)
                    cursor.execute(query, data)
                    myconn.commit()

                    product_details_list.insert_one({
                        'product_name': product_name,
                        'product_link': product_link,
                        'product_price': product_price,
                        'product_description': product_description,
                        'product_other_details': "|".join(list_product_description),
                        'product_id': product_id,
                        'hash_id': hash_id,
                    })

# Close cursor and connection when done
cursor.close()
myconn.close()
