import requests

url = "https://staging-glacier.xbyte.io/api/feed-process"

payload = {'feed_id': f'3066',
            'code': '3066_2024_01_23_batch_1',
           'status': '1'}
files = []
headers = {}
try:
    response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=10)
    
    print(response.text)
except:
    ...

"""
Date
Region
City
Pin Code
Group
Product ID
Merchant Id
Item Name
Item Link
Selling Price at 11:00 AM
MRP at 11:00 AM
Discount running
Disc %
07:00:00 AM
09:00:00 AM
11:00:00 AM
02:00:00 PM
05:00:00 PM
07:00:00 PM
total hours
Live hours
offline hours
Availability

"""

