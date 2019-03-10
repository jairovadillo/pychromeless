import hashlib
import urllib
import glimpse_driver as gd
from s3_help import S3

def md5_str(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return str(m.hexdigest())

def filter(url):
    bad_words = ['file://']
    if any(word in url for word in bad_words):
        raise Exception('suspicious string found in URL')

def lambda_handler(event, context):

    # Fail if URL not defined
    url = urllib.parse.unquote(event['url'])

    # Filter for potentially malicious or invalid URLs
    filter(url)

    # Calculate MD5 hash of URL 
    screenshot_filename = md5_str(url) + '.png'
    local_path = '/tmp/' + screenshot_filename
    remote_path = 'screenshots/' + screenshot_filename

    s3 = S3('glimpsefiles')
    s3_key = s3.get_key(remote_path)

    glimpse = gd.GlimpseDriver()
    glimpse.driver.get(url)

    glimpse.screenshot(local_path)
    s3.upload_file(s3_key, local_path)

    return {'screenshot': 'https://glimpsefiles.s3.amazonaws.com/screenshots/' + screenshot_filename }
