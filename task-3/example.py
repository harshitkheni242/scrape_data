import os
import requests
import hashlib
import pymysql
import pymongo
from parsel import Selector
import json
from datetime import datetime


try:
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client['stockmann']
    product_col = mongo_db['product_list']
    product_reviews = mongo_db['reviews']
    product_details_list = mongo_db['product_details']
except Exception as e:
    print("MongoDB connection error:", e)


try:
    myconn = pymysql.connect(host='localhost', db='stockmann', user='root', password='tP_kc8mn')
    # cursor.execute('CREATE DATABASE IF NOT EXISTS stockmann')
    # myconn.database = 'stockmann'
    cursor = myconn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products_list (
                                    id INT PRIMARY KEY AUTO_INCREMENT,
                                    brand_name VARCHAR(100),
                                    product_name TEXT,
                                    product_price FLOAT,
                                    product_image_link TEXT,
                                    product_link TEXT,
                                    product_id VARCHAR(50),
                                    hash_id VARCHAR(64) UNIQUE
                                )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS product_details (
                                        id INT PRIMARY KEY AUTO_INCREMENT,
                                        product_url TEXT,
                                        product_name TEXT,
                                        product_price FLOAT,
                                        product_rating VARCHAR(50),
                                        product_description TEXT,
                                        product_other_details TEXT,
                                        product_id VARCHAR(50),
                                        hash_id VARCHAR(64) UNIQUE
                                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
                                        id INT PRIMARY KEY AUTO_INCREMENT,
                                        product_url TEXT,
                                        product_name TEXT,
                                        user_name VARCHAR(50),
                                        review_start VARCHAR(50),
                                        review_title TEXT,
                                        review_location VARCHAR(100),
                                        review_write_date_time DATETIME,
                                        verified_purchase BOOLEAN,
                                        review_contents TEXT,
                                        review_image_url TEXT,
                                        review_vote_count INT,
                                        review_url TEXT,
                                        reviewer_url TEXT,
                                        timestamp DATETIME,
                                        product_link TEXT,
                                        hash_id VARCHAR(64) UNIQUE
                                        )''')

except pymysql.Error as e:
    print("MySQL connection error:", e)




url = "https://www.stockmann.com/cosrx/13719?cgid=root&store=ecomm"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cookie": "dwanonymous_8851f22771ae23bce2ab92feeaea5664=ab4TiV9BKjQ2brPqPm8jjDYlli; dntFlagSet=false; __cq_dnt=1; dw_dnt=1; sid=f19r6W7YH4dxR96f2gTppc1PvKH8p_2bDkc; dwsid=cpOLRvIhMyZ_3Nxj81wGUcCDXA5gXtE6ANzPHQ3Ogf04P8jGkOyi-00JORY6hpDV8AOcivjMNjEA5ws3prs_xQ==; cookie_consent_preferences=necessary; rcs=eF5j4cotK8lMETC0NDbUBUKW0mQPQ9M0o-Q0sxRd87QUM12TpGQzXcM0IwNd42Qz4xRjQ5M04yQjAJu0Do0",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

}

params = {
    'apikey': '4757443a-5df6-4d60-896e-727fde66a701',
    '_noconfig': 'true',
    'page_locale': 'fi_FI',
}

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

        try:
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
        except Exception as e:
            print(e)



        response1 = requests.get(
            f'https://display.powerreviews.com/m/{merchant_id}/l/all/product/{product_id}/reviews',
            headers=headers,
            params=params
        )
        if response1.status_code == 200:
            reviews = response1.json()
            for result in reviews.get('results', []):
                for review in result.get('reviews', []):
                    try:
                        user_nickname = review['details']['nickname']
                        review_title = review['details']['headline']
                        review_location = review['details']['location']
                        review_created_date = datetime.fromtimestamp(review['details']['created_date'] / 1000)
                        verified_buyer = review['badges'].get('is_verified_buyer', False)
                        comments = review['details']['comments']
                        vote_count = review['metrics']['helpful_votes']
                        rating = review['metrics']['rating']
                        review_url = f"https://display.powerreviews.com/m/1231103975/l/all/product/{product_id}/reviews"



                    except KeyError as e:
                        print("KeyError:", e)
                    except Exception as e:
                        print("Error:", e)

        else:
            print('Failed to fetch reviews:', response1.status_code)



else:
    print('Failed to fetch product page:', response.status_code)

# Close MySQL connection
myconn.close()


