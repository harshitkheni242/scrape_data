import requests
import json
from config import get_mongo_connection
import os
import hashlib


collection_category, collection_product_link, collection_product_pdp = get_mongo_connection()

cookies = {
    'visitor_id486711': '444754809',
    'visitor_id486711-hash': '044228762a1d7cd9125a6cb2d626f457074a88f706d9a4ec82e22ea39b2573096caab1c0622d95eeb29fab520fba9f15ccdcfd5b',
    'CookieConsent': '{stamp:%27d3UPvwvcvXxLKxdb9EKgDRGim35wSOIjMoTtxPWiFREFvdCJdBzXCw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:7%2Cutc:1715321560795%2Cregion:%27in%27}',
    'NEXT_REGION': 'us',
    'NEXT_LOCALE': 'en',
    '_gcl_au': '1.1.791798221.1715322168',
    '__ncuid': '1c96aaac-7852-467e-aa7a-ed3a7512b3e7',
    '_hjSessionUser_1568514': 'eyJpZCI6IjY4MmM0YmMzLTgzMzUtNTJkMy05OTE0LWE0ZTE0MmY1MTU2ZSIsImNyZWF0ZWQiOjE3MTUzMjIxNjkwNDAsImV4aXN0aW5nIjp0cnVlfQ==',
    '_fbp': 'fb.1.1715333245688.870078773',
    '_gid': 'GA1.2.72501047.1715584298',
    '57942': '',
    '58312': '',
    '58313': '',
    '59942': '',
    '57928': '',
    '58306': '',
    '59941': '',
    '57927': '',
    '57941': '',
    '58305': '',
    '_hjSession_1568514': 'eyJpZCI6ImQ5MGZiYWZmLTMwZWItNGNjYi04MTI5LThlYzM5OWFiYjFmNyIsImMiOjE3MTU1ODQ4ODUzOTMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
    '_gat_ncAudienceInsightsGa': '1',
    '_ga_VQHQQPW9Y9': 'GS1.1.1715584267.4.1.1715584936.0.0.0',
    '_ga': 'GA1.2.1758873249.1715228388',
}

headers1 = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # 'cookie': 'visitor_id486711=444754809; visitor_id486711-hash=044228762a1d7cd9125a6cb2d626f457074a88f706d9a4ec82e22ea39b2573096caab1c0622d95eeb29fab520fba9f15ccdcfd5b; CookieConsent={stamp:%27d3UPvwvcvXxLKxdb9EKgDRGim35wSOIjMoTtxPWiFREFvdCJdBzXCw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:7%2Cutc:1715321560795%2Cregion:%27in%27}; NEXT_REGION=us; NEXT_LOCALE=en; _gcl_au=1.1.791798221.1715322168; __ncuid=1c96aaac-7852-467e-aa7a-ed3a7512b3e7; _hjSessionUser_1568514=eyJpZCI6IjY4MmM0YmMzLTgzMzUtNTJkMy05OTE0LWE0ZTE0MmY1MTU2ZSIsImNyZWF0ZWQiOjE3MTUzMjIxNjkwNDAsImV4aXN0aW5nIjp0cnVlfQ==; _fbp=fb.1.1715333245688.870078773; _gid=GA1.2.72501047.1715584298; 57942=; 58312=; 58313=; 59942=; 57928=; 58306=; 59941=; 57927=; 57941=; 58305=; _hjSession_1568514=eyJpZCI6ImQ5MGZiYWZmLTMwZWItNGNjYi04MTI5LThlYzM5OWFiYjFmNyIsImMiOjE3MTU1ODQ4ODUzOTMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _gat_ncAudienceInsightsGa=1; _ga_VQHQQPW9Y9=GS1.1.1715584267.4.1.1715584936.0.0.0; _ga=GA1.2.1758873249.1715228388',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'x-nextjs-data': '1',
}



headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # 'cookie': '_ALGOLIA=anonymous-86e0da18-c600-4b3f-8ccc-753475a00600; NEXT_LOCALE=en; __ncuid=de13db32-62c3-4d48-b9f9-12f0b9aec27b; _gid=GA1.2.894275405.1715228388; _hjSessionUser_1568514=eyJpZCI6IjI1OTBiYjNjLWJlZTAtNTQzMy04OWU1LTY4MzAxODkxZDI3YSIsImNyZWF0ZWQiOjE3MTUyMjgzODc2NTUsImV4aXN0aW5nIjp0cnVlfQ==; CookieConsent={stamp:%27V9ycVJe005YlwrutH/KBJfi4lHeTSTEXXUGi//X8GE3octzz0t2sPw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:6%2Cutc:1715228389293%2Cregion:%27in%27}; _gcl_au=1.1.1011386424.1715228389; visitor_id486711=444754809; visitor_id486711-hash=044228762a1d7cd9125a6cb2d626f457074a88f706d9a4ec82e22ea39b2573096caab1c0622d95eeb29fab520fba9f15ccdcfd5b; NEXT_REGION=us; _hjSession_1568514=eyJpZCI6IjNkOThkM2RhLTM3NzgtNGJkMy04ZWU0LWU4NTdiMGJjNWRkMCIsImMiOjE3MTUyNTIxNTQ0NTUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; 57942=; 58312=; 58313=; 59942=; 57928=; 58306=; 59941=; 57927=; 57941=; 58305=; _ga=GA1.2.1758873249.1715228388; _ga_VQHQQPW9Y9=GS1.1.1715252154.3.1.1715255472.0.0.0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

response = requests.get(
    "https://www.simplotfoods.com/_next/data/EWhPr-sYTH0eDzQQSA1ol/foodservice-categories/vegetables/asparagus.json?slugs=foodservice-categories&slugs=vegetables&slugs=asparagus",
    # cookies=cookies,
    headers=headers,
)

