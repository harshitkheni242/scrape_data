import time

from fuzzywuzzy import fuzz
import os.path
import sys

from Henfruit_blinkit_app.Export_excel import Export_Csv
from Henfruit_blinkit_app.spiders.get_zipcode_cookie import *



Headers = {
    'accept': 'application/json',
    # 'accept-encoding': 'gzip, deflate, br',
    'app_api_version': '28',
    'app_client': 'consumer_android',
    'app_version': '80150630',
    'auth_key': '45bff2b1437ff764d5e5b9b292f9771428e18fc40b7f3b7303d196ea84ab4341',
    'battery-level': 'EXCELLENT',
    'connection': 'keep-alive',
    'content-length': '188',
    'content-type': 'application/json; charset=UTF-8',
    'cookie': '__cfruid=3df010127324c270f12bb93fc5e206569da4f907-1697088888; path=/; domain=.grofers.com; HttpOnly; Secure; SameSite=None',
    'cpu-level': 'AVERAGE',
    'cur_lat': '31.24916',
    'cur_lon': '121.4878983',
    'device_id': '208fbcc06e9d287b',
    'host': 'api2.grofers.com',
    'host_app': 'blinkit',
    'lat': '13.0097647',
    'lon': '77.5253962',
    'memory-level': 'AVERAGE',
    'network-level': 'LOW',
    'qd_sdk_request': 'true',
    'qd_sdk_version': '1',
    'registration_id': 'cvadEKDVRT2AaKdclGl73R:APA91bENgoz44rHN20puVMBMJe3Bau4nC1W8fIDvofo6uy7b6iwH6YdapvzRueoTuICD59N4HTpPgOvkmL9hdElulQvv0kRk_7nU62CzLPY6sy6mGS4LiJnBFO05c_KUCRvUgDCFwTUe',
    'rn_bundle_version': '1009002001',
    'screen_density': '750px',
    'screen_density_num': '1.5',
    'storage-level': 'EXCELLENT',
    'user-agent': 'com.grofers.customerapp/280150630 (Linux; U; Android 9; en_US; ASUS_Z01QD; Build/PI; Cronet/114.0.5735.33)',
    'version_name': '15.63.0',
    'x-rider-installed': 'false',
    'x-zomato-installed': 'false'
}

# -------------------------------------- Crawlera Key --------------------------------------

# username = 'sp6eg5exu9'
# password = 'MFqg27ipq4Wv8phLqw'
# proxy = f"http://{username}:{password}@gate.smartproxy.com:10000"
# proxies = {
#   "http": proxy,
#   "https": proxy
# }
# -------------------------------------- Crawlera Key --------------------------------------
# -------------------------------------- Crawlera Key --------------------------------------
proxi = 'crawlera'
# proxi = 'uncloker'

if proxi == 'crawlera':
    # -------------------------------------- Crawlera Key --------------------------------------
    
    current_proxy = open('Crawlera_key.txt', 'r').read()
    # -------------------------------------- Crawlera Key --------------------------------------
    # proxy_port = "8010"
    
    proxy_host = "proxy.zyte.com"
    proxy_port = "8011"
    proxy_auth = f"{current_proxy}:"
    proxies = {
        "http": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
        "https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
    }
    Proxy = 'crawlera'
    Headers['x-requested-with'] = "XMLHttpRequest"
    Headers['X-Crawlera-Cookies'] = "disable"
