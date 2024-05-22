import requests
from lxml import html

url = 'http://quotes.toscrape.com'

response = requests.get(url)

tree = html.fromstring(response.content)

for quote in tree.xpath('//div[@class="quote"]'):
    quotes = quote.xpath('.//span[@class="text"]/text()')[0].strip()
    authors = quote.xpath('.//small[@class="author"]/text()')[0].strip()
    tags = ",".join(quote.xpath('.//a[@class="tag"]/text()'))
    link = quote.xpath('.//@href')[0]

    print(link)
