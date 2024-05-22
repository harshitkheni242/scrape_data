# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from Henfruit_blinkit_app.config import *
from Henfruit_blinkit_app.items import *


class HenfruitBlinkitAppPipeline:
    try:
        print('hello')
        con = pymysql.connect(host=db_host, user=db_user, password=db_passwd)
        db_cursor = con.cursor()
        create_db = f"create database if not exists `{db_name}` CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci"
        db_cursor.execute(create_db)
        con = pymysql.connect(host=db_host, user=db_user, password=db_passwd, database=db_name, autocommit=True,
                              use_unicode=True, charset="utf8")
        cursor = con.cursor()
        # create branch table

        try:
            # # todo ----> Set Input table Status Pending before create new table <------
            slot_list = ['07:00:00 AM', '09:00:00 AM', '11:00:00 AM', '02:00:00 PM', '05:00:00 PM']

            Period = datetime.today().strftime("%p")
            Hour = datetime.today().strftime("%I")

            Timeslot = f'{Hour}:00:00 {Period}'

            check_status = f"SELECT Status FROM `slot_status` WHERE Slots = '{Timeslot}'"
            cursor.execute(check_status)
            status_result = cursor.fetchone()[0]

            stmt = f"SHOW TABLES LIKE '{pdp_table}'"
            cursor.execute(stmt)
            result = cursor.fetchone()

            if not result or str(status_result).lower() == 'pending':
                if not result:
                    banner_sql1 = f'''update  `slot_status` set Status = "Pending"'''
                    # print(banner_sql)
                    cursor.execute(banner_sql1)
                    con.commit()

                if str(status_result).lower() == 'pending':
                    banner_sql = f'''update  `{pdp_table}` set Status = "Pending"'''
                    # print(banner_sql)
                    cursor.execute(banner_sql)
                    con.commit()
                    banner_sql1 = f'''update  `slot_status` set Status = "Done" where Slots = "{Timeslot}"'''
                    # print(banner_sql)
                    cursor.execute(banner_sql1)
                    con.commit()
                    
                    banner_sql2 = f'''update  `slot_status` set Status = "Pending" where Slots = "File_upload"'''
                    # print(banner_sql)
                    cursor.execute(banner_sql2)
                    con.commit()

            create_table_pdp_review_res = "create table if not exists " + Input_table + """ (
                                                                `Id` int(11) NOT NULL AUTO_INCREMENT,
                                                                `Status` varchar(20) DEFAULT 'Pending',
                                                                `htmlpath` varchar(500) DEFAULT NULL,
                                                                `Latitude` varchar(50) DEFAULT NULL,
                                                                `Longitude` varchar(50) DEFAULT NULL,
                                                                `Region` varchar(50) DEFAULT NULL,
                                                                `City` varchar(50) DEFAULT NULL,
                                                                `Pin Code` varchar(50) DEFAULT NULL,
                                                                `Group` varchar(50) DEFAULT NULL,
                                                                `Product ID` varchar(50) DEFAULT NULL, 
                                                                `Item Name` varchar(150) DEFAULT NULL,
                                                                `Item Link` varchar(150) DEFAULT NULL,
                                                                PRIMARY KEY (`Id`),
                                                                KEY `NewIndex2` (`Status`)
                                                              ) ENGINE=MyISAM DEFAULT CHARSET=utf8"""
            cursor.execute(create_table_pdp_review_res)

        except Exception as e:
            print(e)

        try:

            create_table_pdp_review_res6 = "create table " + pdp_table + """ (
                                                                `Id` int(11) NOT NULL AUTO_INCREMENT,
                                                                `Status` varchar(20) DEFAULT 'Pending',
                                                                `htmlpath` varchar(500) DEFAULT NULL,
                                                                `Latitude` varchar(50) DEFAULT NULL,
                                                                `Longitude` varchar(50) DEFAULT NULL,
                                                                `Date` varchar(50) DEFAULT NULL,
                                                                `Region` varchar(50) DEFAULT NULL,
                                                                `City` varchar(50) DEFAULT NULL,
                                                                `Pin Code` varchar(50) DEFAULT NULL,
                                                                `Group` varchar(50) DEFAULT NULL,
                                                                `Product ID` varchar(50) DEFAULT NULL, 
                                                                `Product ID1` varchar(50) DEFAULT NULL, 
                                                                `Merchant Id` varchar(50) DEFAULT NULL, 
                                                                `Item Name` varchar(150) DEFAULT NULL,
                                                                `Item Name1` varchar(150) DEFAULT NULL,
                                                                `Item Link` varchar(150) DEFAULT NULL,
                                                                `Selling Price at 11:00 AM` varchar(50) DEFAULT NULL,
                                                                `MRP at 11:00 AM` varchar(50) DEFAULT NULL,
                                                                `Discount running` varchar(50) DEFAULT NULL,
                                                                `Disc %` varchar(50) DEFAULT NULL,
                                                                `07:00:00 AM` varchar(50) DEFAULT NULL,
                                                                `09:00:00 AM` varchar(50) DEFAULT NULL,
                                                                `11:00:00 AM` varchar(50) DEFAULT NULL,
                                                                `02:00:00 PM` varchar(50) DEFAULT NULL,
                                                                `05:00:00 PM` varchar(50) DEFAULT NULL,
                                                                `total hours` varchar(50) DEFAULT NULL,
                                                                `Live hours` varchar(50) DEFAULT NULL,
                                                                `offline hours` varchar(50) DEFAULT NULL,
                                                                `Availability` varchar(50) DEFAULT NULL,
                                                                PRIMARY KEY (`Id`),
                                                                KEY `NewIndex2` (`Status`)
                                                              ) ENGINE=MyISAM DEFAULT CHARSET=utf8"""
            cursor.execute(create_table_pdp_review_res6)
            insert = f"""INSERT INTO {pdp_table} (`Latitude`, `Longitude`, `Region`, `City`, `Pin Code`, `Group`, `Product ID`, `Item Name`, `Item Link`)
                        SELECT `Latitude`, `Longitude`, `Region`, `City`, `Pin Code`, `Group`, `Product ID`, `Item Name`, `Item Link` FROM {Input_table}"""
            cursor.execute(insert)
            con.commit()


        except Exception as e:
            print(e)

    except Exception as e:
        print("There is some issue", e)

    def process_item(self, item, spider):
        if isinstance(item, PDP_Item):
            print("  ******* Running Update Query *******  ")
            try:
                s = ''
                for key in item:
                    values = str(item[key]).replace('"', "'")
                    s += "{0}={1}, ".format(f'`{key}`', f'"{values}"')

                Id = item['Id']
                fields = s[:-2].replace(f'Id="{Id}",', "").replace("None", " ")

                update_query = f"update {pdp_table} set {fields} where Id ='{Id}'"
                print(update_query)
                self.cursor.execute(update_query)
                self.con.commit()
                print(f"  ********** Update Query Fired for {Id} *************  ")


            except Exception as E:
                print("Update Query  Error", E)