else:
    """
    brd.superproxy.io:22225
    brd-customer-hl_4fc8c816-zone-zone1krushil
    v59ddwtao95p
    """
    # web_unblocker_proxies
    # proxies = {
    #     'http': 'http://brd-customer-hl_4fc8c816-zone-zone1krushil:v59ddwtao95p@brd.superproxy.io:22225',
    #     'https': 'http://brd-customer-hl_4fc8c816-zone-zone1krushil:v59ddwtao95p@brd.superproxy.io:22225',
    # }
    
    # unblocker_smartproxy
    # proxies = {
    #     'http': 'http://U0000132814:l9dwi8pQjmPoGh0p9I@unblock.smartproxy.com:60000',
    #     'https': 'http://U0000132814:l9dwi8pQjmPoGh0p9I@unblock.smartproxy.com:60000'
    # }
    
    # mobile_smartproxy
    # proxies = {
    #     "https": f"http://spp3kljehm:n1rp25B5fRCreinhHe@as-gate.visitxiangtan.com:8000",
    #     "http": f"http://spp3kljehm:n1rp25B5fRCreinhHe@as-gate.visitxiangtan.com:8000",
    # }
    #
    # # Residentials PROXY:
    # proxies = {
    #     "https": f"http://sp9uiprib1:EDxdhj2gzB2xIv68rw@us.smartproxy.com:10000",
    #     "http": f"http://sp9uiprib1:EDxdhj2gzB2xIv68rw@us.smartproxy.com:10000",
    # }
    # proxies = {
    #     'http': 'http://unlocker_krushil:xByTenEw2024@unblock.oxylabs.io:60000',
    #     'https': 'http://unlocker_krushil:xByTenEw2024@unblock.oxylabs.io:60000',
    # }

