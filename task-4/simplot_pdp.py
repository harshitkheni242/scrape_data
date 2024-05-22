import json
import requests
from config import get_mongo_connection
import hashlib
import os
import threading
import time
from parsel import Selector

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'visitor_id486711=444754809; visitor_id486711-hash=044228762a1d7cd9125a6cb2d626f457074a88f706d9a4ec82e22ea39b2573096caab1c0622d95eeb29fab520fba9f15ccdcfd5b; CookieConsent={stamp:%27d3UPvwvcvXxLKxdb9EKgDRGim35wSOIjMoTtxPWiFREFvdCJdBzXCw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:7%2Cutc:1715321560795%2Cregion:%27in%27}; NEXT_REGION=us; NEXT_LOCALE=en; _gcl_au=1.1.791798221.1715322168; __ncuid=1c96aaac-7852-467e-aa7a-ed3a7512b3e7; _hjSessionUser_1568514=eyJpZCI6IjY4MmM0YmMzLTgzMzUtNTJkMy05OTE0LWE0ZTE0MmY1MTU2ZSIsImNyZWF0ZWQiOjE3MTUzMjIxNjkwNDAsImV4aXN0aW5nIjp0cnVlfQ==; _fbp=fb.1.1715333245688.870078773; _gid=GA1.2.72501047.1715584298; _hjSession_1568514=eyJpZCI6IjMyZWEzYzFmLWU1MDktNDIzMi04MDhiLTk4N2Q2ZDliZDg2MSIsImMiOjE3MTU1OTk1NTk0MDcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; 57942=; 58312=; 58313=; 59942=; 57928=; 58306=; 59941=; 57927=; 57941=; 58305=; _ga=GA1.2.1758873249.1715228388; _ga_VQHQQPW9Y9=GS1.1.1715599558.5.1.1715605958.0.0.0',
    'if-none-match': 'W/"a4763fe39373401f73fb7c9452cdcd35-ssl-df"',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}
collection_category, collection_product_link, collection_product_pdp = get_mongo_connection()

fetch_link = collection_product_link.find({})

