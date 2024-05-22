import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

driver.get("https://example.com")  # Replace "https://example.com" with the URL you want to capture

width = driver.execute_script("return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

driver.set_window_size(width, height)

full_page = driver.find_element(By.TAG_NAME, "body")
driver.save_screenshot("screenshot/quotes_to_scrape.png")

driver.quit()