class BlinkitSpider(scrapy.Spider):
    name = 'blinkit'
    handle_httpstatus_list = [404]

    def __init__(self, start='', end='', upload=''):
        try:
            self.start = start
            self.end = end
            self.upload = upload
            self.cursor = HenfruitBlinkitAppPipeline.cursor
            self.con = HenfruitBlinkitAppPipeline.con

        except Exception as e:
            print('__init__ error:', e)

    def start_requests(self):
        slot_list = ['07:00:00 AM', '09:00:00 AM', '11:00:00 AM', '02:00:00 PM', '05:00:00 PM']

        Period = datetime.today().strftime("%p")
        Hour = datetime.today().strftime("%I")

        Timeslot = f'{Hour}:00:00 {Period}'
        Timeslot1 = f'{Hour}_00_00_{Period}'

        # pdp_table = f'product_data_{Timeslot1}_{new_td}'

        brand_select = f"select `Id`, `Latitude`, `Longitude`, `Region`, `City`, `Pin Code`, `Group`, `Product ID`, `Item Name`  from {pdp_table} where Status = 'Pending' AND ID BETWEEN {self.start} AND {self.end}"
        self.cursor.execute(brand_select)
        brand_list = [column for column in self.cursor.fetchall()]
        if not brand_list:
            print("...................Getting empty Result.................")
        else:
            for i in brand_list:
                row_id = i[0]
                Latitude = i[1]
                Longitude = i[2]
                Region = i[3]
                City = i[4]
                PinCode = i[5]
                Group = i[6]
                Product_ID = i[7]
                Item_Name = i[8]

                if Timeslot in slot_list:
                    Path_Timeslot = f'{Hour}_00_00_{Period}'
                    print(Timeslot)
                    search_keywors = str(Item_Name).replace("(","").replace(")","").replace(" ","_").replace("-","").replace(",","")
                    filename = f'/Search_{PinCode}_{City}_{Group}_{Product_ID}_{search_keywors}_{Path_Timeslot}.html'
                    path = HTMLs + filename
                    path = path.replace("\\", "/")

                    # delete_duplicate_row = f"delete from {pdp_table} where ID1 = {row_id} and Parent ='No'"
                    # self.cursor.execute(delete_duplicate_row)
                    # self.con.commit()
                    if Longitude and Latitude:
                        Headers['lat'] = str(Latitude)
                        Headers['lon'] = str(Longitude)
                    else:
                        get_lat_lon = Get_Latitude_Longitude(Region, City, PinCode, Group)
                        Latitude = get_lat_lon.get('Latitude')
                        Longitude = get_lat_lon.get('Longitude')
                        Headers['lat'] = str(Latitude)
                        Headers['lon'] = str(Longitude)
                        update1 = f"UPDATE {Input_table} SET `Latitude`= '{Latitude}', `Longitude`= '{Longitude}' WHERE  `Region` = '{Region}' AND `City` = '{City}' AND `Pin Code` = '{PinCode}' AND `Group` = '{Group}'"
                        print(update1)
                        self.cursor.execute(update1)
                        self.con.commit()
                        update = f"UPDATE {pdp_table} SET `Latitude`= '{Latitude}', `Longitude`= '{Longitude}' WHERE  `Region` = '{Region}' AND `City` = '{City}' AND `Pin Code` = '{PinCode}' AND `Group` = '{Group}'"
                        self.cursor.execute(update)
                        self.con.commit()

                    if Latitude == "N/A":
                        update = f"UPDATE {pdp_table} SET Status = 'Not Found' WHERE Id = '{row_id}'"
                        self.cursor.execute(update)
                        self.con.commit()
                        print("No Product Found....")
                        continue

                    meta = {'row_id': row_id,
                            'path': path,
                            'Latitude': Latitude,
                            'Longitude': Longitude,
                            'Region': Region,
                            'City': City,
                            'PinCode': PinCode,
                            'Group': Group,
                            'Product_ID': Product_ID,
                            # 'pdp_table': pdp_table,
                            'Item_Name': Item_Name
                            }
                    if os.path.exists(path):
                        yield scrapy.FormRequest(url=f'file:///{path}', callback=self.parse, meta=meta, dont_filter=True)

                    else:
                        encoded_Item_Name = quote(Item_Name)
                        # Replace spaces with '+'
                        encoded_Item_Name = encoded_Item_Name.replace('%20', '+')

                        print(encoded_Item_Name)

                        search_url = f"https://api2.grofers.com/v1/layout/search?offset=0&limit=24&last_snippet_type=product_card_snippet_type_2&last_widget_type=listing_container&page_index=1&q={encoded_Item_Name}&search_count=24&search_method=basic&search_type=history&total_entities_processed=1&total_pagination_items=24"

                        payload = {
                            'monet_assets': [
                                {
                                    'name': 'ads_vertical_banner',
                                    'processed': 0,
                                    'total': 0
                                }
                            ],
                            'postback_meta': {
                                'boosted_product_ids': []
                            },
                            'previous_search_query': Item_Name
                        }
                        response_flag = False
                        for _ in range(10):
                            # req = requests.get(url,verify=False,proxies=web_blocker,headers=headers)
                            res = requests.post(url=search_url, headers=Headers, data=json.dumps(payload), verify=False,
                                                proxies=proxies)
                            print(res.status_code)
                            if res.status_code == 200 and 'stepper_data_v2' in res.text and 'snippets' in res.text:
                                response_flag = True
                                break

                            elif "Oops! We couldn't find products matching" in res.text or "snippet-list is empty for slp" in res.text:
                                response_flag = True
                                break

                            if str(row_id) == "1" and (res.status_code == 407 or 'User account suspended' in res.text):
                                print("Crawlera Key Expired...")
                                Skype_bot(
                                    f"Crawlera Key Expired...{current_proxy}\n\nUpdate Working key on below path:\n\\\\192.168.1.129\E\Kamaram_Choudhary\working\Hen's fruit\Henfruit_blinkit_app\Henfruit_blinkit_app\spiders\Crawlera_key.txt")
                                break

                            time.sleep(5)

                        if response_flag:
                            if res.status_code == 200 and 'stepper_data_v2' in res.text and 'snippets' in res.text:
                                with open(path, 'w', encoding='utf-8')as f:
                                    f.write(res.text)

                                yield scrapy.FormRequest(url=f'file:////{path}', callback=self.parse, meta=meta, dont_filter=True)

                            elif "Oops! We couldn't find products matching" in res.text or "snippet-list is empty for slp" in res.text:
                                print("Oops! We couldn't find products matching")
                                with open(path, 'w', encoding='utf-8') as f:
                                    f.write(res.text)

                                update = f"UPDATE {pdp_table} SET Status = 'Not Found' WHERE Id = '{row_id}'"
                                self.cursor.execute(update)
                                self.con.commit()
                                print("No Product Found....")

                            # elif res.status_code == 550:
                            #     update = f"UPDATE {pdp_table} SET Status = 'Not Found' WHERE Id = '{row_id}'"
                            #     self.cursor.execute(update)
                            #     self.con.commit()
                            #     print("No Product Found....")
                            #
                            else:
                                # if str(row_id) == "1" and (res.status_code == 407 or 'User account suspended' in res.text):
                                #     print("Crawlera Key Expired...")
                                #     Skype_bot(f"Crawlera Key Expired...{current_proxy}\n\nUpdate Working key on below path:\n\\192.168.1.129\E\Kamaram_Choudhary\working\Hen's fruit\Henfruit_blinkit_app\Henfruit_blinkit_app\spiders\Crawlera_key.txt")
                                #
                                print("Getting Wrong Response....", Product_ID)
                                res = requests.post(url=search_url, headers=Headers, data=json.dumps(payload), verify=False,
                                                    proxies=proxies)
                                print(res.status_code)

                                if res.status_code == 200 and 'stepper_data_v2' in res.text and 'snippets' in res.text:
                                    with open(path, 'w', encoding='utf-8') as f:
                                        f.write(res.text)

                                    yield scrapy.FormRequest(url=f'file:////{path}', callback=self.parse, meta=meta,
                                                             dont_filter=True)

                
                else:
                    print("Current Slot Not Required for scrape....")
                    continue

    def parse(self, response):
        row_id = response.meta.get('row_id')
        path = response.meta.get('path')
        Latitude = response.meta.get('Latitude')
        Longitude = response.meta.get('Longitude')
        Region = response.meta.get('Region')
        City = response.meta.get('City')
        PinCode = response.meta.get('PinCode')
        Group = response.meta.get('Group')
        Product_ID = response.meta.get('Product_ID')
        Item_Name = response.meta.get('Item_Name')
        
        result_find_flag = False
        Items = PDP_Item()
        Items['Id'] = row_id
        try:
            print("Start Crawling.....")
            # print(response.text)
            try:
                Data_Json = json.loads(response.text)
            except Exception as e:
                print("Error in Json Load: ", e)
                os.remove(path)
                return None



            for product_ in Data_Json['response']['snippets']:
                # print(json.dumps(product_))
                if 'stepper_data_v2' in str(product_):
                    product_1 = product_['data']['stepper_data_v2']['increment_actions']['default'][0]['add_to_cart']['cart_item']

                    Product_id = product_1['product_id']
                    merchant_id = product_1['merchant_id']
                    print("Product_id :", Product_id)

                    Product_name = product_1['product_name']
                    print("Product_name :", Product_name)
                    print("INPUT_name :", Item_Name)
                    
                    if "(" in Product_name:
                        Product_unit = str(Product_name).split("(")[-1].split(")")[0]
                    else:
                        Product_unit = product_1['unit']
                        
                    Product_unit = str(Product_unit).lower().replace('pieces', 'piece')
                    if "(" in Product_unit:
                        Product_unit = str(Product_unit).split("(")[-1].split(")")[0]
                    print("Product_unit :", Product_unit)
    
                    # Use fuzz.ratio() for simple string similarity
                    product_name1 = Item_Name.split(",")[0]
                    match_score = fuzz.ratio(product_name1, Product_name)

                    print(f"Matching Score: {match_score}%")

                    if match_score > 80 and Product_unit in str(Item_Name).lower():
                        result_find_flag = True
                        Items['htmlpath'] = path
                        Items['Status'] = "Done"
                        Items['Date'] = current_date
                        Items['Product ID1'] = Product_id
                        Items['Merchant Id'] = merchant_id
                        Items['Item Name1'] = Product_name

                        Available = product_['data']['product_state']
                        if str(Available).lower() == 'available':
                            availability = 'YES'
                        else:
                            availability = 'No'

                        slot_list = ['07:00:00 AM', '09:00:00 AM', '02:00:00 PM', '05:00:00 PM']

                        Period = datetime.today().strftime("%p")
                        Hour = datetime.today().strftime("%I")

                        Timeslot = f'{Hour}:00:00 {Period}'
                        print(Timeslot)
                        if Timeslot == '11:00:00 AM':
                            print('Going to update Price and Availability....')

                            regular_price = product_1['mrp']
                            print("regular_price : ", regular_price)

                            selling_price = product_1['price']
                            print("selling_price : ", selling_price)

                            Items['Selling Price at 11:00 AM'] = selling_price

                            Items['MRP at 11:00 AM'] = regular_price

                            if selling_price != regular_price:
                                discount_running = float(regular_price) - float(selling_price)
                                # Calculate the percentage
                                percentage = round(((regular_price - selling_price) / regular_price) * 100, 2)

                                # Print the result
                                print(f"The percentage of MRP vs. SP is: {percentage}%")

                            else:
                                discount_running = '0'
                                percentage = "0.00"

                            Items['Discount running'] = discount_running

                            Items['Disc %'] = percentage

                            Items['11:00:00 AM'] = availability

                            yield Items

                            get_yes_count = f"SELECT SUM( CASE WHEN `07:00:00 AM` = 'Yes' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `09:00:00 AM` = 'Yes' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `11:00:00 AM` = 'Yes' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `02:00:00 PM` = 'Yes' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `05:00:00 PM` = 'Yes' THEN 1 ELSE 0 END )  AS total_yes_count, SUM( CASE WHEN `07:00:00 AM` = 'No' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `09:00:00 AM` = 'No' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `11:00:00 AM` = 'No' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `02:00:00 PM` = 'No' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `05:00:00 PM` = 'No' THEN 1 ELSE 0 END ) AS total_no_count FROM `{pdp_table}` WHERE Id = {row_id}"
                            self.cursor.execute(get_yes_count)
                            # live_hours = self.cursor.fetchone()[0]
                            live_hours = self.cursor.fetchone()
                            yes_count = live_hours[0]
                            no_count = live_hours[1]
                            print("Total Yes Count :", yes_count)

                            total_hours = yes_count + no_count

                            Availability = round((yes_count / total_hours) * 100, 1)

                            Items['total hours'] = total_hours
                            Items['Live hours'] = yes_count
                            Items['offline hours'] = no_count
                            Items['Availability'] = Availability

                            yield Items
                            break

                        elif Timeslot in slot_list:
                            print("Going to update only Availability....")
                            Items[Timeslot] = availability

                            print("All slot crawled....")
                            yield Items

                            get_yes_count = f"SELECT SUM( CASE WHEN `07:00:00 AM` = 'Yes' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `09:00:00 AM` = 'Yes' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `11:00:00 AM` = 'Yes' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `02:00:00 PM` = 'Yes' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `05:00:00 PM` = 'Yes' THEN 1 ELSE 0 END ) AS total_yes_count, SUM( CASE WHEN `07:00:00 AM` = 'No' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `09:00:00 AM` = 'No' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `11:00:00 AM` = 'No' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `02:00:00 PM` = 'No' THEN 1 ELSE 0 END ) + SUM( CASE WHEN `05:00:00 PM` = 'No' THEN 1 ELSE 0 END ) AS total_no_count FROM `{pdp_table}` WHERE Id = {row_id}"
                            self.cursor.execute(get_yes_count)
                            # live_hours = self.cursor.fetchone()[0]
                            live_hours = self.cursor.fetchone()
                            yes_count = live_hours[0]
                            no_count = live_hours[1]
                            print("Total Yes Count :", yes_count)

                            total_hours = yes_count + no_count

                            Availability = round((yes_count / total_hours) * 100, 1)

                            Items['total hours'] = total_hours
                            Items['Live hours'] = yes_count
                            Items['offline hours'] = no_count
                            Items['Availability'] = Availability

                            yield Items
                            break


                        else:
                            print("Time Slot Not Available In Table....")

                elif "Oops! We couldn't find products matching" in response.text:
                    update = f"UPDATE {pdp_table} SET Status = 'Not Found' WHERE Id = '{row_id}'"
                    self.cursor.execute(update)
                    self.con.commit()
                    print("No Product Found....")
            
            if not result_find_flag:
                print("Product Name or Unit Not Match...")
                Items['htmlpath'] = path
                Items['Date'] = current_date
                Items['Status'] = "Not Found"

                yield Items

        except Exception as E:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, filename, E, exc_tb.tb_lineno)

            if os.path.exists(path):
                os.remove(path)

    def close(self, spider, reason):
        print("Spider closing...")
        Period = datetime.today().strftime("%p")
        Hour = datetime.today().strftime("%I")
        Timeslot = f'{Hour}:00:00 {Period}'
        print(Timeslot)
        
        
        slot_list = ['07:00:00 AM', '09:00:00 AM', '11:00:00 AM', '02:00:00 PM', '05:00:00 PM']
        
        check_File_pending = f"SELECT COUNT(*) FROM slot_status WHERE STATUS = 'Pending' and Slots = 'File_upload'"
        self.cursor.execute(check_File_pending)
        file_result = self.cursor.fetchone()[0]
        
        index = slot_list.index(Timeslot) + 1
        batch = f"batch_{index}"
        print(batch)
        
        if Timeslot == '05:00:00 PM' and self.upload == 'yes' and file_result == 1:
            check_pending = f"SELECT COUNT(*) FROM {pdp_table} WHERE STATUS = 'Pending'"
            self.cursor.execute(check_pending)
            result = self.cursor.fetchone()[0]
    
            if result == 0:
                
                import requests
                
                url = "https://glacier.xbyte.io/api/feed-process"
                
                payload = {'feed_id': f'3066',
                           'code': f'3066_{new_td}_{batch}',
                           'file_path': f'/mnt/data/Weekly Scheduler/0. Henfruit/Blinkit/CSV/{new_td}',
                           'status': '1'}
                files = []
                headers = {}
                try:
                    response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=10)
                    
                    print(response.text)
                except Exception as e:
                    print(e)
                
                Self_QA = f"""SELECT * FROM `{pdp_table}` WHERE (`Selling Price at 11:00 AM` IS NULL OR
                `MRP at 11:00 AM` IS NULL OR  `07:00:00 AM` IS NULL OR  `09:00:00 AM` IS NULL OR  `11:00:00 AM` IS
                NULL OR  `02:00:00 PM` IS NULL OR  `05:00:00 PM` IS NULL OR  `total hours`
                IS NULL OR  `Live hours` IS NULL OR  `offline hours` IS NULL OR  `Availability` IS NULL) AND STATUS =
                'Done'"""
                self.cursor.execute(Self_QA)
                Self_QA_result = self.cursor.fetchall()
                
                if Self_QA_result == ():
                    print("Going to create Excel File")
                    c = Export_Csv()
                    c.export_excel_keyword()

                else:
                    print("Auto QA Failed....")
                    
                    Self_QA = f"""SELECT Id FROM `{pdp_table}` WHERE (`Selling Price at 11:00 AM` IS NULL OR
                                   `MRP at 11:00 AM` IS NULL OR  `07:00:00 AM` IS NULL OR  `09:00:00 AM` IS NULL OR  `11:00:00 AM` IS
                                   NULL OR  `02:00:00 PM` IS NULL OR  `05:00:00 PM` IS NULL OR  `total hours`
                                   IS NULL OR  `Live hours` IS NULL OR  `offline hours` IS NULL OR  `Availability` IS NULL) AND STATUS =
                                   'Done'"""
                        
                    self.cursor.execute(Self_QA)
                    brand_list = [column for column in self.cursor.fetchall()]
                    for ii in brand_list:
                        Id = ii[0]
                        Update_Self_QA = f"""UPDATE {pdp_table} SET Status = 'Not Found' WHERE Id = '{Id}'"""
                        print(Update_Self_QA)
                        self.cursor.execute(Update_Self_QA)
                        self.con.commit()
                    time.sleep(10)

            else:
                print("Somthing Remaining in last slot...")

        elif Timeslot in slot_list and self.upload == 'yes' and file_result == 1:

            check_pending = f"SELECT COUNT(*) FROM {pdp_table} WHERE STATUS = 'Pending'"
            self.cursor.execute(check_pending)
            result = self.cursor.fetchone()[0]

            if result == 0:
                print("Going to create Excel File As Per Slot Wise.....")
                c = Export_Csv()
                c.export_excel_keyword()
                #
                import requests
                
                url = "https://glacier.xbyte.io/api/feed-process"
                
                payload = {'feed_id': f'3066',
                           'code': f'3066_{new_td}_{batch}',
                           'file_path': f'/mnt/data/Weekly Scheduler/0. Henfruit/Blinkit/CSV/{new_td}',
                           'status': '1'}
                files = []
                headers = {}
                try:
                    response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=10)
                    
                    print(response.text)
                except Exception as e:
                    print(e)
                

            
            else:
                print("Somthing Remaining in last slot...")

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl blinkit -a start=1 -a end=2000 -a upload=yes".split())
