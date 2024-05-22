import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mydb.createCollection(
    "weather24h",
    {
       'timeseries': {
          'timeField': "timestamp",
          'metaField': "data",
          'granularity': "hours"
       },
       'expireAfterSeconds': 86400
    }
)


start_url = "https://www.flipkart.com/mens-tshirts/pr?sid=clo%2Cash%2Cank%2Cedy&fm=neo%2Fmerchandising&iid=M_4f30fd57-bbd7-4130-9a89-e93691b13920_1_372UD5BXDFYS_MC.IF56C41VGEYS&otracker=hp_rich_navigation_2_1.navigationCard.RICH_NAVIGATION_Fashion~Men%2527s%2BTop%2BWear~Men%2527s%2BT-Shirts_IF56C41VGEYS&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_2_L2_view-all&cid=IF56C41VGEYS&page=1"
create_tb_db()
next_page_link = get_next_page(start_url)
count = 0
while next_page_link and count < 24:
    count += 1
    print(next_page_link)
    next_page_link = get_next_page(next_page_link)
    if count == 24:
        break  # Exit the loop once count reaches 24
