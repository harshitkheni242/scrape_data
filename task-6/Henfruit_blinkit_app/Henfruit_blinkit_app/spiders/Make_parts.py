from Henfruit_blinkit_app.pipelines import *
import os
import numpy as np

def parts(Spider_type):
    con = pymysql.connect(host=db_host, user=db_user, password=db_passwd)
    db_cursor = con.cursor()
    create_db = f"create database if not exists {db_name} CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci"
    db_cursor.execute(create_db)
    con = pymysql.connect(host=db_host, user=db_user, password=db_passwd, database=db_name, autocommit=True)
    cursor = con.cursor()

    if Spider_type == 'pdp':
        # sql_query = f"SELECT Id FROM {pdp_table} WHERE Status = 'Pending'"
        sql_query = f"SELECT Id FROM {pdp_table} WHERE Status = 'Pending'"
        Spider_Name = f'blinkit'
        Bat_FileName = "blinkit_pending.bat"
        set_timeout1 = 10
    else:
        return None

    print(sql_query)
    cursor.execute(sql_query)
    core_list = [column for column in cursor.fetchall()]
    C_ids = []

    for itm in core_list:
        id = itm[0]
        C_ids.append(id)

    Store_Name = f'scrapy'
    C_ids.sort()

    l = len(C_ids)
    print(l)

    if l >= 30:
        n = 30

    else:
        n = l

    d = round(l / n)
    x_ids = np.array_split(C_ids, n)

    pending_bat = []
    set_timeout = 0
    loop_index = 0
    for parts in x_ids:

        loop_index += 1
        set_timeout += 1

        if set_timeout == set_timeout1:
            pending_bat.append("timeout 10")
            set_timeout = 0
        # if loop_index == len(x_ids):
        #     commands = f'start {Store_Name} crawl {Spider_Name} -a start={parts[0]} -a end={parts[-1]} -a upload=yes'
        #     pending_bat.append(commands)
        # else:
        commands = f'start {Store_Name} crawl {Spider_Name} -a start={parts[0]} -a end={parts[-1]}'
        pending_bat.append(commands)

    pending_parts = "taskkill /f /im scrapy.exe\n" + "\n".join(pending_bat)
    # print(pending_parts)

    path = os.getcwd() +"/"+ Bat_FileName

    path = path.replace("\\", "/")
    with open(path, 'w') as f:
        f.write(pending_parts)

    print("New Parts Created.........", Bat_FileName)

    os.chdir(os.getcwd())
    os.startfile(Bat_FileName)

if __name__ == '__main__':
    # Spider_type: str = 'pl'
    Spider_type: str = 'pdp'
    parts(Spider_type)
