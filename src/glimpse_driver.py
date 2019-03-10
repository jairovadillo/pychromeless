import os
import uuid
from selenium import webdriver

class Options:
    def __init__(self):
        #self.resolution = "1280x1696"
        self.resolution = "1920x1080"

class Firefox(Options):
    def __init__(self):
        Options.__init__(self)
        self.options = webdriver.FirefoxOptions()
        self.options.headless = True
        self.options.accept_insecure_certs = True
        self.options.add_argument("--width={}".format(self.resolution[:self.resolution.index("x")]))
        self.options.add_argument("--height={}".format(self.resolution[:self.resolution.index("x") + 1]))

        self.driver = webdriver.Firefox(firefox_options=self.options)


class Chromium(Options):
    def __init__(self):
        Options.__init__(self)

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
            'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        self.options.binary_location = os.getcwd() + "/bin/headless-chromium"

        self.driver = webdriver.Chrome(chrome_options=self.options)


class GlimpseDriver:
    def __init__(self, browser=Chromium()):
        self.driver = browser.driver

    def screenshot(self, path):
        return self.driver.save_screenshot(path)

    def get_path(self):
        pass

    def get_location(self):
        return self.driver.execute_script('return window.location')

    def effective_url(self):
        return self.driver.execute_script('return window.location')['href']
