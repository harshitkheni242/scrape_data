from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

username = 'AppleApple'
password = '123apple'

driver.get("https://quotes.toscrape.com/")

element = driver.find_element(By.XPATH, "//a[contains(text(), 'Login')]")
element.click()
time.sleep(2)
username1 =  driver.find_element(By.XPATH, "//input[@id='username']").send_keys(username)
password1 =  driver.find_element(By.XPATH, "//input[@id='password']").send_keys(username)
time.sleep(2)
element = driver.find_element(By.XPATH, "//input[@value='Login']")
element.click()
time.sleep(2)
driver.quit()

