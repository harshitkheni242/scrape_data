import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
options = Options()
options.add_argument("--headless")


driver = webdriver.Chrome(options=options)


driver.get("https://quotes.toscrape.com/")


def get_scroll_dimension(axis):
    return driver.execute_script(f"return document.body.parentNode.scroll{axis}")


def capture_full_page_screenshot(file_name):
    width = get_scroll_dimension("Width")
    height = get_scroll_dimension("Height")
    driver.set_window_size(width, height)
    driver.save_screenshot(file_name)

page_counter = 1

while True:
    capture_full_page_screenshot(f"screenshots/selenium-page-{page_counter}.png")

    next_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
    if next_button:
        next_button.click()
        page_counter += 1
        time.sleep(2)
    else:
        break


driver.quit()
