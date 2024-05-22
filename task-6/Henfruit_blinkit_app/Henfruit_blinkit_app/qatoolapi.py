# todo : file validation mail
import os
import requests

# TODO - Request URL
url = "http://192.168.0.39:5055/validate"

# TODO Main mail function
def validation_mail(file_path, batch):
    file = file_path.split("\\")[-1]
    project_id = 3066
    project_user_id = batch

    # TODO - Parameters
    params = {
        "ProjectID": project_id,  # TODO - As per your Project ID
        "UserStoryID": project_user_id,  # TODO - As per your project user id
        "toArray":"['kamaram.choudhary@xbyte.io']",
        "CcArray": "['savanp.xbyte@gmail.com', 'twinkal.prajapati@xbyte.io', 'krushil.gajjar@xbyte.io', 'niyati.dave@xbyte.io', 'suraj.mehta@xbyte.io']",
        # "CcArray": "['ankit.mochi.xbyte@gmail.com','vikram.chauhan.xbyte@gmail.com','abhishek.soni@xbyte.io']",
        # "BccArray": "[]"
        # TODO - Required CC list inside String
    }

    # TODO - Input Files
    data_file_path = fr"{file_path}"
    sample_file_path = data_file_path
    rules_json_path = rf"E:/Kamaram_Choudhary/working/Hen's fruit/Henfruit_blinkit_app/Henfruit_blinkit_app/{project_id}_{project_user_id}_rules.json"
    data_file = ('data_file', (file, open(data_file_path, "rb")))
    sample_file = ('sample_file', (file, open(sample_file_path, "rb")))
    rules_json = ('rules_json', (f"{project_id}_{project_user_id}_rules.json", open(rules_json_path, "rb")))

    # TODO Sending Response
    files = [data_file, sample_file, rules_json]
    response = requests.request(method="GET", url=url, params=params, files=files)
    print(response.status_code)
    # TODO Getting Response
    return response.text

# file_path = fr"D:\Weekly Scheduler\0. Henfruit\Blinkit\CSV\2024_01_30\Henfruit_Blinkit_2024_01_30___11_00_00_AM.xlsx"
#
# target_function = validation_mail(file_path, 3)
# print(target_function)