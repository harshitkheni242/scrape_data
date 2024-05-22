import json
import requests
from config import get_mongo_connection
import hashlib
import os
import threading

headers1 = {
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

collection_category, collection_product_link, collection_product_pdp = get_mongo_connection()

def fetch_subcategory_links():
    subcategory_links = []
    subcategories = collection_category.find({})
    for sub_category_info in subcategories:
        category = sub_category_info.get("category")
        if sub_category_info.get("subcategory") == "Halved":
            subcategory_name = sub_category_info.get("subcategory").replace("Halved", "Halves")
        else:
            subcategory_name = sub_category_info.get("subcategory")
        link = sub_category_info.get("link")
        if subcategory_name and link:
            subcategory_links.append({"subcategory": subcategory_name, "link": link, "category": category})
    return subcategory_links

def fetch_product_links(sub_category_name, link, category):
    all_product_links = []
    page = 0
    while True:
        data = {
            "requests": [{
                "indexName": "all_master_us_en",
                "params": f"clickAnalytics=true&facets=%5B%22brand%22%2C%22peel%22%2C%22preparationMethod%22%2C%22variety%22%5D&filters=subCategories%3A%22{sub_category_name}%22%20AND%20categories%3A%22{category}%22%20AND%20regions%3A%22us%22%20AND%20type%3AproductPageTemplate&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=12&maxValuesPerFacet=100&page={page}&tagFilters=&userToken=1758873249_1715228388"
            }]
        }

        try:
            response = requests.post(
                'https://wt7g3wtd5r-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.19.1)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.59.0)%3B%20react%20(18.2.0)%3B%20react-instantsearch%20(7.2.1)%3B%20react-instantsearch-core%20(7.2.1)%3B%20next.js%20(12.3.4)%3B%20JS%20Helper%20(3.15.0)&x-algolia-api-key=cd3b2e2ff4a865a492c38538fcdb9b63&x-algolia-application-id=WT7G3WTD5R',
                headers=headers1,
                json=data,
            )

            if response.status_code == 200:

                product_link_data = json.loads(response.text)
                for hit in product_link_data['results'][0]['hits']:
                    link = 'https://www.simplotfoods.com' + hit['url']
                    if link not in all_product_links:
                        all_product_links.append(link)

                if page <= product_link_data['results'][0]['nbPages']:
                    page += 1
                else:
                    break
            else:
                print("Status code Error", response.status_code)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return all_product_links


html_path = os.path.join(os.getcwd(), "simplot")

try:
    if not os.path.exists(html_path):
        os.makedirs(html_path)
except Exception as e:
    print(e)

subcategory_links = fetch_subcategory_links()
try:
    for subcategory_link in subcategory_links:
        link = subcategory_link["link"]
        category = subcategory_link["category"]
        sub_category_name = subcategory_link["subcategory"]
        product_links = fetch_product_links(sub_category_name, link, category)
        for p_link in product_links:
            try:
                hashid = hashlib.md5(bytes(link + category + sub_category_name + p_link, "utf8")).hexdigest()
                hashid = str(int(hashid, 16) % (10 ** 32))
            except Exception as e:
                print("Hash id not generated:", e)
                continue

            try:
                collection_product_link.insert_one({
                    "link": link,
                    "categorys": category,
                    "subactegory": sub_category_name,
                    "product_links": p_link,
                    "hashid": hashid
                })

                collection_product_link.create_index("hashid", unique=True)
            except Exception as e:
                print(e)
            try:
                collection_category.update_one({"subcategory": sub_category_name}, {"$set": {"status": "done"}})
                print("####### Status Done ######")

            except Exception as e:
                print(e)
            # full_html_path = os.path.join(html_path, f"{short_hash}.html")
            # if os.path.exists(full_html_path):
            #     with open(full_html_path, 'r', encoding='utf8') as f:
            #         html_response = f.read()
            # else:
            #     response1 = requests.get(product_links, headers=headers1)
            #     print(response1.status_code)
            #     html_response = response1.text
            #     if response1.status_code == 200:
            #         with open(full_html_path, 'w', encoding='utf8') as f:
            #             f.write(html_response)
            #         print("File Saved!.")
            #     else:
            #         print("Getting Response issue... ")
            #         exit(0)

except Exception as e:
    print(e)
