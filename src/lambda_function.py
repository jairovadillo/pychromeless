import time

from webdriver_wrapper import WebDriverWrapper


def lambda_handler(*args, **kwargs):
    driver = WebDriverWrapper()

    driver.get_url('https://www.google.es/')

    driver.set_input_value('//input[@name="q"]', '21 buttons')

    driver.click('//center//img[@alt="Google"]')
    time.sleep(0.5)

    driver.click('//input[@name="btnK"]')
    time.sleep(0.5)

    first_google_result_title = driver.get_inner_html('(//div[@class="rc"]//a)[1]')

    print("--------------------------")
    print(first_google_result_title)
    print("--------------------------")

    driver.close()
