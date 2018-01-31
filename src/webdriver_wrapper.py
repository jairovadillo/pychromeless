import os
import shutil
import uuid

from selenium import webdriver


class WebDriverWrapper:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        self._tmp_folder = '/tmp/{}'.format(uuid.uuid4())

        if not os.path.exists(self._tmp_folder):
            os.makedirs(self._tmp_folder)

        if not os.path.exists(self._tmp_folder + '/user-data'):
            os.makedirs(self._tmp_folder + '/user-data')

        if not os.path.exists(self._tmp_folder + '/data-path'):
            os.makedirs(self._tmp_folder + '/data-path')

        if not os.path.exists(self._tmp_folder + '/cache-dir'):
            os.makedirs(self._tmp_folder + '/cache-dir')

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x1696')
        chrome_options.add_argument('--user-data-dir={}'.format(self._tmp_folder + '/user-data'))
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=99')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--data-path={}'.format(self._tmp_folder + '/data-path'))
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--homedir={}'.format(self._tmp_folder))
        chrome_options.add_argument('--disk-cache-dir={}'.format(self._tmp_folder + '/cache-dir'))
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

        chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

        self._driver = webdriver.Chrome(chrome_options=chrome_options)

    def get_url(self, url):
        self._driver.get(url)

    def set_input_value(self, xpath, value):
        elem_send = self._driver.find_element_by_xpath(xpath)
        elem_send.send_keys(value)

    def click(self, xpath):
        elem_click = self._driver.find_element_by_xpath(xpath)
        elem_click.click()

    def get_inner_html(self, xpath):
        elem_value = self._driver.find_element_by_xpath(xpath)
        return elem_value.get_attribute('innerHTML')

    def close(self):
        # Close webdriver connection
        self._driver.quit()

        # Remove specific tmp dir of this "run"
        shutil.rmtree(self._tmp_folder)

        # Remove possible core dumps
        folder = '/tmp'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if 'core.headless-chromi' in file_path and os.path.exists(file_path) and os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)