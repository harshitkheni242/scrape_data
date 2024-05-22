from datetime import datetime
import os.path

current_date = datetime.now().strftime('%d/%m/%Y')
new_td = datetime.now().strftime('%Y_%m_%d')
new_td1 = datetime.now().strftime('%d-%m-%Y')
year = datetime.now().strftime('%Y')

db_host = '192.168.1.129'

db_user = 'root'
db_passwd = 'xbyte'
db_name = 'Henfruit_Blinkit'

from datetime import datetime

# Get today's date
today_date = datetime.now().date()


# Check if today's date is greater than the given date
Input_table = f'input_data'

Period = datetime.today().strftime("%p")
Hour = datetime.today().strftime("%I")

# Timeslot1 = f'{Hour}_00_00_{Period}'
pdp_table = f'product_data_{new_td}'

HTMLs = f"/mnt/data/Weekly Scheduler/0. Henfruit/Blinkit/HTMLs/{new_td}"
HTML = HTMLs
CSV_Path = f'/mnt/data/Weekly Scheduler/0. Henfruit/Blinkit/CSV/{new_td}'

try:
    if not os.path.exists(HTML):
        os.makedirs(HTML)

    if not os.path.exists(CSV_Path):
        os.makedirs(CSV_Path)

except Exception as e:
    print('exception in makedir config file error: ', e)


def Skype_bot(msg):
    from skpy import Skype, SkypeChats

    # sk = Skype("botxbyte.bau@gmail.com", "Krushil@#12345")
    sk = Skype("botxbyte.bau@gmail.com", "krushil@123")
    # skc = SkypeChats(sk)
    # print(skc.recent())

    ch = sk.chats["19:9ba60a83d8ac43e2b4670a97e9a8851e@thread.skype"]  # [XBYKPR:2217] Henfruit
    ch.sendMsg(msg)
    
# Skype_bot("msg")
#

