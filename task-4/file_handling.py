html_path = "/home/ravin.parmar/ravin_traning/task_3/html1"

try:
    if not os.path.exists(html_path):
        os.makedirs(html_path)
except Exception as e:
    print(e)

full_html_path = os.path.join(html_path, f"1.html")

if os.path.exists(full_html_path):
     with open(full_html_path, 'r', encoding='utf8') as f:
         html_response = f.read()
else:
    response = requests.get('https://www.simplotfoods.com/foodservice-categories', cookies=cookies, headers=headers)
    print(response.status_code)
    html_response = response.text

    if response.status_code == 200:
        with open(full_html_path, 'w', encoding='utf8') as f:
            f.write(html_response)
    else:
        print("Getting Response issue... ")
        exit(0)