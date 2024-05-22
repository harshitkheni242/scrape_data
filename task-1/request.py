import requests
from lxml import html
import pymysql
from contextlib import closing
import pandas as pd

try:
    with closing(pymysql.connect(host="localhost", user="root", port=3306, password="Kheni@2002", db='quotes_to_scrape')) as myconn:
        try:
            myconn.ping(reconnect=True)
            print("Database is connected")

            with closing(myconn.cursor()) as cursor:
                new_db = input("Enter new Database name: ")
                cursor.execute(f"SHOW DATABASES LIKE '{new_db}'")
                database_exists = cursor.fetchone()

                if not database_exists:
                    cursor.execute(f"CREATE DATABASE {new_db}")
                    print(f"Database '{new_db}' created successfully")
                else:
                    print(f"Database '{new_db}' already exists")

                # myconn.db = new_db
                # print("Database Created")

                new_table = input("Enter a table Name: ")
                cursor.execute(f"SHOW TABLES LIKE '{new_table}'")
                table_exists = cursor.fetchone()
                if not table_exists:
                    cursor.execute(f'''CREATE TABLE {new_table} (
                                    id INT PRIMARY KEY AUTO_INCREMENT,
                                    quotes TEXT(400),
                                    authors VARCHAR(100),
                                    tags VARCHAR(100)
                                   )''')
                    print(f"Table '{new_table}' Created")
                else:
                    print(f"Table '{new_table}' already exists")
                quotes_data = []
                for i in range(1, 11):
                    url = f'http://quotes.toscrape.com/page/{i}/'

                    response = requests.get(url)

                    if response.status_code == 200:
                        tree = html.fromstring(response.content)

                        for quote in tree.xpath('//div[@class="quote"]'):
                            quotes = quote.xpath('.//span[@class="text"]/text()')[0].strip()
                            authors = quote.xpath('.//small[@class="author"]/text()')[0].strip()
                            tags = ",".join(quote.xpath('.//a[@class="tag"]/text()'))



                            # query = f"INSERT INTO {new_table} (quotes, authors, tags) VALUES (%s, %s, %s)"
                            # data = (quotes, authors, tags)
                            # cursor.execute(query, data)
                            # myconn.commit()



                            query = f"SELECT * FROM {new_table}"
                            cursor.execute(query)
                            results = cursor.fetchall()
                            for result in results:
                                data = {'id': result[0], 'quotes':result[1], 'authors':result[2], 'tags': result[3]}
                                quotes_data.append(data)

                        # Writing DataFrame to CSV file with comma (,) as delimiter
                        df = pd.DataFrame(quotes_data)
                        df.to_csv('quotes.csv', sep=' ', index=False)



                    else:
                       print("Failed to retrieve the webpage. Status code:", response.status_code)


        except pymysql.Error as e:
            print("Failed to connect to the database server:", e)

except pymysql.Error as e:
    print("Database connection error:", e)
