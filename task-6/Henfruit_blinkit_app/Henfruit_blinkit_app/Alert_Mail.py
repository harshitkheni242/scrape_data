import time
from dropbox.exceptions import AuthError
import dropbox
from easygui import *
import time
import pymysql
import requests
import json
from datetime import datetime, timedelta
import os.path
from datetime import date
from dateutil.relativedelta import relativedelta, TH


def Skype_bot(msg):
	# Author: Arab Bask
	from skpy import Skype, SkypeChats
	sk = Skype("botxbyte.bau@gmail.com", "krushil@123")

	#   skype_obj = mailto:skype("botxbyte.bau@gmail.com", "Krushil@12345")
	# skc = SkypeChats(sk)
	# print(skc.recent())
	
	ch = sk.chats["19:9ba60a83d8ac43e2b4670a97e9a8851e@thread.skype"]  # [XBYKPR:2217] Henfruit
	ch.sendMsg(msg)


if __name__ == '__main__':
	today = datetime.today()
	today_date = datetime.now().strftime('%Y_%m_%d')
	yesterday1 = today - timedelta(days=1)
	yesterday = yesterday1.strftime('%Y_%m_%d')
	y_y = yesterday1.strftime('%Y')
	y_d = yesterday1.strftime('%d')
	m_d = yesterday1.strftime('%b.%y')
	
	# place with your access token
	ACCESS_TOKEN = 'QCPF1vlY6OYAAAAAAAAAAV6Ccw5Dar7DZ-rQ2n2q5YQBV9SJwS3AuwGQoIT5-wkE'
	
	# Initialize Dropbox client
	dbx = dropbox.Dropbox(ACCESS_TOKEN)
	
	host_list = ['192.168.1.94', '192.168.1.39', '192.168.1.129']
	
	db_list = ["henfruit_zepto", "swiggy_instamart", "henfruit_blinkit"]  # TODO - Comparison
	label_list = ["henfruit_zepto", "henfruit_swiggy", "henfruit_blinkit"]  # TODO - Comparison
	
	today_table_list = [f'productdata_{today_date}', f'productdata_{today_date}', f'product_data_{today_date}', ]
	yesterday_table_list = [f'productdata_{yesterday}', f'productdata_{yesterday}', f'product_data_{yesterday}', ]
	
	today_file_size_list = []
	yester_file_size_list = []
	
	today_filelist = [
		f'Henfruit_Zepto_{today_date}_05_00_00_PM.xlsx',
		f'Henfruit_Swiggy_{today_date}_05:00:00.xlsx',
		f'Henfruit_Blinkit_{today_date}___05_00_00_PM.xlsx',
	]
	yester_filelist = [
		f'Henfruit_Zepto_{yesterday}_05_00_00_PM.xlsx',
		f'Henfruit_Swiggy_{yesterday}_05:00:00.xlsx',
		f'Henfruit_Blinkit_{yesterday}___05_00_00_PM.xlsx',
	]
	
	y = datetime.now().strftime("%Y")
	M_Y = datetime.now().strftime("%b.%y")
	d = datetime.now().strftime("%d")
	# Specify the folder path you want to list
	tfolder_path = f"/Henfruit/{y}/{M_Y}/{d}"
	yfolder_path = f"/Henfruit/{y_y}/{m_d}/{y_d}"
	
	try:
		for ii in range(len(today_filelist)):
			t_filename = today_filelist[ii]
			y_filename = yester_filelist[ii]
			
			try:
				# Get file metadata
				tmetadata = dbx.files_get_metadata(f"{tfolder_path}/{t_filename}")
				tfile_size = tmetadata.size
				tfile_size = round(tfile_size / 1024, 2)
				today_file_size_list.append(f"{tfile_size} kb")
				print(f"File size of '{tfolder_path}' is {tfile_size} bytes.")
			except:
				print(f"File Not Found...", f"{tfolder_path}/{t_filename}")
				time.sleep(10)
				exit(1)
			try:
				ymetadata = dbx.files_get_metadata(f"{yfolder_path}/{y_filename}")
				yfile_size = ymetadata.size
				yfile_size = round(yfile_size / 1024, 2)
				yester_file_size_list.append(f"{yfile_size} kb")
				print(f"File size of '{yfolder_path}' is {yfile_size} bytes.")
			except:
				print(f"File Not Found...", f"{yfolder_path}/{y_filename}")
				time.sleep(10)
				exit(1)
				
	
	except dropbox.exceptions.HttpError as err:
		print(f"Dropbox API error: {err}")
	except AuthError as auth_err:
		print(f"Authorization error: {auth_err}")
	except dropbox.exceptions.ApiError as api_err:
		print(f"API error: {api_err}", )
	
	username_list = ['root', 'root', 'root', 'root']
	passwrd_list = ['xbyte', 'xbyte', 'xbyte', 'xbyte']
	
	# message = "Choose Your Mail Type"
	# title = "Mail Type"
	# choices = ["Client", "Internal","Cancel"]
	# choise = buttonbox(message, title, choices)
	
	# if choise == 'Client':
	print("Going to Send mail to client....")
	for_to = open(f'{os.getcwd()}/to_list.txt', 'r').read().splitlines()
	for_cc = open(f'{os.getcwd()}/cc_list.txt', 'r').read().splitlines()
	for_bcc = open(f'{os.getcwd()}/bcc_list.txt', 'r').read().splitlines()
	
	# elif choise == 'Internal':
	# print("Going to Send mail to Internal....")
	# for_to = open(f'{os.getcwd()}/internal_to_list.txt', 'r').read().splitlines()
	# for_cc = open(f'{os.getcwd()}/internal_cc_list.txt', 'r').read().splitlines()
	# for_bcc = open(f'{os.getcwd()}/internal_bcc_list.txt', 'r').read().splitlines()
	
	Dropbox_url = "https://www.dropbox.com/sh/ftaeq1yr9wvlas5/AADL18SusXYkYinhoriUMbsHa?dl=0"
	"----------------------------------------------------------------"
	
	# url = 'http://192.168.0.39:5020/composite_graph/'
	url = 'http://103.156.143.42:5020/composite_graph/'

	payload = {"project_name": 'Henfruit',
	           "type": 'sql',
	           "host": f"{host_list}",
	           "username": f"{username_list}",
	           "password": f"{passwrd_list}",
	           "database_name": f"{db_list}",
	           "today_table": f"{today_table_list}",
	           "yesterday_table": f"{yesterday_table_list}",
	           "label_name": f"{label_list}",
	           "days_to_compare": "",
	           "dynamic_table": 'no',
	           "table_prefix": 'data_Morning',
	           "table_date_format": "%Y_%m_%d",
	           "header_flag": "yes",
	           "header_arr": "['Prodect ID','Item Name','total hours', 'Live hours', 'offline hours', 'Availability']",
	           "file_name": '',
	           "Client_name": 'Tarun',
	           "Alert_code": " 2217",
	           "graph_type": 'bar',
	           "graph_flag": 'yes',
	           "to_arr": f"{for_to}",
	           "cc_arr": f"{for_cc}",
	           "bcc_arr": f"{for_bcc}",
	           "extra_params_arr": f"['Dropbox Link: {Dropbox_url}']",
	           "file_base64": '',
	           "client_io_flag": "YES",
	           "today_file_size": f"{today_file_size_list}",  # TODO - File size
	           "yesterday_file_size": f"{yester_file_size_list}"  # TODO - File size
	           }
	
	# TODO - Getting response from payload
	data = json.dumps(payload)
	response = requests.post(url, data=data)

	if 'Mail Sent !!!' in response.text:
		JSON = json.loads(response.text)
		print("Mail Sent!!!")
		msg = JSON['message']
		Skype_bot(msg)

	print(response.text)
	time.sleep(30)
