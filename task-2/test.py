import os
import requests
import hashlib
import pymysql
import pymongo
from parsel import Selector
from contextlib import closing
import user_agents
import re

regex = r'\d+'

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
                                product_name TEXT,
                                sponsored VARCHAR(400),
                                product_price VARCHAR(100),
                                product_mrp VARCHAR(10),
                                product_offer VARCHAR(100),
                                product_deal VARCHAR(400),
                                product_image TEXT,
                                product_link TEXT,
                                product_id VARCHAR(50),
                                product_list_id VARCHAR(50),
                                hash_id VARCHAR(64) UNIQUE
                            )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS categorys_list (
                                            id INT PRIMARY KEY AUTO_INCREMENT,
                                            category_name TEXT,
                                            category_link TEXT,
                                            hash_id VARCHAR(64) UNIQUE,
                                            status VARCHAR(50)
                                        )''')
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


def get_next_page(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'Network-Type=4g; T=clvgeqo2u0z2a1pfrn5i271em-BR1714119916135; at=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFkOTYzYzUwLTM0YjctNDA1OC1iMTNmLWY2NDhiODFjYTBkYSJ9.eyJleHAiOjE3MTU4NDc5MTYsImlhdCI6MTcxNDExOTkxNiwiaXNzIjoia2V2bGFyIiwianRpIjoiY2MzOWVmN2QtNGZkOC00ZTRkLWE2YjEtODAzYjZmZGY1MGQ0IiwidHlwZSI6IkFUIiwiZElkIjoiY2x2Z2VxbzJ1MHoyYTFwZnJuNWkyNzFlbS1CUjE3MTQxMTk5MTYxMzUiLCJrZXZJZCI6IlZJNzYwOTFDNTMxRTdFNDdCMUFCMUJFMzM3QjY1RkNCOTgiLCJ0SWQiOiJtYXBpIiwidnMiOiJMTyIsInoiOiJDSCIsIm0iOnRydWUsImdlbiI6NH0.J768BOGRSNs6ZKaSTmoRHPPgRHsFxLgs8aYvz0jl_R4; K-ACTION=null; ud=8.6uH41AnRCPNLlFt7n-PoRo-2GnVsAtn0wJjhxXuRLocm-uRiKKNw6jf2pcOVWALKmJ-N491LwdEpcQJkRf2eV98EmgH8-Rf4kQJrt96OzhNGERTBY0bYSTkfLfU9Mmgm0jokC5LKbgDkAIV78qkVqg; _pxvid=8341c291-03a6-11ef-9868-c617c856e7ec; rt=null; AMCV_17EB401053DAF4840A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C19844%7CMCMID%7C35440263086200621611175732437404066774%7CMCAAMLH-1714724717%7C12%7CMCAAMB-1715062329%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1714464729s%7CNONE%7CMCAID%7C331459666C90359A-60000B1C2206FA56; vh=699; vw=264; dpr=2; gpv_pn=ProductList; gpv_pn_t=ProductList; pxcts=7507aa4e-06d6-11ef-8ed8-f19fbea10198; SN=VI76091C531E7E47B1AB1BE337B65FCB98.TOKFF2DA39140654957B54E5EFC17099C34.1714470396.LO; _px3=0303453182a7a7bbb08cf6972aae0cc922d76b361e48828534f269ec12c80ee8:43Lb4+hARWWOuWop9zNSZcB2Mv//zoT4Jk7AJmKyTIqaWCQrsVEtUxKbK6+c6aiBNZqkC8bI4SU/dpHdtsQEFQ==:1000:Ez0dVfbWsTKwkzuuf1y4n2F/VkMLvaQKheWJFRtRHh5VcIcpOYXEGzjXFZCrsrKiRL7wUPz96hbKLKWckON9IJEdky6t5Q7x51w3gdPGLcVwCTwqJdMQRq4Q+awPKzrL6bp9ki8hlzHhYK/TNFEFjQseP7bXUTvw9MGS/vjnjzrXJ80A2QycKVokgRJBdSNbu6/zu2jU7p1wsj1I4O1MsCE6AJoHNaxydMhFuvhaUz4=; vd=VI76091C531E7E47B1AB1BE337B65FCB98-1714119919218-6.1714470434.1714469443.153573172; S=d1t13Pz8EP3MTPz8/PyY/Q3M/eo8Yk2KT0LcU/y19g6IF0pf8IYH4qkls63HuCnanLQVlc1BtqMjLVhYR0UeFcR7hmA==',
        'Host': 'www.flipkart.com',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Arch': '"x86"',
        'User-Agent': f'{user_agents.random_useragent()}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_path = "/home/harshit.kheni/flipkart_product_list"
        if not os.path.exists(html_path):
            os.makedirs(html_path)

        tree = Selector(response.text)
        category_link = "https://www.flipkart.com/clothing-and-accessories/topwear/tshirt/men-tshirt/pr?sid=clo,ash,ank,edy&otracker=categorytree&otracker=nmenu_sub_Men_0_T-Shirts"
        next_path = tree.xpath("//nav[@class='WSL9JP']/a/span[contains(text(),'Next')]/../@href").get()
        next_url = f'https://www.flipkart.com{next_path}' if next_path else None
        product_list = tree.xpath("//div[@class='_1sdMkc LFEi7Z']")

        for pl in product_list:
            product_name = pl.xpath(".//a[@class='WKTcLC']/text() | //a[@class='WKTcLC BwBZTg']/text()").get('')
            sponsored = pl.xpath(".//div[@class='syl9yP']/text()").get('')
            price = pl.xpath(".//div[@class='Nx9bqj']/text()").get('')
            product_price = float("".join(re.findall(regex, price)))
            mrp = "".join((pl.xpath(".//div[@class='yRaY8j']/text()")).getall())
            product_mrp = float("".join(re.findall(regex, mrp)))
            product_offer = pl.xpath(".//div[@class='UkUFwK']/span/text()").get('')
            product_deal = pl.xpath(".//div[@class='yiggsN O5Fpg8']/text()").get('')
            product_image = pl.xpath(".//img[@class='_53J4C-']/@src").get('')
            product_link = 'https://www.flipkart.com' + pl.xpath(".//a[@class='rPDeLR']/@href").get('')
            product_id = product_link.split('pid=')[-1].split('&')[0]
            product_list_id = product_link.split('lid=')[-1].split('&')[0]

            concatenated_data = ''.join(
                filter(None, [product_name, sponsored, str(product_price), str(product_mrp), product_offer,
                              product_deal, product_image, product_id, product_list_id]))
            encoded_data = concatenated_data.encode('utf-8')
            hash_id = hashlib.sha256(encoded_data).hexdigest()

            data1 = (product_name, sponsored, product_price, product_mrp, product_offer,
                     product_deal, product_image, product_link, product_id, product_list_id, hash_id)

            data2 = ('t-shirt', category_link, hash_id, 'pending')
            try:
                insert_into_mysql(data1, data2)
                insert_into_mongo(product_list_collection, category_list_collection, data1, data2)
            except Exception as e:
                print("Error inserting data:", e)

            try:
                full_html_path = os.path.join(html_path, f"{hash_id}.html")
                with open(full_html_path, 'w', encoding='utf8') as f:
                    f.write(str(response.text))
            except Exception as e:
                print("Error Html file creating :", e)

        return next_url

    else:
        print("Statu code Error", response.status_code)


start_url = "https://www.flipkart.com/mens-tshirts/pr?sid=clo%2Cash%2Cank%2Cedy&fm=neo%2Fmerchandising&iid=M_4f30fd57-bbd7-4130-9a89-e93691b13920_1_372UD5BXDFYS_MC.IF56C41VGEYS&otracker=hp_rich_navigation_2_1.navigationCard.RICH_NAVIGATION_Fashion~Men%2527s%2BTop%2BWear~Men%2527s%2BT-Shirts_IF56C41VGEYS&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_2_L2_view-all&cid=IF56C41VGEYS&page=1"
create_tb_db()
next_page_link = get_next_page(start_url)
count = 0
while next_page_link and count < 24:
    count += 1
    print(next_page_link)
    next_page_link = get_next_page(next_page_link)



