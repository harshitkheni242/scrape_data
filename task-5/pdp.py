import json

from bs4 import BeautifulSoup
from fix_busted_json import repair_json

from config import *


def extract_age_group(title_text):
    # Find the titleText element and extract its text
    # title_text = "ハブラシが持てるようになったら『クリニカKid’s ハブラシ 0〜2才用』"

    # Define a regular expression pattern to match age group ranges and their units
    age_group_pattern = r'(\d+〜\d+)(才|歳|ヶ月|ケ月)'

    # Use the regular expression pattern to find the age group in the title text
    age_group_match = re.search(age_group_pattern, title_text)

    if age_group_match:
        age_group_range = age_group_match.group(1)
        age_group_unit = age_group_match.group(2)

        # Print the extracted age group range and unit
        print(f'Age Group Range: {age_group_range}')
        print(f'Age Group Unit: {age_group_unit}')

        return f"{age_group_range} {age_group_unit}"

    else:
        print('Age group not found in the title text')
        return None


def extraction_table_description(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table
    table = soup.find('table')

    # Extract data into a dictionary
    data_dict = {}
    rows = table.find_all('tr')

    # Iterate through each row in the table
    for row in rows:
        # Find all cells in the row
        cells = row.find_all(['th', 'td'])

        # Ensure there are two cells (key and value)
        if len(cells) == 2:
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            data_dict[key] = value

    # Print the dictionary
    # print(data_dict)
    return data_dict


def extraction_table_description_1(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize an empty dictionary to store the data
    data = {}

    # Find all rows in the table
    rows = soup.find_all('tr')

    if len(rows) % 2 == 0:
        start = 0
    else:
        start = 1

    # Iterate over each pair of rows and store data in the dictionary
    for i in range(start, len(rows), 2):
        try:
            # Get the key from the first row in the pair
            key = rows[i].text.strip()

            # Get the value from the second row in the pair
            value = rows[i + 1].text.strip()

            # Store the key-value pair in the dictionary
            data[key] = value
        except:
            ...

    # Print the extracted data dictionary
    print(data)
    return data


def extraction_table_specification(html_content):
    # Parse the HTML content
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a dictionary to store the extracted data
    data_dict = {}

    # Find the main container div
    container_div = soup.find('div', class_='v-card__text pa-0')

    # Iterate through each row in the main container div
    rows = container_div.find_all('div', class_='d-flex flex-nowrap')

    for row in rows:
        # print(row)
        # Find the key and value divs in each row
        key_div = row.find('div', class_='font-weight-bold')
        value_div = row.find('div', class_='black--text text-body-1 px-2 px-sm-4 py-3')

        # Get the text from the key and value divs
        if key_div and value_div:
            key = key_div.get_text(strip=True)
            value = value_div.get_text(strip=True)

            # Add the key-value pair to the dictionary
            data_dict[key] = value

    # Print the dictionary containing the extracted data
    print(data_dict)
    return data_dict


def extract_json_from_script(html_content):
    script_json = str(html_content).split(".init(")[-1].split(");")[0]
    # print(script_json)
    fix_json = repair_json(script_json)
    # print(fix_json)
    return json.loads(fix_json)


def extract_review_data(store_id, page_key):

    # print("Calling review function.....")
    review_path = f"{HTMLs}/Review_{store_id}_{page_key}.html"
    if os.path.exists(review_path):
        with open(review_path, 'r', encoding='utf-8') as f:
            review_respo = f.read()
    else:
        url = f"https://shopping.yahoo.co.jp/review/item/list?store_id={store_id}&page_key={page_key}&sc_i=shp_pc_item_review_c"

        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'B=amrmsndj1cses&b=3&s=vs; A=0tf349lj1cses&sd=A&t=1712746972&u=1712746972&v=1; XA=0tf349lj1cses&sd=A&t=1712746972&u=1712746972&v=1; XB=amrmsndj1cses&b=3&s=vs; __lt__cid=bde92357-1640-4bbb-800c-b548053b90d2; srch_vt=vt=grid&new=; _dgma=cada9060-faee-40f4-89b7-65b460f2f9aa; AMCVS_257D34B852785CAF0A490D44%40AdobeOrg=1; AMCV_257D34B852785CAF0A490D44%40AdobeOrg=1406116232%7CMCIDTS%7C19831%7CMCMID%7C72469413648955053000368333190742417550%7CMCAID%7CNONE%7CMCOPTOUT-1713356652s%7CNONE%7CvVersion%7C2.5.0%7CMCAAMLH-1713954252%7C12%7CMCAAMB-1713954252%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI; cto_bundle=lcxRO180ZkJ6SFFRaHBScUhheWNMZXltTDdOayUyRnBBTkNVdXVKJTJCNDAlMkJ5blpTelpnYmsyam1HeDJ4RFhxdzh0aWJTJTJGN0lFSHFaUFRxWVhVSDA1Zktwdlg0eHl4d0NyYkM1NCUyQnlMUnQ2M1E4enloVXc2cmNsS3EzNnBDVDByYyUyQlV2VDhWOEElMkIwbWljTFFwc3UlMkZRWGV6N0NaWU93JTNEJTNE; CLOSE_EVENT=inc=1713418309; _dgmc=cada9060-faee-40f4-89b7-65b460f2f9aa.1713421776420',
            'if-none-match': '"iuqt43ndbe3jea"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        review_respo = response.text

        if '商品レビューを表示できません' not in review_respo and response.status_code == 200:
            with open(review_path, 'w', encoding='utf-8') as f:
                f.write(review_respo)
            print(f'{GREEN}Review Page Saved....')
        else:
            print(f"{RED}Somthing Went Wrong in Review Request 🡆 Page Key🡆 {page_key} 🡆 Status Code",
                  response.status_code)
            return None

    review_respo_selector = Selector(text=review_respo)
    script_json = review_respo_selector.xpath('//script[@id="__NEXT_DATA__"]//text()').get()
    script_json = json.loads(script_json)

    return script_json


def PL_Extraction(start, end):
    data_list = db_pdp_table.find({"Status": "Pending", }).skip(int(start)).limit(int(end))
    # data_list = db_pdp_table.find({"Id": 8})

    for cat_item in data_list:
        Id = cat_item['Id']
        Url = str(cat_item['product_url'])
        sub_category = str(cat_item['sub_category'])
        retry = int(cat_item['retry'])

        Data_Extraction(Id, Url, retry, sub_category)


def Data_Extraction(Id, Url, retry, sub_category):
    try:
        retry_counter = 0

        hash_utf8 = (str(Url).encode('utf8'))
        prod_save_id = int(hashlib.md5(hash_utf8).hexdigest(), 16)

        filename = f'/PDP_{prod_save_id}.html'
        path = HTMLs + filename
        path = path.replace("\\", "/")

        RESPONSE_FLAG = False
        if os.path.exists(path):
            print(f"{GREEN}HTML Page Exists...")
            RESPONSE_FLAG = True
            with open(path, 'r', encoding="utf-8") as f:
                page_response_data = f.read()
            # return None
        else:

            RESPONSE_COUNT = 0

            while RESPONSE_FLAG == False and RESPONSE_COUNT < 5:
                retry_counter += 1
                retry += 1
                try:
                    page_response = requests.get(url=Url, headers=headers)
                    page_response_data = page_response.text

                    try:
                        timeforlog = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                        log_list = {
                            'URL': f'{Url}',
                            'Proxies': 'VPN',
                            'type': 'Product',
                            'current_time': timeforlog,
                            'status_code': page_response.status_code,
                        }

                        request_log.insert_one(log_list)
                    except Exception as e:
                        print("Error in Mongo Query:", e)

                    selector_response = Selector(text=page_response_data)

                    if selector_response.xpath(
                            '//p[@class="red--text mb-0"]//span[contains(@class,"text-h3 ")]//text()').get() and selector_response.xpath(
                        '//h1[contains(@class,"text-h3")]//text()').get():
                        RESPONSE_FLAG = True
                        with open(path, 'w', encoding="utf-8") as f:
                            f.write(page_response_data)

                        print(f"{GREEN} HTML Page SAVED.....")

                    elif page_response.status_code == 200 and 'class="gd3ColumnItemA"' in page_response_data and '</html>' in page_response_data:

                        RESPONSE_FLAG = True
                        with open(path, 'w', encoding="utf-8") as f:
                            f.write(page_response_data)

                        print(f"{GREEN} HTML Page SAVED.....")
                        # return None
                    elif page_response.status_code == 404 or page_response.status_code == 400 or '商品情報を表示できません' in page_response_data or '日ごろのご愛顧、誠にありがとうございます' in page_response_data or 'ご覧になろうとしているページは現在表示できません' in page_response_data:

                        with open(path, 'w', encoding="utf-8") as f:
                            f.write(page_response_data)

                        d = db_pdp_table.update_one({'Id': int(Id)}, {'$set': {'Status': "Not Found"}})
                        print(f"{GREEN}Updated as a Not Found for ID: ", Id, "-->", d.modified_count)
                        return None
                    else:
                        time.sleep(10)
                        RESPONSE_FLAG = False
                        RESPONSE_COUNT += 1

                except:
                    time.sleep(10)
                    # break

        if not RESPONSE_FLAG:
            print("Getting wrong response after all retry execute..URL: ", Url)
            return None

        else:
            print("Crawling start...")

            if '商品情報を表示できません' in page_response_data or '日ごろのご愛顧、誠にありがとうございます' in page_response_data or 'ご覧になろうとしているページは現在表示できません' in page_response_data:
                d = db_pdp_table.update_one({'Id': int(Id)}, {'$set': {'Status': "Not Found"}})
                print(f"{GREEN}Updated as a Not Found for ID: ", Id, "-->", d.modified_count)
                return None

            selector_response = Selector(text=page_response_data)

            items = {}

            items['htmlpath'] = "path"
            items['country'] = "Japan"
            items['category'] = category_name.replace("_", " ")
            items['platform'] = "Yahoo Shopping"
            if category_name == "Nutraceuticals":
                items['currency'] = "YEN"

            else:
                items['currency'] = "JPY"

            price = selector_response.xpath('//div[@class="elPriceArea"]//span[@class="elPriceNumber"]//text()').get()
            if not price:
                price = selector_response.xpath(
                    '//input[@checked="checked"]//..//span[@class="elPriceNumber"]//text()').get()
                if not price:
                    price = selector_response.xpath(
                        '//p[@class="red--text mb-0"]//span[contains(@class,"text-h3 ")]//text()').get()
                    if not price:
                        print("Price should not be none,....", Url)
                        return None

            items['price'] = float(c_replace(str(price).replace(",", "")))
            # items['price'] = c_replace(str(price))

            P_image = selector_response.xpath('//link[contains(@href,"https://item-shopping.c.yimg.jp/")]/@href').get()
            if not P_image:
                P_image = selector_response.xpath('//img[@class="elPanelImage"]/@src').get()
                if not P_image:
                    print("Prodcut image should not be none...")
                    return None

            if not validate_url(P_image):
                print(f"Image Url is not a valid URL...", P_image)
                return None

            items['image'] = P_image

            cat = selector_response.xpath(
                '//*[contains(text(),"お礼品カテゴリ")]//..//following-sibling::div[@class="elRowData"]//text()').getall()
            if not cat:
                cat = selector_response.xpath(
                    '//*[contains(text(),"商品カテゴリ")]//..//following-sibling::div[@class="elRowData"]//text()').getall()
                if not cat:
                    cat = selector_response.xpath(
                        '//div[@id="bclst"]//a//text()').getall()
                    if not cat:
                        cat = selector_response.xpath(
                            '//div[contains(@class,"d-flex align-center pa-2 pa-sm-0 flex-wrap")]//div//a//text()').getall()
                        if not cat:
                            cat = selector_response.xpath(
                                '//div[@class="d-flex align-center flex-wrap"]//div[@class="d-flex align-center"]//a/text()').getall()

            if cat:
                cat = c_replace(cat)
            else:
                print(f"Category should not be blank...", Url)
                return None

            cat = " > ".join(cat)

            items['breadcrumbs'] = cat

            product_name = selector_response.xpath('//div[@class="mdItemName"]//*[@class="elName"]//text()').get()
            if not product_name:
                product_name = selector_response.xpath('//h1[contains(@class,"text-h3")]//text()').get()
                if not product_name:
                    print("Product Name should not be none...", Url)
                    return None

            items['product_name'] = c_replace(product_name)

            items['sku_size'] = extract_size(product_name)

            brand = selector_response.xpath(
                '//div[@class="mdItemBrand"]//p[@class="elBrand"]//a//text()').getall()
            if not brand:
                brand = selector_response.xpath(
                    '//div[@class="v-card__text text-body-2 text-sm-body-1 black--text pa-0 d-flex align-center"]//a//span[@class="v-btn__content"]//text()').getall()
            if brand:
                brand = " ".join(c_replace(brand))

            else:
                brand = ""

            items['brand_name'] = brand

            product_description = selector_response.xpath('//meta[@property="og:description"]/@content').get()
            if not product_description:
                product_description = selector_response.xpath('//div[@class="mdItemDescription"]//text()').getall()

                if product_description:
                    product_description = c_replace(product_description)

                    for iisd in product_description:
                        items['sku_size'] = extract_size(iisd)

                product_description = " ".join(product_description)
            else:
                items['sku_size'] = extract_size(product_description)

            items['description'] = product_description

            manufacturer = ""
            country_of_origin = ""
            material_type_free = ""
            product_serial_num = ""
            product_ingredients_meta_flag = False
            table_1_falg = True
            html_content = selector_response.xpath(
                '//table[@cellspacing="0" and @width="100%" and @cellpadding="5"]').get()
            if not html_content:
                table_1_falg = False
                html_content = selector_response.xpath(
                    '//script[@type="text/template" and (contains(text(),"商品説明"))]//text()').get()

                if not html_content:
                        # '//script[@type="text/template" and (contains(text(),"製造者"))]//text() or contains(text(),"販売名"))]//text() or contains(text(),"製造国"))]//text()').get()
                    html_content = selector_response.xpath(
                        '//script[@type="text/template" and (contains(text(),"製造者")) or (contains(text(),"内容量")) or (contains(text(),"製造国"))]//text()').get()


            if html_content:

                # print("Going to extract table description.....", Url)
                try:
                    if table_1_falg:
                        product_description2_dict = extraction_table_description_1(html_content)
                    else:
                        product_description2_dict = extraction_table_description(html_content)
                        if not product_description2_dict:
                            product_description2_dict = extraction_table_description_1(html_content)

                    descr2_list = []
                    desc_2_flag = False
                    if product_description2_dict:
                        for k, v in product_description2_dict.items():

                            descr2_list.append(f"{k}: {v}")

                            if ('材料' in k or '全成分' in k) and not product_ingredients_meta_flag:
                                product_ingredients_meta_flag = True
                                items['product_ingredients_meta'] = v

                            elif '説明' in k:
                                desc_2_flag = True
                                product_description2 = v

                            elif '使用方法' in k:
                                material_type_free = v

                            elif '製造' in k or '生産国' in k:
                                country_of_origin = v

                            elif 'メーカー' in k or 'メーカー名' in k:
                                manufacturer = v.split('　')[0]


                            if not items['sku_size']:
                                sku_size = extract_size(v)
                                if sku_size:
                                    items['sku_size'] = sku_size

                        if not desc_2_flag:
                            product_description2 = ", ".join(descr2_list)
                            pattern = r'\\u[0-9]{4}'
                            product_description2 = re.sub(pattern, '', product_description2)


                    else:
                        product_description2 = ""
                except:
                    product_description2 = ""


            elif ',itemKindCd' in page_response_data and ',specList:' in page_response_data:
                print("Going to extract data from lohaco specification...", Url)

                json_str = page_response_data.split(",specList:")[-1].split(",itemKindCd:")[0]
                atoz = 'abcdefghijklmnopqrstuvwxyz'
                for i in atoz:
                    # print(i)
                    json_str = json_str.replace(f',value:{i}', "").replace(f'name:{i},', "").replace(
                        f',value:{i.upper()}', "").replace(f'name:{i.upper()},', "").replace('"' + i + '},',
                                                                                             '"},').replace(
                        '"' + i.upper() + '},', '"},').replace(f'value:{i}', "").replace(f'value:{i.upper()}',
                                                                                         "").replace(
                        f'name:{i.upper()}', "").replace(f'name:{i}', "")

                for i in atoz:
                    # print(i)
                    json_str = json_str.replace(',{'+i+'}', "")

                bad_json = json_str.replace(',"value":_}', "}").replace("{},", "").replace("{q},", "").replace(f',value:$', "").replace(',value: }',
                                                                                                            "}").replace(
                    "items:", '"items":').replace("name:", '"name":').replace("value:", '"value":')

                pattern = r'\\u[0-9]{4}'
                bad_json1 = re.sub(pattern, '', bad_json)
                try:
                    bad_json = repair_json(bad_json1)
                except Exception as e:
                    print("Bad Json 🡆 ➪ ", bad_json1, f"\n{RED}Error For Id 🡆 {Id} 🡆 ➪ ", e)
                    return None
                # print(bad_json)

                product_description2_dict = json.loads(bad_json)
                descr2_list = []
                desc_2_flag = False

                for specs in product_description2_dict['items']:

                    try:
                        k = specs['name']
                    except:
                        continue

                    try:
                        v = specs['value']
                    except:
                        v = ""

                    descr2_list.append(f"{k}: {v}")

                    if ('材料' in k or '成分' in k or '原材料' in k) and not product_ingredients_meta_flag:
                        items['product_ingredients_meta'] = v
                        product_ingredients_meta_flag = True

                    elif '説明' in k:
                        desc_2_flag = True
                        product_description2 = v

                    elif '使用方法' in k:  # 原材料
                        material_type_free = v

                    elif 'JAN' in k or 'ISBN' in k or '商品番号' in k:
                        product_serial_num = v

                    elif '製造' in k or '原産国' in k:
                        country_of_origin = v

                    elif 'メーカー' in k or 'メーカー名' in k:
                        manufacturer = v.split('　')[0]

                    if '内容量' in k and not items['sku_size']:
                        sku_size = extract_size(v)
                        items['sku_size'] = sku_size

                if not desc_2_flag:
                    product_description2 = ", ".join(descr2_list)
                    pattern = r'\\u[0-9]{4}'
                    product_description2 = re.sub(pattern, '', product_description2)


            else:
                product_description2 = selector_response.xpath(
                    '//div[contains(@class, "isItemDescription")]//div[@class="elContent"]//text()').getall()

                if product_description2:
                    product_description2 = c_replace(product_description2)

                if product_description2:
                    product_description2 = c_replace(product_description2)

                    for iisd in product_description2:
                        items['sku_size'] = extract_size(iisd)

                    product_description2 = " ".join(product_description2)

                else:
                    product_description2 = ""

            items['material_type_free'] = material_type_free

            items['description2'] = product_description2

            if not country_of_origin:
                country_of_origin = selector_response.xpath(
                    '//div[contains(text(), "原産国")]//following-sibling::div//text()').get(default="")
                if country_of_origin:
                    country_of_origin = c_replace(country_of_origin)

            items['country_of_origin'] = country_of_origin
            items['place_of_origin'] = country_of_origin

            if not manufacturer:
                manufacturer = selector_response.xpath(
                    '//div[contains(text(),"メーカー名")]//following-sibling::div//text()').get(default="")

            items['manufacturer'] = manufacturer

            meta_ingredients = selector_response.xpath((
                '//p[contains(text(), "用成分と") and (contains(@class,"titleText"))]//..//following-sibling::div[@class="extDetails cfx"]//text()')).getall()
            if meta_ingredients:
                meta_ingredients = " ".join(c_replace(meta_ingredients))
            else:
                meta_ingredients = selector_response.xpath(
                    ('''//div[contains(text(), '＜全成分＞')]/following-sibling::text()''')).getall()

            meta_ingredients = " ".join(c_replace(meta_ingredients)).split("＜全成分＞")[-1]
            if not product_ingredients_meta_flag:
                items['product_ingredients_meta'] = meta_ingredients

            active_ing = selector_response.xpath('//*[contains(text(),"有効成分")]//text()').getall()
            if active_ing:
                active_ing = " ".join(c_replace(active_ing)).strip()
                if active_ing:
                    # if not active_ing.startswith("有効成分") and active_ing.count('有効成分') == 1:
                    active_ing = "有効成分" + active_ing.split("有効成分")[-1]
                    # else:
                    #     print("Somthing Went wrong in active_ingredients...", Url)
                    #     return None
                else:
                    print("Check active_ing...", Url)
                    return None
            else:
                active_ing = ""

            items['active_ingredients'] = active_ing

            if not product_serial_num:
                product_serial_num = selector_response.xpath('//div[@class="elFavorite"]//a/@data-pagekey').get(
                    default="")
                if not product_serial_num:

                    product_serial_num = selector_response.xpath('//link[@rel="canonical"]/@href').get(default="")
                    if not product_serial_num:
                        product_serial_num = selector_response.xpath(
                            '//div[contains(text(),"商品番号")]//following-sibling::div//text()').get(default="")

                        if not product_serial_num:
                            product_serial_num = selector_response.xpath(
                                '//*[contains(text(),"商品コード")]//..//following-sibling::div//p//text()').get(
                                default="")

                            if not product_serial_num:
                                product_serial_num = selector_response.xpath(
                                    '//div[(contains(text(),"ISBN")) or (contains(text(),"JAN"))]//following-sibling::div//text()').get(
                                    default="")

                    else:
                        if 'lohaco' in Url:
                            product_serial_num = product_serial_num.split("/")[-2]
                        else:
                            product_serial_num = product_serial_num.split("page_key=")[-1]

            items['product_serial_num'] = product_serial_num

            # (才|歳|ヶ月|ケ月)
            age_group_title = selector_response.xpath(
                '//p[@class="titleText" and (contains(text(), "才")) or (contains(text(), "歳")) or (contains(text(), "ヶ月")) or (contains(text(), "ケ月"))]//text()').get()
            if age_group_title:
                age_group = extract_age_group(age_group_title)
                if age_group:
                    items['recommended_age'] = age_group
                else:
                    items['recommended_age'] = ""

            else:
                items['recommended_age'] = ""

            store_id = selector_response.xpath('//div[@class="elFavorite"]//a/@data-storeid').get()
            page_key = selector_response.xpath('//div[@class="elFavorite"]//a/@data-pagekey').get()
            avg_rating = ""
            total_review = ""
            if page_key and store_id:
                # print("Found Script json for review...")

                # Call the function to extract JSON data
                review_json = extract_review_data(store_id=store_id, page_key=page_key)
                if not review_json:
                    os.remove(path)
                    return None

                total_review = \
                review_json['props']['pageProps']['pickUpItemReviewEntity']['itemReview']['reviewSummary']['count']

                avg_rating = review_json['props']['pageProps']['pickUpItemReviewEntity']['itemReview']['reviewSummary'][
                    'average']
                if not avg_rating and total_review:
                    try:
                        avg_rating = review_json['props']['pageProps']['reviewEntity']['itemReview']['reviews'][0][
                            'rating']
                    except:
                        if not total_review:
                            avg_rating = ''
                            total_review = ''
                        else:
                            avg_rating = '5.0'

                try:
                    num_reviews = review_json['props']['pageProps']['reviewEntity']['itemReview']['filteredCount']
                except:
                    num_reviews = review_json['props']['pageProps']['reviewEntity']['catalogReview']['filteredCount']

                num_reviews = int(num_reviews)

            else:
                script_json = selector_response.xpath(
                    '//script[@type="application/ld+json" and (contains(text(),"description"))]//text()').get()
                if script_json:
                    print("script_json....")
                    script_json = json.loads(script_json)

                    if 'ratingValue' in str(script_json):
                        rating = script_json['aggregateRating']['ratingValue']
                        if rating:
                            Rating = float(c_replace(rating))
                            Rating = round(Rating, 2)
                            avg_rating = str(Rating)
                        else:
                            avg_rating = '0'

                        total_review = script_json['aggregateRating']['reviewCount']

                num_reviews = ""

            if (not avg_rating and total_review or avg_rating and not total_review):
                print("Somthing went wrong in review code,,,,,,", Url)
                return None

            elif avg_rating and total_review:

                items['avg_rating'] = float(avg_rating)
                items['num_ratings'] = int(total_review)
                items['num_reviews'] = num_reviews

            items['input_category'] = sub_category
            items['Status'] = "Done"

            d = db_pdp_table.update_one({"Id": int(Id)}, {"$set": items})
            print(f"{GREEN}Product Table Updated Successfully for Id 🡆 {Id} 🡆 ➪", d.modified_count)

    except Exception as e:
        print(f"{RED}Error For Id 🡆 {Id} 🡆 ➪", e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


if __name__ == '__main__':
    start = 0
    end = 1
    # PL_Extraction(start, end)
    # exit()
    import time

    # exit(0)
    print(f"{GREEN}----- Main open ------- ")
    retry = 0
    while db_pdp_table.count_documents({'Status': 'Pending'}) != 0 and retry < 1:
        total_count = db_pdp_table.count_documents({'Status': 'Pending'})
        print("Total Pending Count ---> ", total_count)
        if total_count >= 100:
            variable_count = total_count // 100
        else:
            variable_count = total_count // total_count

        if variable_count == 0:
            variable_count = total_count ** 2

        count = 1
        threads = [Thread(target=PL_Extraction, args=(i, variable_count)) for i in
                   range(0, total_count, variable_count)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        retry += 1
        print(f"{GREEN}--------- Thread Ends ----------- ")
        # time.sleep(5)

    else:
        print("Something pending in Inputs")
        time.sleep(20)