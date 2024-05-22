import os
import requests
import hashlib
import pymysql
import pymongo
from parsel import Selector
from contextlib import closing
import re
import json



try:
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client["flipkart"]
    product_list_collection = mongo_db["products_list"]
    category_list_collection = mongo_db["categorys_list"]
except Exception as e:
    print("MongoDB connection error:", e)

connection = pymysql.connect(host="localhost", user="root", port=3306, password="")

cursor = connection.cursor()


def create_tb_db():
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS flipkart_product")

        connection.database = 'flipkart_product'

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

        # cursor.execute('''CREATE TABLE IF NOT EXISTS product_details_page (
        #                                             id INT PRIMARY KEY AUTO_INCREMENT,
        #                                             category_name TEXT,
        #                                             category_link TEXT,
        #                                             hash_id VARCHAR(64) UNIQUE,
        #                                             status VARCHAR(50)
        #                                         )''')
    except pymysql.Error as e:
        print("MySQL connection error:", e)
        connection.close()
        cursor.close()


def insert_into_mysql(data1, data2):
    try:
        with closing(connection.cursor()) as cursor:
            query1 = ("INSERT INTO products_list "
                      "(product_name, sponsored, product_price, product_mrp, product_offer, product_deal, product_image, product_link, product_id, product_list_id, hash_id)"
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

            cursor.execute(query1, data1)
            connection.commit()

            query2 = (
                "INSERT INTO categorys_list (category_name, category_link, hash_id, status) VALUES(%s, %s, %s, %s)")
            cursor.execute(query2, data2)
            connection.commit()

            sql_query = """
                SELECT
                    (SELECT COUNT(*) FROM products_list WHERE hash_id = %s) AS product_count,
                    (SELECT COUNT(*) FROM categorys_list WHERE hash_id = %s) AS total_products
            """
            cursor.execute(sql_query, (data2[2], data2[2]))

            product_count, total_products = cursor.fetchone()

            if product_count == total_products:
                cursor.execute("UPDATE categorys_list SET status='done' WHERE hash_id=%s", (data2[2],))
                connection.commit()
                print("Sql Update Done")
            else:
                print("Sql Update Pending")
    except pymysql.Error as e:
        print("Insert into MySQL error:", e)


def insert_into_mongo(product_collection, category_collection, data1, data2):
    try:
        product_collection.insert_one({
            "product_name": data1[0],
            "sponsored": data1[1],
            "product_price": data1[2],
            "product_mrp": data1[3],
            "product_offer": data1[4],
            "product_deal": data1[5],
            "product_image": data1[6],
            "product_link": data1[7],
            "product_id": data1[8],
            "product_list_id": data1[9],
            "hash_id": data1[10]
        })

        category_collection.insert_one({
            "category_name": data2[0],
            "category_link": data2[1],
            "hash_id": data2[2],
            "status": data2[3]

        })

        total_products_count = category_collection.count_documents({"hash_id": data2[2]})
        inserted_products_count = product_collection.count_documents({"hash_id": data2[2]})

        if total_products_count == inserted_products_count:
            category_collection.update_one({"hash_id": data2[2]}, {"$set": {"status": "done"}})
            print("Mongo Update Done")
        else:
            print("Mongo Update Pending")



    except Exception as e:
        print("Insert into MongoDB error:", e)


def stockmann():
    url = "https://www.stockmann.com/cosrx/13719?cgid=root&store=ecomm"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cookie": "dwanonymous_8851f22771ae23bce2ab92feeaea5664=ab4TiV9BKjQ2brPqPm8jjDYlli; dntFlagSet=false; __cq_dnt=1; dw_dnt=1; sid=f19r6W7YH4dxR96f2gTppc1PvKH8p_2bDkc; dwsid=cpOLRvIhMyZ_3Nxj81wGUcCDXA5gXtE6ANzPHQ3Ogf04P8jGkOyi-00JORY6hpDV8AOcivjMNjEA5ws3prs_xQ==; cookie_consent_preferences=necessary; rcs=eF5j4cotK8lMETC0NDbUBUKW0mQPQ9M0o-Q0sxRd87QUM12TpGQzXcM0IwNd42Qz4xRjQ5M04yQjAJu0Do0",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "api_key": "4757443a-5df6-4d60-896e-727fde66a701"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tree = Selector(response.text)
        domain = 'https://www.stockmann.com'
        product_list = tree.xpath("//div[@class='product-tile js-gtm-product-tile']")

        for pl in product_list:
            product_json = pl.xpath(".//@data-power-review").get('')
            product_brand = pl.xpath(".//span[@class='brand-name']/text()").get('')
            product_title = pl.xpath(".//a[@class='pdp-title']/text()").get('').strip()
            product_link = domain + pl.xpath(".//a[@class='pdp-title']/@href").get('')
            product_pp = pl.xpath(".//div[@class='price']/span/span[@class='value']/text()").get('').strip().replace(
                ',', '.')
            product_price = float("".join(re.findall(regex, product_pp)))
            json_data = json.loads(product_json)
            product_id = json_data['common']['page_id']
            product_image = json_data['product']['image_url']

            concatenated_data = ''.join(
                filter(None,
                       [product_brand, product_title, product_link, str(product_price), product_image, product_id, ]))
            encoded_data = concatenated_data.encode('utf-8')
            hash_id = hashlib.sha256(encoded_data).hexdigest()

            query1 = ("INSERT INTO products_list "
                      "(brand_name, product_name, product_price, product_image_link, product_link, product_id, hash_id)"
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)")

            data = (product_brand, product_title, product_price, product_image, product_link, product_id, hash_id)

            try:
                cursor.execute(query1, data)
                myconn.commit()
                cursor.close()
                myconn.close()
                print("Data inserted into MySQL table successfully!")
            except pymysql.Error as e:
                print("Error inserting data into MySQL:", e)

            # try:
            #     product_list.insert_one({
            #         'brand_name': product_brand,
            #         'product_name': product_title,
            #         'product_price': product_price,
            #         'product_image_link': product_image,
            #         'product_link': product_link,
            #         'product_id': product_id,
            #         'hash_id': hash_id,
            #     })
            #     print("Data inserted into MongoDB collection successfully!")
            # except Exception as e:
            #     print("Error inserting data into MongoDB:", e)

            # response1 = requests.get(product_link, headers=headers)
            # if response1.status_code == 200:
            #     tree1 = Selector(response1.text)
            #     product_details_page = tree1.xpath("//div[@class='main-img-detail-block']")
            #     for pdp in product_details_page:
            #         product_brand_name = pdp.xpath("//div[@class='brand-name']/a/text()").get('')


    else:
        print('response status code ', response.status_code)