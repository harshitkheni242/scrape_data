if __name__ == '__main__':

    import pymysql
    from DRP_Esteelauder.pipelines import *
    from DRP_Esteelauder.config import *
    try:
        print('Connection Creating....')
        con = pymysql.connect(host=db_host, user=db_user, password=db_passwd, database=db_name, autocommit=True,
                              use_unicode=True, charset="utf8")
        cursor = con.cursor()
        brand_select = f"select `Id`, `Domain_url`, `Country_Name` from {Domain_table} where Status = 'Pending'"
        cursor.execute(brand_select)
        brand_list = [column for column in cursor.fetchall()]
        if not brand_list:
            print("...................Getting empty Result.................")
        else:
            for i in brand_list:
                row_id = i[0]
                Domain_url = i[1]
                Country_Name = i[2]

                if Country_Name == 'New Zealand':
                        continue
                elif Country_Name == 'Argentina' or \
                        Country_Name == 'Colombia' or \
                        Country_Name == 'Venezuela' or \
                        Country_Name == 'Portugal' or \
                        Country_Name == 'Middle East' or \
                        Country_Name == 'Phillipines':
                    update = f"UPDATE {Domain_table} SET status = 'Not Found' Where Id = '{row_id}'"
                    cursor.execute(update)
                    con.commit()
                    print("Domain Table Updated as Not Found...")
                    continue


                filename = f'/main_{Country_Name}.html'
                path = HTML + filename
                path = path.replace("\\", "/")

                delete = f"DELETE FROM {category_table} WHERE `cat_id` = '{row_id}'"
                cursor.execute(delete)
                con.commit()

                import re
                import requests

                if str(Domain_url).endswith("com.cn"):
                    sitemape_url = f'{Domain_url}/sitemap-0.xml'
                else:
                    sitemape_url = f'{Domain_url}/sitemap.xml'

                print(sitemape_url)

                urllist = [sitemape_url]

                mfg_list = []
                for k in urllist:
                    if os.path.exists(path):
                        with open(path,'r',encoding='utf-8') as f:
                            res = f.read()
                    else:
                        r = requests.get(k)
                        res = r.text
                        with open(path,'w',encoding='utf-8') as f:
                            f.write(res)

                    if res:
                        lss = re.findall('<loc>(.*?)</loc>', res)
                        for kk in lss:
                            mfg_list.append(kk)
                    else:
                        print(k, "wrong response")

                category_flag = False
                counter = 0
                for category_url in mfg_list:

                    if category_url.startswith(f'{Domain_url}/products'):
                        category_flag = True
                        print(category_url)
                        if Domain_url not in category_url:
                            category_url = Domain_url + category_url

                        import urllib.parse
                        category_url = urllib.parse.unquote_plus(category_url)
                        counter += 1
                        print(category_url)
                        try:
                            insert = f"""INSERT INTO `{category_table}`(`Id1`, `Cat_Url`,`Domain_url`,`Country_Name`)
                                                                            VALUES ('{row_id}','{category_url}','{Domain_url}','{Country_Name}')"""
                            cursor.execute(insert)
                            con.commit()
                        except Exception as e:
                            if 'Duplicate' not in str(e):
                                print(e)
                                exit(0)


                if category_flag:
                    update = f"UPDATE {Domain_table} SET status = 'Done',`Category_count`= '{counter}' Where Id = '{row_id}'"
                    cursor.execute(update)
                    con.commit()
                    print("Domain Table Updated as Done...")
                else:
                    update = f"UPDATE {Domain_table} SET status = 'Not Found' Where Id = '{row_id}'"
                    cursor.execute(update)
                    con.commit()
                    print("Domain Table Updated as Not Found...")
    except Exception as e:
        print(e)

