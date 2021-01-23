def crawl():
    from chromedriver_py import binary_path
    from selenium import webdriver
    import uuid
    import os
    print("VERSION 2")
    tmp_folder = f'/tmp/{uuid.uuid4()}'

    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    if not os.path.exists(tmp_folder + '/user-data'):
        os.makedirs(tmp_folder + '/user-data')

    if not os.path.exists(tmp_folder + '/data-path'):
        os.makedirs(tmp_folder + '/data-path')

    if not os.path.exists(tmp_folder + '/cache-dir'):
        os.makedirs(tmp_folder + '/cache-dir')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir={}'.format(tmp_folder + '/user-data'))
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path={}'.format(tmp_folder + '/data-path'))
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir={}'.format(tmp_folder))
    chrome_options.add_argument('--disk-cache-dir={}'.format(tmp_folder + '/cache-dir'))
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = "/app//bin/headless-chromium"

    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=binary_path)

    driver.get('http://example.com')
    elem_value = driver.find_element_by_xpath('(//div//h1)[1]')
    result = elem_value.get_attribute('innerHTML')

    print(result)

    return result


if __name__ == "__main__":
    print('running')
    crawl()
