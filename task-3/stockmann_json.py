import os
import requests
import hashlib
import pymysql
import pymongo
from parsel import Selector
from contextlib import closing
import re
import json
from datetime import datetime


regex = f'(\d+\.\d+)'

try:
    mongo_cliant = pymongo.MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_cliant['stockmann']
    product_col = mongo_db['product_list']
    product_reviews = mongo_db['reviews']

except Exception as e:
    print("MongoDB connection error:", e)


myconn = pymysql.connect(host='localhost', db='stockmann', user='root', password='tP_kc8mn')

cursor = myconn.cursor()
try:
    # cursor.execute('CREATE DATABASE IF NOT EXISTS stockmann')
    # myconn.database = 'stockmann'
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
    tree = Selector(response.text)
    domain = 'https://www.stockmann.com'
    product_list = tree.xpath("//div[@class='product-tile js-gtm-product-tile']")


    for pl in product_list:
        product_json1 = pl.xpath(".//@data-product").get('')
        product_json = pl.xpath(".//@data-power-review").get('')
        json_data1 = json.loads(product_json1)
        json_data = json.loads(product_json)
        product_link = domain + pl.xpath(".//a[@class='pdp-title']/@href").get('')
        product_brand = json_data1['brand']
        product_price = json_data1['price']
        product_name = json_data['product']['name']
        product_id = json_data['common']['page_id']
        merchant_id = json_data['common']['merchant_id']
        product_image = json_data['product']['image_url']
        product_description = json_data['product']['description']

        response1 = requests.get(
            f'https://display.powerreviews.com/m/{merchant_id}/l/all/product/{product_id}/reviews',
            headers=headers,
            params=params
        )

        reviews = json.loads(response1.text)
        try:
            for result in reviews['results']:
                for review in result['reviews']:
                    try:

                        product_id_review = result['page_id']
                        user_nickname = review['details']['nickname']
                        product_name = review['details']['product_name']
                        review_title = review['details']['headline']
                        review_location = review['details']['location']
                        review_created_date = datetime.fromtimestamp(review['details']['created_date'] / 1000)
                        verified_buyer = review['badges']['is_verified_buyer']
                        comments = review['details']['comments']
                        vote_count = review['metrics']['helpful_votes']
                        rating = review['metrics']['rating']
                        timestamp = datetime.now()
                        review_rating = review['metrics']['rating']
                        review_url = f"https://display.powerreviews.com/m/1231103975/l/all/product/{product_id_review}/reviews"

                        concatenated_data = ''.join(
                            filter(None, [product_name, user_nickname, review_title, review_location, review_created_date,
                                          verified_buyer, comments, vote_count, rating, timestamp, review_rating, review_url, product_link]))
                        encoded_data = concatenated_data.encode('utf-8')
                        hash_id = hashlib.sha256(encoded_data).hexdigest()

                        query1 = ("INSERT INTO reviews"
                                  "(product_name, user_name, review_title, review_location,"
                                  " review_write_date_time, verified_purchase, review_contents, review_vote_count, review_url, product_link, timestamp, hash_id)"
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

                        data = (product_name, user_nickname, review_title, review_location, review_created_date, verified_buyer,
                                comments, vote_count, review_url, product_link, timestamp, hash_id)

                        try:
                            cursor.execute(query1, data)
                            myconn.commit()
                            print("Data inserted into MySQL table successfully!")
                        except pymysql.Error as e:
                            print("Error inserting data into MySQL:", e)

                        try:
                            product_reviews.insert_one({
                                'product_name': product_name,
                                'user_name': user_nickname,
                                'review_title': review_title,
                                'review_location': review_location,
                                'review_write_date_time': review_created_date,
                                'verified_purchase': verified_buyer,
                                'review_contents': comments,
                                'review_vote_count': vote_count,
                                'review_url': review_url,
                                'product_link': product_link,
                                'timestamp': timestamp,
                                'hash_id': hash_id,
                            })
                            print("Data inserted into MongoDB collection successfully!")
                        except Exception as e:
                            print("Error inserting data into MongoDB:", e)

                    except KeyError as e:
                        print("KeyError:", e)
                    except Exception as e:
                        print("Error:", e)
        except Exception as e:
            print("Error:", e)
else:
    print('response status code ', response.status_code)