for link in fetch_link:
    product_url = link.get("product_links")
    response = requests.get(product_url, headers=headers)
    html_path = os.path.join(os.getcwd(), "simplot_pdp")

    try:
        if not os.path.exists(html_path):
            os.makedirs(html_path)
    except Exception as e:
        print(e)
    category = link.get("categorys")
    sub_categorys = link.get("subactegory")

    if response.status_code == 200:
        pdp = Selector(response.text)
        product_details = pdp.xpath("//script[@id='__NEXT_DATA__']/text()").get('')
        product_details_json = json.loads(product_details)
        try:
            title = product_details_json['props']['pageProps']['breadcrumbs'][1]['title']
        except:
            title = ''
        try:
            product_images = []
            sku = product_details_json['props']['pageProps']['product']['sku']
            for image in product_details_json['props']['pageProps']['product']['productImages']:
                product_image = f'https://www.simplotfoods.com/_next/image?url=https%3A%2F%2Fsimplotfoodgroup.azureedge.net%2Ffood_group%2F1200_1200%2F{sku}_{image}.jpg&w=640&q=75'
                product_images.append(product_image)
            product_image_first = product_images[0]
            product_image_second = "|".join(product_images[1:])

        except:
            sku = ''
            product_image = ''

        try:
            cut_size = product_details_json['props']['pageProps']['product']['productSectionMarketingDetails']['cutSize']

        except:
            cut_size = ''

        try:
            pack_size = product_details_json['props']['pageProps']['product']['productSectionMarketingDetails']['casePackDescription']
        except:
            pack_size = ''

        try:
           product_descriptions = product_details_json['props']['pageProps']['product']['productSectionMarketingDetails']['generalDescription']
        except:
            product_descriptions = ''

        try:
            product_brand = product_details_json['props']['pageProps']['product']['primaryBrand']['name']
        except:
            product_brand = ''

        try:
            product_gross_weight = product_details_json['props']['pageProps']['product']['productSectionSpecifications']['grossWeight']
        except:
            product_gross_weight = ''

        try:
            product_net_weight = product_details_json['props']['pageProps']['product']['productSectionSpecifications']['netWeight']
        except:
            product_net_weight = ''

        try:
            product_manufactureCountry = product_details_json['props']['pageProps']['product']['productSectionSpecifications']['manufactureCountry']
        except:
            product_manufactureCountry = ''

        try:

            product_benefits = "|".join(product_details_json['props']['pageProps']['product']['productSectionMarketingDetails']['benefits'])

        except:
            product_benefits = ''

        try:
            product_specifications = \
            product_details_json['props']['pageProps']['product']['productSectionSpecifications'][
                'specificationFlagsCollection']['items']
            specifications = []
            for p_s in product_specifications:
                specifications.append(p_s['title'])
        except KeyError:
            specifications = []

        Specifications = {}
        for spec in specifications:
            try:
                Specifications[spec] = 'Yes'
            except KeyError:
                Specifications[spec] = None



                                                 ########## Shipping & Storage  ########


        try:
            shipping_storage_width = product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['width']
            shipping_storage_width_uom = shipping_storage_width + product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['widthUoM']

        except:
            shipping_storage_width_uom = ''

        try:
            shipping_storage_length = product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['length']
            shipping_storage_length_uom = shipping_storage_length + product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['lengthUoM']

        except:
            shipping_storage_length_uom = ''

        try:
            shipping_storage_height = product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['height']
            shipping_storage_height_uom = shipping_storage_height + product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['heightUoM']

        except:
            shipping_storage_height_uom = ''

        try:
            shipping_storage_caseCube = product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['caseCube']

        except:
            shipping_storage_caseCube = ''

        try:
            shipping_storage_tixHi = product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['tixHi']

        except:
            shipping_storage_tixHi = ''

        try:
            shipping_storage_shelfLife = product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['shelfLife']

        except:
            shipping_storage_shelfLife = ''

        try:
            shipping_storage_storageTempHigh = product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['storageTempHigh']
            shipping_storage_storageTempHigh_uom = shipping_storage_storageTempHigh+'°'+product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['storageTempUoM']

        except:
            shipping_storage_storageTempHigh = ''

        try:
            shipping_storage_storageTempLow = product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['storageTempLow']
            shipping_storage_storageTempLow_uom = shipping_storage_storageTempLow+'°'+product_details_json['props']['pageProps']['product']['productSectionShippingStorage']['storageTempUoM']

        except:
            shipping_storage_storageTempLow = ''

        try:
            Storage_Temp_From_To = shipping_storage_storageTempLow_uom+"/"+shipping_storage_storageTempHigh_uom

        except:
            shipping_storage_low_high = ''


        try:
            preparation1  = product_details_json['props']['pageProps']['product']['productSectionPreparation']['description']
        except:
            shipping_storage_shelfLife = ''


        preparation = []
        try:
            for i in product_details_json['props']['pageProps']['product']['productSectionPreparation']['prepInstructionsCollection']['items']:
               preparation.append(i['method']['name'])

        except:
            preparation = []

        Preparation = {}
        for pre in preparation:
            try:
                for bullet in product_details_json['props']['pageProps']['product']['productSectionPreparation']['prepInstructionsCollection']['items']:
                    Preparation[pre] = "|".join(bullet["bullets"])

            except KeyError:
                Preparation[pre] = None



                                                     #############   Ingredients & Nutrition   ############

        try:
            ingredients_and_nutrition_ingredients = product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['ingredients']


        except:
             ingredients_and_nutrition_ingredients = ''



        try:
            ingredients_and_nutrition_serving_suggestion = product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['servingSuggestion']

        except:
            ingredients_and_nutrition_serving_suggestion = ''


        try:
            ingredients_and_nutrition_serving_size = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['householdServingSize']
        except:
            ingredients_and_nutrition_serving_size = ''

        try:
            ingredients_and_nutrition_serving_per_container = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['averageServingsPerCase']
        except:
            ingredients_and_nutrition_serving_per_container = ''

        try:
            ingredients_and_nutrition_calories = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['Calories']
        except:
            ingredients_and_nutrition_calories = ''

        try:
            ingredients_and_nutrition_totalFat_amount_per_serving = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['totalFat'] + product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['totalFatUom']
        except:
            ingredients_and_nutrition_totalFat_amount_per_serving = ''


        try:
            ingredients_and_nutrition_total_fat_daily_values = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['totalFatPctDv']+"%"
        except:
            ingredients_and_nutrition_total_fat_daily_values = ''

        try:
            ingredients_and_nutrition_total_fat_saturated_fat_amount_per_serving = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['saturatedFat'] + product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['saturatedFatUom']

        except:
            ingredients_and_nutrition_total_fat_saturated_fat_amount_per_serving = ''

        try:
            ingredients_and_nutrition_total_fat_saturated_fat_daily_values = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['saturatedFatPctDv']+"%"
        except:
            ingredients_and_nutrition_total_fat_saturated_fat_daily_values = ''


        try:
            ingredients_and_nutrition_total_fat_trans_fat_amount_per_serving = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['transFat']+"g"

        except:
            ingredients_and_nutrition_total_fat_trans_fat_amount_per_serving = ''

        try:
            ingredients_and_nutrition_cholesterol_amount_per_serving = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['cholesterol']+"mg"

        except:
            ingredients_and_nutrition_cholesterol_amount_per_serving = ''

        try:
            ingredients_and_nutrition_cholesterol_daily_values = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['cholesterolPctDv']+"%"

        except:
            ingredients_and_nutrition_cholesterol_daily_values = ''

        try:
            ingredients_and_nutrition_sodium_amount_per_serving = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['sodium']+"mg"

        except:
            ingredients_and_nutrition_sodium_amount_per_serving = ''

        try:
            ingredients_and_nutrition_sodium_daily_values = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['sodiumPctDv']+"%"

        except:
            ingredients_and_nutrition_sodium_daily_values = ''


        try:
            ingredients_and_nutrition_total_carbohydrate_amount_per_serving = \
            product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition']['totalCarbohydrate']+"g"

        except:
            ingredients_and_nutrition_total_carbohydrate_amount_per_serving = ''

        try:
            ingredients_and_nutrition_total_carbohydrate_daily_values = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'totalCarbohydratePctDv'] + "%"

        except:
            ingredients_and_nutrition_total_carbohydrate_daily_values = ''

        try:
            ingredients_and_nutrition_total_carbohydrate_dietary_fiber_amount_per_serving = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'dietaryFiber'] + "g"

        except:
            ingredients_and_nutrition_total_carbohydrate_dietary_fiber_amount_per_serving = ''

        try:
            ingredients_and_nutrition_total_carbohydrate_dietary_fiber_daily_values = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'dietaryFiberPctDv'] + "%"

        except:
            ingredients_and_nutrition_total_carbohydrate_dietary_fiber_daily_values = ''


        try:
            ingredients_and_nutrition_total_carbohydrate_total_sugars_added_sugars_amount_per_serving = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'totalSugars'] + "g"

        except:
            ingredients_and_nutrition_total_carbohydrate_total_sugars_added_sugars_amount_per_serving = ''


        try:
            ingredients_and_nutrition_total_carbohydrate_total_sugars_added_sugars_daily_values = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'addedSugarPctDv'] + "%"

        except:
            ingredients_and_nutrition_total_carbohydrate_total_sugars_added_sugars_daily_values = ''


        try:
            ingredients_and_nutrition_protein_amount_per_serving = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'protein'] + "g"

        except:
            ingredients_and_nutrition_protein_amount_per_serving = ''

        try:
            ingredients_and_nutrition_vitamin_d_amount_per_serving = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'vitaminD'] + "mcg"

        except:
            ingredients_and_nutrition_vitamin_d_amount_per_serving = ''

        try:
            ingredients_and_nutrition_vitamin_d_daily_values = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'vitaminDPctDv'] + "%"

        except:
            ingredients_and_nutrition_vitamin_d_daily_values = ''


        try:
            ingredients_and_nutrition_calcium_amount_per_serving = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'calcium'] + "mg"

        except:
            ingredients_and_nutrition_calcium_amount_per_serving = ''

        try:
            ingredients_and_nutrition_calcium_daily_values = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'calciumPctDv'] + "%"

        except:
            ingredients_and_nutrition_calcium_daily_values = ''

        try:
            ingredients_and_nutrition_iron_amount_per_serving = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'iron'] + "mg"

        except:
            ingredients_and_nutrition_iron_amount_per_serving = ''

        try:
            ingredients_and_nutrition_iron_daily_values = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'ironPctDv'] + "%"

        except:
            ingredients_and_nutrition_iron_daily_values = ''

        try:
            ingredients_and_nutrition_potassium_amount_per_serving = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'potassium'] + "mg"

        except:
            ingredients_and_nutrition_potassium_amount_per_serving = ''

        try:
            ingredients_and_nutrition_potassium_daily_values = \
                product_details_json['props']['pageProps']['product']['productSectionIngredientsNutrition'][
                    'potassiumPctDv'] + "%"

        except:
            ingredients_and_nutrition_potassium_daily_values = ''


        hashid = str(
            int(hashlib.md5(bytes(str(category) + str(sub_categorys) + str(title) + str(product_url) + str(sku), "utf8")).hexdigest(),
                32) % (
                    10 ** 32))

        try:
            full_html_path = os.path.join(html_path, f"{hashid}.html")
            if os.path.exists(full_html_path):
                with open(full_html_path, 'r', encoding='utf8') as f:
                    html_response = f.read()
            else:
                response1 = requests.get(product_url, headers=headers)
                print(response1.status_code)
                html_response = response1.text
                if response1.status_code == 200:
                    with open(full_html_path, 'w', encoding='utf8') as f:
                        f.write(html_response)
                    print("File Saved!.")
                else:
                    print("Getting Response issue... ")
                    exit(0)
        except Exception as e:
            print(e)



        try:
            collection_product_pdp.insert_one({
                "categorys": category,
                "subcategorys": sub_categorys,
                "product_links" : product_url,
                "product_name" : title,
                "product_first_image" : product_image_first,
                "product_second_image" : product_image_second,
                "product_sku" : sku,
                "cut_size" : cut_size,
                "pack_size" : pack_size,
                "description" : product_descriptions,
                "specifications_brand" : product_brand,
                "specifications_weight_gross" : product_gross_weight,
                "specifications_weight_net" : product_net_weight,
                "specifications_manufacturing_country" : product_manufactureCountry,
                "Specifications": Specifications,
                "shipping_&_storage_length": shipping_storage_length_uom,
                "shipping_&_storage_width": shipping_storage_width_uom,
                "shipping_&_storage_height": shipping_storage_height_uom,
                "shipping_&_storage_case_cube": shipping_storage_caseCube,
                "shipping_&_storage_tixhi": shipping_storage_tixHi,
                "shipping_&_storage_shelf_life": shipping_storage_shelfLife,
                "shipping_&_storage_temp_from/to": Storage_Temp_From_To,
                "preparation": preparation1,
                "preparation_and": Preparation,
                "ingredients_and_nutrition_ingredients": ingredients_and_nutrition_ingredients,
                "ingredients_and_nutrition_serving_suggestion": ingredients_and_nutrition_serving_suggestion,
                "ingredients_and_nutrition_serving_size": ingredients_and_nutrition_serving_size,
                "ingredients_and_nutrition_servings_per_container": ingredients_and_nutrition_serving_per_container,
                "ingredients_and_nutrition_calories": ingredients_and_nutrition_calories,
                "ingredients_and_nutrition_total_fat_amount_per_serving": ingredients_and_nutrition_totalFat_amount_per_serving,
                "ingredients_and_nutrition_total_fat_daily_values": ingredients_and_nutrition_total_fat_daily_values,
                "ingredients_and_nutrition_total_fat_saturated_fat_amount_per_serving": ingredients_and_nutrition_total_fat_saturated_fat_amount_per_serving,
                "ingredients_and_nutrition_total_fat_saturated_fat_daily_values": ingredients_and_nutrition_total_fat_saturated_fat_daily_values,
                "ingredients_and_nutrition_total_fat_trans_fat_amount_per_serving": ingredients_and_nutrition_total_fat_trans_fat_amount_per_serving,
                "ingredients_and_nutrition_cholesterol_amount_per_serving": ingredients_and_nutrition_cholesterol_amount_per_serving,
                "ingredients_and_nutrition_cholesterol_daily_values": ingredients_and_nutrition_cholesterol_daily_values,
                "ingredients_and_nutrition_sodium_amount_per_serving": ingredients_and_nutrition_sodium_amount_per_serving,
                "ingredients_and_nutrition_sodium_daily_values": ingredients_and_nutrition_sodium_daily_values,
                "ingredients_and_nutrition_total_carbohydrate_amount_per_serving": ingredients_and_nutrition_total_carbohydrate_amount_per_serving,
                "ingredients_and_nutrition_total_carbohydrate_daily_values": ingredients_and_nutrition_total_carbohydrate_daily_values,
                "ingredients_and_nutrition_total_carbohydrate_dietary_fiber_amount_per_serving": ingredients_and_nutrition_total_carbohydrate_dietary_fiber_amount_per_serving,
                "ingredients_and_nutrition_total_carbohydrate_dietary_fiber_daily_values": ingredients_and_nutrition_total_carbohydrate_dietary_fiber_daily_values,
                "ingredients_and_nutrition_total_carbohydrate_total_sugars_added_sugars_amount_per_serving": ingredients_and_nutrition_total_carbohydrate_total_sugars_added_sugars_daily_values,
                "ingredients_and_nutrition_total_carbohydrate_total_sugars_added_sugars_daily_values": ingredients_and_nutrition_total_carbohydrate_total_sugars_added_sugars_daily_values,
                "ingredients_and_nutrition_protein_amount_per_serving": ingredients_and_nutrition_protein_amount_per_serving,
                "ingredients_and_nutrition_vitamin_d_amount_per_serving": ingredients_and_nutrition_vitamin_d_amount_per_serving,
                "ingredients_and_nutrition_vitamin_d_daily_values": ingredients_and_nutrition_vitamin_d_daily_values,
                "ingredients_and_nutrition_calcium_amount_per_serving": ingredients_and_nutrition_calcium_amount_per_serving,
                "ingredients_and_nutrition_calcium_daily_values": ingredients_and_nutrition_calcium_daily_values,
                "ingredients_and_nutrition_iron_amount_per_serving": ingredients_and_nutrition_iron_amount_per_serving,
                "ingredients_and_nutrition_iron_daily_values": ingredients_and_nutrition_iron_daily_values,
                "ingredients_and_nutrition_potassium_amount_per_serving": ingredients_and_nutrition_potassium_amount_per_serving,
                "ingredients_and_nutrition_potassium_daily_values": ingredients_and_nutrition_potassium_daily_values,
                "hashid": hashid

            })
            collection_product_pdp.create_index("hashid", unique=True)
            print("##### Inserted Data ######")
        except Exception as e:
            print(e)



    else:
        print("Status code Error ", response.status_code)

