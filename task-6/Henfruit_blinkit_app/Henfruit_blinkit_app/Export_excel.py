import json
import os

import dropbox
import pandas as pd
from Henfruit_blinkit_app.pipelines import *
from colorama import init, Fore, Back, Style
from Henfruit_blinkit_app.qatoolapi import validation_mail
init(convert=True)



class Export_Csv:

    # make csv csv method
    def export_excel_keyword(self):
        try:
            print("Going to sql connetion....")
            conn = pymysql.connect(host=db_host, user=db_user, password=db_passwd, database=db_name, use_unicode=True,
                                   charset="utf8")
            cursor = conn.cursor()

            try:
                csv_file_date = datetime.now().strftime("%Y_%m_%d")
                y = datetime.now().strftime("%Y")
                M_Y = datetime.now().strftime("%b.%y")
                d = datetime.now().strftime("%d")

                Period = datetime.today().strftime("%p")
                Hour = datetime.today().strftime("%I")
                Timeslot = f'{Hour}:00:00 {Period}'
                print(Timeslot)
                slot_list = ['07:00:00 AM', '09:00:00 AM', '11:00:00 AM', '02:00:00 PM', '05:00:00 PM']
                table_slot = f'{Hour}_00_00_{Period}'
                
                print("Going to sql connetion....")

                if Timeslot == '07:00:00 AM': #  WHERE `Availability` IS NOT NULL
                    batch = 1
                    select_sql_query = f"""SELECT  `Date`, `Region`, `City`, `Pin Code`, `Group`, `Product ID`,  `Merchant Id`,  `Item Name`, `Item Link`, `07:00:00 AM`, `total hours`, `Live hours`, `offline hours`, `Availability` from {pdp_table}"""
                    data_frame = pd.read_sql(select_sql_query, conn)

                elif Timeslot == '09:00:00 AM':
                    batch = 2
                    select_sql_query = f"""SELECT  `Date`, `Region`, `City`, `Pin Code`, `Group`, `Product ID`,  `Merchant Id`,  `Item Name`, `Item Link`, `07:00:00 AM`, `09:00:00 AM`, `total hours`, `Live hours`, `offline hours`, `Availability` from {pdp_table}"""
                    data_frame = pd.read_sql(select_sql_query, conn)
                elif Timeslot == '11:00:00 AM':
                    batch = 3
                    select_sql_query = f"""SELECT  `Date`, `Region`, `City`, `Pin Code`, `Group`, `Product ID`,  `Merchant Id`,  `Item Name`, `Item Link`, `Selling Price at 11:00 AM`, `MRP at 11:00 AM`, `Discount running`, `Disc %`,`07:00:00 AM`, `09:00:00 AM`, `11:00:00 AM`, `total hours`, `Live hours`, `offline hours`, `Availability` from {pdp_table}"""
                    data_frame = pd.read_sql(select_sql_query, conn)

                elif Timeslot == '02:00:00 PM':
                    batch = 4
                    select_sql_query = f"""SELECT  `Date`, `Region`, `City`, `Pin Code`, `Group`, `Product ID`,  `Merchant Id`,  `Item Name`, `Item Link`, `Selling Price at 11:00 AM`, `MRP at 11:00 AM`, `Discount running`, `Disc %`, `07:00:00 AM`, `09:00:00 AM`, `11:00:00 AM`, `02:00:00 PM`, `total hours`, `Live hours`, `offline hours`, `Availability` from {pdp_table}"""
                    data_frame = pd.read_sql(select_sql_query, conn)

                else:
                    batch = 5
                    select_sql_query = f"""SELECT  `Date`, `Region`, `City`, `Pin Code`, `Group`, `Product ID`,  `Merchant Id`,  `Item Name`, `Item Link`, `Selling Price at 11:00 AM`, `MRP at 11:00 AM`, `Discount running`, `Disc %`, `07:00:00 AM`, `09:00:00 AM`, `11:00:00 AM`, `02:00:00 PM`, `05:00:00 PM`, `total hours`, `Live hours`, `offline hours`, `Availability` from {pdp_table}"""
                    data_frame = pd.read_sql(select_sql_query, conn)

                # else:
                #     batch = 6
                #     select_sql_query = f"""SELECT  `Date`, `Region`, `City`, `Pin Code`, `Group`, `Product ID`, `Merchant Id`,  `Item Name`, `Item Link`, `Selling Price at 11:00 AM`, `MRP at 11:00 AM`, `Discount running`, `Disc %`, `07:00:00 AM`, `09:00:00 AM`, `11:00:00 AM`, `02:00:00 PM`, `05:00:00 PM`, `07:00:00 PM`, `total hours`, `Live hours`, `offline hours`, `Availability` from {pdp_table}"""
                #     data_frame = pd.read_sql(select_sql_query, conn)


                Excel_filename =  f"Henfruit_Blinkit_{csv_file_date}___{table_slot}.xlsx"

                Excel_fullpath = CSV_Path + "\\" + Excel_filename

                if not os.path.exists(Excel_fullpath):
                    writer = pd.ExcelWriter(Excel_fullpath, engine='xlsxwriter', engine_kwargs={'options': {'strings_to_urls': False}})
                    data_frame.to_excel(writer, index=False)
                    writer.close()

                print(Excel_fullpath)
               
                try:
            
                    TOKEN = f'QCPF1vlY6OYAAAAAAAAAAV6Ccw5Dar7DZ-rQ2n2q5YQBV9SJwS3AuwGQoIT5-wkE'

                    dbx = dropbox.Dropbox(TOKEN)
                    with open(Excel_fullpath, 'rb') as f:
                        db_path = f"/Henfruit/{y}/{M_Y}/{d}/{Excel_filename}"
                        print(db_path)
                        try:
                            dbx.files_upload(f.read(), db_path, mode=dropbox.files.WriteMode.overwrite)
                            Skype_bot(f"File Uploaded on Dropbox: {Excel_filename}")
                            
                            banner_sql2 = f'''update `slot_status` set Status = "Done" where Slots = "File_upload"'''
                            # print(banner_sql)
                            cursor.execute(banner_sql2)
                            conn.commit()
                            
                        except Exception as e:
                            if "('conflict', WriteConflictError" in str(e):
                                pass
                            else:
                                print("Error in Drop Box Uploading...", e)
                                return None

                            # share_url = "None1"
                        print('File Uploaded on Dropbox', Excel_fullpath)
                    
                    # target_function = validation_mail(Excel_fullpath, batch)
                    # print(target_function)
                    
                    if Timeslot == '05:00:00 PM':

                        # Specify the folder path you want to list
                        folder_path = f"/Henfruit/{y}/{M_Y}/{d}"

                        # List files in the specified folder
                        try:

                            swiggy = 0
                            blinkit = 0
                            zepto = 0
                            bigbasket = 0

                            files = dbx.files_list_folder(folder_path).entries
                            print(len(files))
                            for file in files:
                                print(file.name)
                                if 'Swiggy' in file.name:
                                    swiggy += 1

                                elif 'Blinkit' in file.name:
                                    blinkit += 1

                                elif 'Zepto' in file.name:
                                    zepto += 1

                                elif 'Bigbasket' in file.name:
                                    bigbasket += 1

                            if len(files) == 12:
                                msg = "All file uploaded. Please send mail."

                                # print(msg)
                                # Skype_bot(msg)
                                os.chdir(os.getcwd())
                                os.startfile('Hansfruit_Mail.bat')
                            else:
                                add_msg = ""
                                if blinkit != 6:
                                    missing_file = 6 - blinkit
                                    if not add_msg:
                                        add_msg += f"\nMissing File Details:\n{missing_file} Missing Blinkit's File."
                                    else:
                                        add_msg += f"\n{missing_file} Missing Blinkit's File."
                                elif swiggy != 2:
                                    missing_file = 2 - swiggy
                                    if not add_msg:
                                        add_msg += f"\nMissing File Details:\n{missing_file} Missing Swiggy's File."
                                    else:
                                        add_msg += f"\n{missing_file} Missing Swiggy's File."

                                elif bigbasket != 2:
                                    missing_file = 2 - bigbasket
                                    if not add_msg:
                                        add_msg += f"\nMissing File Details:\n{missing_file} Missing BigBasket's File."
                                    else:
                                        add_msg += f"\n{missing_file} Missing BigBasket's File."

                                elif zepto != 2:
                                    missing_file = 2 - zepto
                                    if not add_msg:
                                        add_msg += f"\nMissing File Details:\n{missing_file} Missing Zepto's File."
                                    else:
                                        add_msg += f"\n{missing_file} Missing Zepto's File."

                                msg = f"{12-len(files)} files haven't been uploaded yet. Please check and upload them as soon as possible and after that send mail. \nThank you!"
                                # print(msg)
                                # # Skype_bot(add_msg)
                                # Skype_bot(msg)
                                os.chdir(os.getcwd())
                                os.startfile('Hansfruit_Mail.bat')
                                
                        except Exception as e:
                            print(f"Error listing folder: {e}")

                except Exception as e:
                    print(e)
                    pass

                print(Fore.GREEN, "Successfully Excel File Wrote... Done............!", Excel_filename, Fore.RESET)

            except Exception as e:
                print(e)

        except Exception as e:
            print(e)


# if __name__ == '__main__':
#     c = Export_Csv()
#     c.export_excel_keyword()
