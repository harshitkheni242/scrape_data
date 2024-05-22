import time

from selinum import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# options = Options()
# options.add_argument('__headless')

username = 'appleapple'
password = '123apple'

driver = webdriver.Chrome()

driver.get("https://quotes.toscrape.com/")

login = driver.find_element(By.XPATH, "//a[contains(text(),'Login')]")

time.sleep(2)

login.click()

time.sleep(2)

username1 = driver.find_element(By.XPATH, "//input[@id='username']").send_keys(username)
password1 = driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)

time.sleep(2)

submit = driver.find_element(By.XPATH, "//input[@value='Login']").click()

time.sleep(2)
driver.quit()