if response.status_code == 200:
        html_path = "/home/harshit.kheni/Training_Harshit/task-4/simplot"
        try:
            if not os.path.exists(html_path):
                os.makedirs(html_path)
        except Exception as e:
            print(e)

        json_load1 = json.loads(response.text)
        for item in json_load1['pageProps']['navBar']['navigationBarDropdownGroups']['dropdownGroups'][0]['column1Categories'][
            'categories']:
            category_name1 = item['categoryName']
            category_name1_modified = "-".join(category_name1.lower().split())
            for sub_item in item['childLinks']['items']:
                sub_category_name1 = sub_item['linkTitle']
                subcategory_text_modified = "-".join(sub_category_name1.lower().split())
                link1 = f"https://www.simplotfoods.com/foodservice-categories/{category_name1_modified}/{subcategory_text_modified}"
                try:
                    hashid = str(
                        int(hashlib.md5(bytes(category_name1 + sub_category_name1 + link1, "utf8")).hexdigest(),
                            32) % (
                                10 ** 32))
                except:
                    print("Hash id not genrated")
                # full_html_path = os.path.join(html_path, f"{short_hash}.html")
                # if os.path.exists(full_html_path):
                #     with open(full_html_path, 'r', encoding='utf8') as f:
                #         html_response = f.read()
                # else:
                #     response1 = requests.get(link1, headers=headers1, cookies=cookies)
                #     print(response1.status_code)
                #     html_response = response1.text
                #     if response1.status_code == 200:
                #         with open(full_html_path, 'w', encoding='utf8') as f:
                #             f.write(html_response)
                #         print("File Saved!.")
                #     else:
                #         print("Getting Response issue... ")
                #         exit(0)

                data1 = {
                    "link": link1,
                    "category": category_name1,
                    "subcategory": sub_category_name1,
                    "hashid": hashid,
                    "status": "pending"
                }
                collection_category.insert_one(data1)
                collection_category.create_index("hashid", unique = True)

        for item in \
        json_load1['pageProps']['navBar']['navigationBarDropdownGroups']['dropdownGroups'][0]['column2Categories'][
            'categories']:
            category_name2 = item['categoryName']
            category_name2_modified = "-".join(category_name2.lower().split())
            for sub_item in item['childLinks']['items']:
                sub_category_name2 = sub_item['linkTitle']
                subcategory_text_modified = "-".join(sub_category_name2.lower().split())
                link2 = f"https://www.simplotfoods.com/foodservice-categories/{category_name2_modified}/{subcategory_text_modified}"
                concatenated_data = ''.join([category_name2, sub_category_name2, link2])
                sha256_hash = hashlib.sha256(concatenated_data.encode("utf-8")).hexdigest()
                short_hash = sha256_hash[:8]
                try:
                    hashid = str(
                        int(hashlib.md5(bytes(category_name2 + sub_category_name2 + link2, "utf8")).hexdigest(),
                            32) % (
                                10 ** 32))
                except:
                    print("Hash id not genrated")

                data2 = {
                    "link": link2,
                    "category": category_name2,
                    "subcategory": sub_category_name2,
                    "hashid": hashid,
                    "status": "pending"
                }
                collection_category.insert_one(data2)
                collection_category.create_index("hashid", unique=True)
                # full_html_path = os.path.join(html_path, f"{short_hash}.html")
                # if os.path.exists(full_html_path):
                #     with open(full_html_path, 'r', encoding='utf8') as f:
                #         html_response = f.read()
                # else:
                #     response1 = requests.get(link2, headers=headers1, cookies=cookies)
                #     print(response1.status_code)
                #     html_response = response1.text
                #     if response1.status_code == 200:
                #         with open(full_html_path, 'w', encoding='utf8') as f:
                #             f.write(html_response)
                #         print("File Saved!.")
                #     else:short_hash
                #         print("Getting Response issue... ")
                #         exit(0)



        for item in \
        json_load1['pageProps']['navBar']['navigationBarDropdownGroups']['dropdownGroups'][0]['column3Categories'][
            'categories']:
            category_name3 = item['categoryName']
            category_name3_modified = "-".join(category_name3.lower().split())
            for sub_item in item['childLinks']['items']:
                sub_category_name3 = sub_item['linkTitle']
                subcategory_text_modified = "-".join(sub_category_name3.lower().split())
                link3 = f"https://www.simplotfoods.com/foodservice-categories/{category_name3_modified}/{subcategory_text_modified}"
                try:
                    hashid = str(
                        int(hashlib.md5(bytes(category_name3 + sub_category_name3 + link3, "utf8")).hexdigest(),
                            32) % (
                                10 ** 32))
                except:
                    print("Hash id not genrated")
                # full_html_path = os.path.join(html_path, f"{short_hash}.html")
                # if os.path.exists(full_html_path):
                #     with open(full_html_path, 'r', encoding='utf8') as f:
                #         html_response = f.read()
                # else:
                #     response1 = requests.get(link3, headers=headers1, cookies=cookies)
                #     print(response1.status_code)
                #     html_response = response1.text
                #     if response1.status_code == 200:
                #         with open(full_html_path, 'w', encoding='utf8') as f:
                #             f.write(html_response)
                #         print("File Saved!.")
                #     else:
                #         print("Getting Response issue... ")
                #         exit(0)

                data3 = {
                    "link": link3,
                    "category": category_name3,
                    "subcategory": sub_category_name3,
                    "hashid": hashid,
                    "status": "pending"
                }
                collection_category.insert_one(data3)
                collection_category.create_index("hashid", unique=True)

        for item in \
        json_load1['pageProps']['navBar']['navigationBarDropdownGroups']['dropdownGroups'][0]['column4Categories'][
            'categories']:
            category_name4 = item['categoryName']
            category_name4_modified = "-".join(category_name4.lower().split()).replace('&', 'and')
            for sub_item in item['childLinks']['items']:
                sub_category_name4 = sub_item['linkTitle']
                subcategory_text_modified = "-".join(sub_category_name4.lower().split())
                link4 = f"https://www.simplotfoods.com/foodservice-categories/{category_name4_modified}/{subcategory_text_modified}"
                try:
                    hashid = str(
                        int(hashlib.md5(bytes(category_name4 + sub_category_name4 + link4, "utf8")).hexdigest(),
                            32) % (
                                10 ** 32))
                except:
                    print("Hash id not genrated")
                # full_html_path = os.path.join(html_path, f"{short_hash}.html")
                # if os.path.exists(full_html_path):
                #     with open(full_html_path, 'r', encoding='utf8') as f:
                #         html_response = f.read()
                # else:
                #     response1 = requests.get(link4, headers=headers1, cookies=cookies)
                #     print(response1.status_code)
                #     html_response = response1.text
                #     if response1.status_code == 200:
                #         with open(full_html_path, 'w', encoding='utf8') as f:
                #             f.write(html_response)
                #         print("File Saved!.")
                #     else:
                #         print("Getting Response issue... ")
                #         exit(0)

                data4 = {
                    "link": link4,
                    "category": category_name4,
                    "subcategory": sub_category_name4,
                    "hashid": hashid,
                    "status": "pending"
                }
                collection_category.insert_one(data4)
                collection_category.create_index("hashid", unique=True)

else:
    print("error status code ", response.status_code)