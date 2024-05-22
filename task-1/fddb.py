import requests
from lxml import html


URL = "https://fddb.info/db/de/hersteller/"
response = requests.get(URL)
print(response)
tree = html.fromstring(response.content)

for main in tree.xpath("//div[@class='standardcontent']"):
    category = main.xpath(".//h2/text()")
    subcategory = main.xpath(".//div/a/text()")
    link = [('https://fddb.info/'+link) for link in main.xpath(".//@href")]

    for i in link:
        print(i)







