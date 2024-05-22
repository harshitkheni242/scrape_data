import pymongo

def get_mongo_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["simploat_food"]
    collection_category = db["category_link"]
    collection_product_link = db["product_link"]
    collection_product_pdp = db["product_details_page"]

    return collection_category, collection_product_link, collection_product_pdp

