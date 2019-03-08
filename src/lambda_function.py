import os
import hashlib
import urllib
import boto3
import botocore
from webdriver_wrapper import WebDriverWrapper

def md5_str(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return str(m.hexdigest())

def lambda_handler(event, context):

    GLIMPSE_BUCKET_NAME = os.getenv('GLIMPSE_BUCKET_NAME')

    # Fail if URL not defined
    scannee = urllib.parse.unquote(event['url'])

    # Filter for potentially malicious or invalid URLs
    bad_words = ['file://']
    if any(word in scannee for word in bad_words):
        raise Exception('suspicious string found in URL')

    # Calculate MD5 hash of URL 
    screenshot_filename = md5_str(scannee) + '.png'
    screenshot_path = '/tmp/' + screenshot_filename
    screenshot_key_path = 'screenshots/' + screenshot_filename

    s3_resource = boto3.resource('s3')
    screenshot_key = s3_resource.Object(bucket_name=GLIMPSE_BUCKET_NAME, key=screenshot_key_path)
    
    # Check if a screenshot already exists
    try:
        s3_resource.Object(GLIMPSE_BUCKET_NAME, 'screenshots/' + screenshot_filename).download_file(screenshot_path)
        print(' ### Screenshot already exists for this URL. ###')
        return {'screenshot': 'https://glimpsefiles.s3.amazonaws.com/screenshots/' + screenshot_filename }
    except botocore.exceptions.ClientError as e:
        print(e)
        if e.response['Error']['Code'] == "404" or e.response['Error']['Code'] == "403":
            print("### The object does not exist. Screenshotting... ###")
        else:
            raise

    print('### Fetching: {} ###'.format(scannee))
    driver = WebDriverWrapper()
    driver.get_url(scannee)

    print('### Saving screenshot to: {} ###'.format(screenshot_key_path))
    driver.screenshot(screenshot_path)

    driver.close()

    # Upload screenshot to S3
    screenshot_key.upload_file(screenshot_path)
    return {'screenshot': 'https://glimpsefiles.s3.amazonaws.com/screenshots/' + screenshot_filename }
