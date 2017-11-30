import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def lambda_handler(*args, **kwargs):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

    # path_chromedriver = os.getcwd() + 'bin/chromedriver'
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get('https://www.google.es/')
    elem_send = driver.find_element_by_xpath('//input[@id="lst-ib"]')
    elem_send.send_keys('asdf')
    elem_click = driver.find_element_by_xpath('//center//img[@alt="Google"]')
    elem_click.click()
    time.sleep(0.5)
    elem_click = driver.find_element_by_xpath('//input[@name="btnK"]')
    elem_click.click()
    time.sleep(0.5)
    first_a = '(//div[@class="_NId"]//a)[1]'
    elem_value = driver.find_element_by_xpath(first_a)
    elem_value = elem_value.get_attribute('innerHTML')

    print(elem_value)
    driver.quit()


if __name__ == "__main__":
    lambda_handler()
