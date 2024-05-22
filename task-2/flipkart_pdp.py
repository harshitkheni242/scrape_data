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
# try:
#     mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
#     mongo_db = mongo_client["flipkart"]
#     product_list_collection = mongo_db["products_list"]
#     category_list_collection = mongo_db["categorys_list"]
#     details_list_collection = mongo_db["product_details_list"]
# except Exception as e:
#     print("MongoDB connection error:", e)


connection = pymysql.connect(host="localhost", user="root", port=3306, password="tP_kc8mn", db='flipkart_products')


cursor = connection.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS products_list (
#                                    id INT PRIMARY KEY AUTO_INCREMENT,
#                                    product_name VARCHAR(100),
#                                    sponsered TEXT,
#                                    product_offer FLOAT,
#                                    product_price TEXT,
#                                    product_mrp TEXT,
#                                    product_color VARCHAR(50),
#                                    product_size
#                                    hash_id VARCHAR(64) UNIQUE
#                                )''')


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

cursor.execute('SELECT * FROM product_list')
product_links = cursor.fetchall()
for product_link in product_links:
    product_name = product_link[1]
    sponsered = product_link[2]
    product_offer = product_link[5]
    product_detail_price = float("".join(re.findall(regex, product_link[3])))
    product_detail_mrp = float("".join(re.findall(regex, product_link[4])))
    response1 = requests.get(product_link[8], headers=headers)
    if response1.status_code == 200:
        html_path1 = "/home/harshit.kheni/flipkart_product_details"
        if not os.path.exists(html_path1):
            os.makedirs(html_path1)
        tree1 = Selector(response1.text)
        product_color = tree1.xpath("//div[@class='_3Rka5k _60M1Vj col col-12-12' and .//*[contains(text(), 'Color')]]//ul")
        product_size = tree1.xpath("//div[@class='_3Rka5k _60M1Vj col col-12-12' and .//*[contains(text(), 'Size')]]//ul")
        for color in product_color:
            product_colors = ",".join(color.xpath(".//div//div/text()").getall())
        for size in product_size:
            product_sizes = ",".join(size.xpath(".//a/text()").getall())

        product_other_details = tree1.xpath("//div[@class='sBVJqn']/div[@class='row']")
        for about_details in product_other_details:
            key = about_details.xpath(".//div[@class='col col-3-12 _9NUIO9']//text()").get('')
            value = about_details.xpath(".//div[@class='col col-9-12 -gXFvC']//text()").get('')










 # details_list_collection.insert_one({
 #                            'product_name': product_name,
 #                            'sponsered': product_link,
 #                            'product_price': product_price,
 #                            'product_mrp': product_description,
 #                            'product_offer': product_description,
 #                            'product_detail_price': "|".join(list_product_description),
 #                            'product_colors': product_id,
 #                            'product_sizes': hash_id,
 #                        })









# print(product_color)
# for row in tree1.xpath("//div[@class='_5Pmv5S']//div[@class='sBVJqn']"):
#     label = row.xpath(".//div[@class='col col-3-12 _9NUIO9']/text()")
#     print(label)


# for pdp in product_details_list:
#     product_brand_name = pdp.xpath(".//span[@class='mEh187']/text()").get('')
#     product_title = pdp.xpath(".//span[@class='VU-ZEz']/text() | //h1/span[@class='VU-ZEz']/text()[1]").get('')
#     product_detail_offer = pdp.xpath(".//div[@class='UkUFwK WW8yVX dB67CR']/span/text()").get('')
#     product_ratings = pdp.xpath("//div[@class='XQDdHH _1Quie7']/text()").get('')
#     product_ratings_reviews = pdp.xpath("//span[@class='Wphh3N']/span/text()").get('')
#     product_color_size = pdp.xpath(".//ul[@class='hSEbzK']")
#     # color = ",".join(product_color_size[0].xpath(".//div[@class='AEyO3k ApdQe9 TMNmtm CWoMYn']/div[@class='V3Zflw QX54-Q E1E-3Z dpZEpc']/text()").getall())
#     # size_chart = ",".join(product_color_size[1].xpath(".//div[@class='AEyO3k ApdQe9 TMNmtm CWoMYn']/div[@class='V3Zflw QX54-Q E1E-3Z dpZEpc']/text()").getall())
#     # size = ",".join(product_color_size[1].xpath(".//a[@class='CDDksN zmLe5G dpZEpc']/text()").getall())
#     seller_name = pdp.xpath(".//div[@id='sellerName']/span/span/text()").get('')
#     # product_other_details_key = pdp.xpath(".//div[@class='_5Pmv5S']//div[@class='sBVJqn']//div[@class='col col-3-12 _9NUIO9']/text()").getall()
#     # product_other_details_value = pdp.xpath("//div[@class='_5Pmv5S']//div[@class='sBVJqn']//div[@class='col col-9-12 -gXFvC']/text()")


# concatenated_data = ''.join(
#     filter(None, [product_name, sponsored, str(product_price), str(product_mrp), product_offer,
#                   product_deal, product_image, product_id, product_list_id]))
# encoded_data = concatenated_data.encode('utf-8')
# hash_id = hashlib.sha256(encoded_data).hexdigest()
#
# data1 = (product_name, sponsored, product_price, product_mrp, product_offer,
#          product_deal, product_image, product_link, product_id, product_list_id, hash_id)
#
# data2 = ('t-shirt', category_link, hash_id, 'pending')
# try:
#     insert_into_mysql(data1, data2)
#     insert_into_mongo(product_list_collection, category_list_collection, data1, data2)
# except Exception as e:
#     print("Error inserting data:", e)
#
# try:
#     full_html_path = os.path.join(html_path, f"{hash_id}.html")
#     with open(full_html_path, 'w', encoding='utf8') as f:
#         f.write(str(response.text))
#
# except Exception as e:
#     print("Error Html file creating :", e)
#     return None