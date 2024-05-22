import pymongo
import user_agents
import re

def get_mongo_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["lohaco_yahoo"]
    collection_pdp = db["product_details"]


    return collection_pdp




headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'B=d1f6f3b4-1277-11ef-bd88-3775bafa6a8a&v=6&u=1715749130&s=u2; A=d5vpjgpj48g8a&sd=A&t=1715749130&u=1715749130&v=1; XA=d5vpjgpj48g8a&sd=A&t=1715749130&u=1715749130&v=1; XB=d1f6f3b4-1277-11ef-bd88-3775bafa6a8a&v=6&u=1715749130&s=u2',
    'if-none-match': '"25609-ta/r7woaCCxwBUVZl+IKkQ/3564"',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Chromium";v="124.0.6367.207", "Google Chrome";v="124.0.6367.207", "Not-A.Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-ch-ua-platform-version': '"6.5.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': f'{user_agents.random_useragent()}',
}



def extract_size(size_string):
    try:
        # Regular expression pattern to match size and quantity like "90g×1本"
        size_quantity_pattern = r'(\d+(\.\d+)?(?:g|kg|ml|l|oz|lb))\s*×\s*(\d+個|袋|本)'
        size_quantity_match = re.search(size_quantity_pattern, size_string)

        if size_quantity_match:
            # Extract size and quantity from the match
            size = size_quantity_match.group(1)
            quantity = size_quantity_match.group(3)
            # Combine size and quantity in the format "size (quantity)"
            Product_Size = f"{size}×{quantity}"
        else:
            # Regular expression pattern to match sizes only (e.g., 90g, 200ml)
            size_pattern = r'\b\d+(\.\d+)?\s*(ml|mL|l|g|kg|oz|lb)\b'
            size_match = re.search(size_pattern, size_string)

            # Regular expression pattern to match quantities only (e.g., 24本入り)
            # quantity_pattern = r'\(\d+\s*本入り\)'
            quantity_pattern = r'\(\d+\s*本入り\)|(\d+\s*個)'
            quantity_match = re.search(quantity_pattern, size_string)

            # Extract the size and quantity separately
            if size_match:
                size = size_match.group()
            else:
                size = ""

            if quantity_match:
                quantity = quantity_match.group()
            else:
                quantity = ""

            # Combine size and quantity if both are present
            if size and quantity:
                Product_Size = f"{size} {quantity}"
            else:
                Product_Size = size or quantity



    except:
        Product_Size = ""

    return Product_Size






