cursor.execute('SELECT product_link FROM products_list')
        product_links = cursor.fetchone()
        for pdp_url in product_links:
            response2 = requests.get(pdp_url, headers=headers)
            if response2.status_code == 200:
                tree2 = Selector(response2.text)



query1 = ("INSERT INTO products_list "
                  "(brand_name, product_name, product_price, product_image_link, product_link, product_id, hash_id)"
                  "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        data = (product_brand, product_title, product_price, product_image, product_link, product_id, hash_id)
        try:
            cursor.execute(query1, data)
            myconn.commit()
            print("Data inserted into MySQL table successfully!")
        except pymysql.Error as e:
            print("Error inserting data into MySQL:", e)




# query1 = ("INSERT INTO products_list "
    #           "(brand_name, product_name, product_price, product_image_link, product_link, product_id, hash_id)"
    #           "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    #
    # data = (product_brand, product_title, product_price, product_image, product_link, product_id, hash_id)
    #
    # try:
    #     cursor.execute(query1, data)
    #     myconn.commit()
    #     print("Data inserted into MySQL table successfully!")
    # except pymysql.Error as e:
    #     print("Error inserting data into MySQL:", e)


# concatenated_data = ''.join(
#     filter(None, [product_brand, product_name, product_link, str(product_price), product_image, product_id, ]))
# encoded_data = concatenated_data.encode('utf-8')
# hash_id = hashlib.sha256(encoded_data).hexdigest()


# cursor.execute('SELECT product_link FROM products_list')
# product_links = cursor.fetchone()
# for pdp_url in product_links:
#     response2 = requests.get(pdp_url, headers=headers)
#     if response2.status_code == 200:
#         tree2 = Selector(response2.text)
#         product_details_page = tree2.xpath("//div[@class='accordion-wrapper']")
#         product_details = product_details_page.xpath("//div[@data-tab='tab-2']/div[@class='content']")
#         for pdp in product_details:
#             key1 = pdp.xpath(".//div[@data-property='orinId']/text()").get('')


# query1 = ("INSERT INTO products_list "
#           "(brand_name, product_name, product_price, product_image_link, product_link, product_id, hash_id)"
#           "VALUES (%s, %s, %s, %s, %s, %s, %s)")
#
# data = (product_brand, product_title, product_price, product_image, product_link, product_id, hash_id)
#
# try:
#     cursor.execute(query1, data)
#     myconn.commit()
#     print("Data inserted into MySQL table successfully!")
# except pymysql.Error as e:
#     print("Error inserting data into MySQL:", e)


# query1 = ("INSERT INTO products_list "
#           "(brand_name, product_name, product_price, product_image_link, product_link, product_id, hash_id)"
#           "VALUES (%s, %s, %s, %s, %s, %s, %s)")
#
# data = (product_brand, product_title, product_price, product_image, product_link, product_id, hash_id)
#
# try:
#     cursor.execute(query1, data)
#     myconn.commit()
#     print("Data inserted into MySQL table successfully!")
# except pymysql.Error as e:
#     print("Error inserting data into MySQL:", e)

# try:
#     product_col.insert_one({
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

