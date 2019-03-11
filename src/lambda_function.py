import hashlib
import urllib
import glimpse_driver as gd
from s3_help import S3
from selenium.common.exceptions import WebDriverException

def md5_str(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return str(m.hexdigest())

def filter(url):
    bad_words = ['file://']
    if any(word in url for word in bad_words):
        raise Exception('suspicious string found in URL')

def lambda_handler(event, context):

    # Decode the url argument and fix if no protocol
    url = urllib.parse.unquote(event['url'])
    if 'http' not in url:
        url = 'http://' + url

    # Filter for potentially malicious or invalid URLs
    filter(url)

    # Calculate MD5 hash of URL 
    screenshot_filename = md5_str(url) + '.png'
    local_path = '/tmp/' + screenshot_filename
    remote_path = 'screenshots/' + screenshot_filename

    s3 = S3('glimpsefiles')
    s3_key = s3.get_key(remote_path)

    # Don't update if update==false or doesn't exist
    # TODO: If update != true or false. Invalid request.
    if 'update' in event.keys():
        if event['update'] != 'true':
            exists = s3.check_exists('screenshots/', screenshot_filename)
            if exists: # Screenshot exists for this hashed URL. Return the link.
                return exists
    else:
        exists = s3.check_exists('screenshots/', screenshot_filename)
        if exists: # Screenshot exists for this hashed URL. Return the link.
            return exists


    glimpse = gd.GlimpseDriver()
    try:
        glimpse.driver.get(url)
        glimpse.screenshot(local_path)
        s3.upload_file(s3_key, local_path)
        return {'screenshot': 'https://glimpsefiles.s3.amazonaws.com/screenshots/' + screenshot_filename, 'effective_url': glimpse.driver.current_url}

    except WebDriverException as e:
        return {'error_message': e.msg}
