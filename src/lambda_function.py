import time

from webdriver_wrapper import WebDriverWrapper
from selenium.webdriver.common.keys import Keys


def lambda_handler(*args, **kwargs):
    driver = WebDriverWrapper()

    driver.get_url('https://www.google.es/')

    driver.set_input_value('//input[@name="q"]', '21 buttons')

    button = driver.find("//input[@name='btnK']")
    button.send_keys(Keys.TAB)
    driver.click('//input[@name="btnK"]')

    first_google_result_title = driver.get_inner_html('(//div[@class="rc"]//a)[1]')

    print("--------------------------")
    print(first_google_result_title)
    print("--------------------------")

    driver.close()
