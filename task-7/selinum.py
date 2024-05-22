from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime

# Get the current timestamp for the image name
today = datetime.now()
image_name = today.strftime("%Y-%m-%d %H:%M:%S")

# Set the path where the screenshot will be saved
# path = os.path.dirname(os.path.abspath('screen_shot'))5
path = os.getcwd()


# Configure Chrome WebDriver options
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument("--headless")  # Use headless mode for running in the background
options.add_argument("--disable-gpu")

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Navigate to the URL you want to capture
driver.get("https://www.thefragranceshop.co.uk/bestsellers/l")

# Wait for the page to load (you can adjust the sleep time as needed)
time.sleep(1)

# Use JavaScript to get the full width and height of the webpage
width = driver.execute_script("return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

# Set the window size to match the entire webpage
driver.set_window_size(width, height)

# Find the full page element (usually 'body') and capture the screenshot
full_page = driver.find_element(By.TAG_NAME, "body")
full_page.screenshot(f"{image_name}.png")

# Close the browser window
driver.quit()
