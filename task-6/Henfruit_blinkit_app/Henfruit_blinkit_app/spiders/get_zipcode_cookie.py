# Address Prediction Requests
import json
import requests
from urllib.parse import quote
from Henfruit_blinkit_app.pipelines import *
def Get_Latitude_Longitude(Region, City, Pincode, Group):
    location_search_string = quote(f"{Region} {City} {Pincode} {Group}")
    print(location_search_string)

    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?key=AIzaSyArrRa3Syd1a1oHvAcTmqk4RX1jGBEYyt4&language=en-US&input={location_search_string}&locationrestriction=rectangle%3A6.462699900000000%2C68.109700000000000%7C35.513327000000000%2C97.395358699999990&components=country%3Ain&sessiontoken=5188ba23-3072-44a5-aafe-c64e5998b1ce"

    headerse = {
    'accept-encoding': 'gzip',
    'connection': 'Keep-Alive',
    'host': 'maps.googleapis.com',
    'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)',
    'x-android-cert': '5B7F42A4B014511E44C93F201C2DFA35CAC44FEE',
    'x-android-package': 'com.grofers.customerapp',
    'x-places-android-sdk': '3.0.0',

    }

    address_prediction_res = requests.get(url,headers=headerse)
    # print(address_prediction_res.text)
    print(address_prediction_res.status_code)
    if 'ZERO_RESULTS' not in address_prediction_res.text:
        address_prediction_json = json.loads(address_prediction_res.text)
        
        place_id = address_prediction_json['predictions'][0]['place_id']
        print("Place Id:",place_id)
        
        title = quote(address_prediction_json['predictions'][0]['structured_formatting']['main_text'])
        print("Place Title:",title)
        
        second_title = quote(address_prediction_json['predictions'][0]['structured_formatting']['secondary_text'])
        print("Second Place Title:",second_title)

        location_requests = f'https://api2.grofers.com/v1/location_info?place_id={place_id}&poi=true&title={title}&description={second_title}&is_pin_moved=false'
        # print(location_requests)

        h2 = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'app_api_version': '28',
        'app_client': 'consumer_android',
        'app_version': '80150630',
        'auth_key': '45bff2b1437ff764d5e5b9b292f9771428e18fc40b7f3b7303d196ea84ab4341',
        'battery-level': 'EXCELLENT',
        'connection': 'keep-alive',
        'cookie': '__cf_bm=PcIjfTINOY11JdB9S2198nJb0wGqDGONie8J0VKBnpg-1697088892-0-AciQpXH7vvNS4UQHaT/dH3uoJIbCr9LOqQU+50eocvLI3cE2x9baagdtOiD1bDv1J/XFDHFZUIoAIxnkYUxHZiA=; path=/; expires=Thu, 12-Oct-23 06:04:52 GMT; domain=.grofers.com; HttpOnly; Secure; SameSite=None',
        'cpu-level': 'AVERAGE',
        'cur_lat': '31.24916',
        'cur_lon': '121.4878983',
        'device_id': '208fbcc06e9d287b',
        'host': 'api2.grofers.com',
        'host_app': 'blinkit',
        'lat': '12.9801076',
        'lon': '77.6428737',

        'storage-level': 'EXCELLENT',
        'user-agent': 'com.grofers.customerapp/280150630 (Linux; U; Android 9; en_US; ASUS_Z01QD; Build/PI; Cronet/114.0.5735.33)',
        'version_name': '15.63.0',
        'x-rider-installed': 'false',
        'x-zomato-installed': 'false'

        }

        web_blocker={
          'http': 'http://wpruthak:2HUyJeBd5s3a@nunblock.oxylabs.io:60000',
          'https': 'http://wpruthak:2HUyJeBd5s3a@unblock.oxylabs.io:60000',
        }
        
        

        web_blocker={
          'http': 'http://brd-customer-hl_4fc8c816-zone-zone_us:33p04eaqxtpu:60000',
          'https': 'http://brd-customer-hl_4fc8c816-zone-zone_us:33p04eaqxtpu:60000',
        }
        
        

        proxy_host = "proxy.zyte.com"
        current_proxy = '5bfb8a7d1d5b4cc0a754ccc2f874b7ac'
        # proxy_port = "8010"
        proxy_port = "8011"
        proxy_auth = f"{current_proxy}:"
        proxies = {
            "http": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
            "https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
        }
        Proxy = 'crawlera'
        h2['x-requested-with'] = "XMLHttpRequest"
        h2['X-Crawlera-Cookies'] = "disable"

        location_requests_res = requests.get(location_requests,headers=h2, proxies=proxies,verify=False)

        print("================ location_requests_res ===================")
        # print(location_requests_res.text)
        print(location_requests_res.status_code)
        location_requests_json = json.loads(location_requests_res.text)


        Latitude = location_requests_json['coordinate']['lat']
        print("Latitude: ",Latitude)
        Longitude = location_requests_json['coordinate']['lon']
        print("Longitude :", Longitude)
        meta = {
          'Latitude': Latitude,
          'Longitude': Longitude,
        }

        return meta
    else:
        meta = {
            'Latitude': "N/A",
            'Longitude': "N/A",
        }

        return meta


if __name__ == '__main__':
    cursor = HenfruitBlinkitAppPipeline.cursor
    con = HenfruitBlinkitAppPipeline.con
    
    brand_select = f"select `Id`, `Latitude`, `Longitude`, `Region`, `City`, `Pin Code`, `Group`, `Product ID`, `Item Name`  from {Input_table}"
    cursor.execute(brand_select)
    brand_list = [column for column in cursor.fetchall()]
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


            if not Longitude and not Latitude:
              
                get_lat_lon = Get_Latitude_Longitude(Region, City, PinCode, Group)
                Latitude = get_lat_lon.get('Latitude')
                Longitude = get_lat_lon.get('Longitude')
                
                update1 = f"UPDATE {Input_table} SET `Latitude`= '{Latitude}', `Longitude`= '{Longitude}' WHERE  `Region` = '{Region}' AND `City` = '{City}' AND `Pin Code` = '{PinCode}' AND `Group` = '{Group}'"
                print(update1)
                cursor.execute(update1)
                con.commit()
                print("Location updated for: %s | %s | %s | %s" % (Region, City, PinCode, Group))
    