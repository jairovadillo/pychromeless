import os
import hashlib
import urllib
import boto
import boto.s3
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from webdriver_wrapper import WebDriverWrapper

def md5_str(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return str(m.hexdigest())

def lambda_handler(event, context):
    driver = WebDriverWrapper()

    # Fail if URL not defined
    scannee = urllib.parse.unquote(event['url'])

    bad_words = ['file://']
    if any(word in scannee for word in bad_words):
        raise Exception('suspicious string found in URL')


    screenshot_filename = md5_str(scannee) + '.png'
    screenshot_path = '/tmp/' + screenshot_filename

    print('Fetching: {}'.format(scannee))
    driver.get_url(scannee)

    print('Saving screenshot to: {}'.format(screenshot_filename))
    driver.screenshot(screenshot_path)

    driver.close()

    S3_KEY_ID = os.environ.get('S3_KEY_ID')
    S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY')

    conn = S3Connection(S3_KEY_ID, S3_SECRET_KEY)
    bucket = conn.get_bucket('glimpsefiles')
    key = Key(bucket, 'screenshots/' + screenshot_filename)
    key.set_contents_from_filename(screenshot_path)

    return {'screenshot': 'https://glimpsefiles.s3.amazonaws.com/screenshots/' + screenshot_filename }
