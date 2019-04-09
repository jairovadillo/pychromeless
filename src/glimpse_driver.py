import os
import uuid
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class BrowserSettings:
    def __init__(self):
        self.resolution = "1280x1696"
        #self.resolution = "1920x1080"

class Firefox(BrowserSettings):
    def __init__(self):
        BrowserSettings.__init__(self)

        os.system("/var/task/bin/firefox/firefox --headless")

        binary = FirefoxBinary("/var/task/bin/firefox/firefox")
        self.options = Options()

        self.options.set_headless(headless=True)
        
        self.options.accept_insecure_certs = True
        self.width = self.resolution[:self.resolution.index("x")]
        self.height = self.resolution[:self.resolution.index("x") + 1]
        
        self.driver = webdriver.Firefox(firefox_binary=binary, firefox_options=self.options)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(self.width, self.height)



class Chromium(BrowserSettings):
    def __init__(self, ua):
        BrowserSettings.__init__(self)

        self._tmp_folder = '/tmp/{}'.format(uuid.uuid4())

        if not os.path.exists(self._tmp_folder):
            os.makedirs(self._tmp_folder)

        if not os.path.exists(self._tmp_folder + '/user-data'):
            os.makedirs(self._tmp_folder + '/user-data')

        if not os.path.exists(self._tmp_folder + '/data-path'):
            os.makedirs(self._tmp_folder + '/data-path')

        if not os.path.exists(self._tmp_folder + '/cache-dir'):
            os.makedirs(self._tmp_folder + '/cache-dir')

        self.options = webdriver.ChromeOptions()

        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=' + self.resolution)
        self.options.add_argument('--user-data-dir={}'.format(self._tmp_folder + '/user-data'))
        self.options.add_argument('--hide-scrollbars')
        self.options.add_argument('--enable-logging')
        self.options.add_argument('--log-level=0')
        self.options.add_argument('--v=99')
        self.options.add_argument('--single-process')
        self.options.add_argument('--data-path={}'.format(self._tmp_folder + '/data-path'))
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument('--homedir={}'.format(self._tmp_folder))
        self.options.add_argument('--disk-cache-dir={}'.format(self._tmp_folder + '/cache-dir'))
        self.options.add_argument(
            f'user-agent={ua}')
        self.options.binary_location = os.getcwd() + "/bin/headless-chromium"

        self.driver = webdriver.Chrome(chrome_options=self.options)


class GlimpseDriver:
    def __init__(self, browser=Chromium(ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")):
        self.driver = browser.driver

    def screenshot(self, path):
        return self.driver.save_screenshot(path)

    def get_path(self):
        pass

    def get_location(self):
        return self.driver.execute_script('return window.location')

    def get_network_history(self):
        net_list = self.driver.execute_script('return window.performance.getEntries()')
        return [site['name'] for site in net_list ]
