import hashlib
import urllib
from datetime import datetime
import glimpse_driver as gd
from s3_help import S3
from db_help import DynamoDB
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
    # Filter for potentially malicious or invalid URLs
    filter(url)

    if 'http' not in url:
        url = 'http://' + url

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Calculate MD5 hash of URL
    url_hash = md5_str(url)
    return_data = {'urlhash': url_hash} 
    screenshot_filename = url_hash + '.png'
    local_path = '/tmp/' + screenshot_filename
    remote_path = 'screenshots/' + screenshot_filename

    db = DynamoDB('glimpsedata')

    exists = False
    db_data = db.get({'urlhash': url_hash})
    
    if db_data is None:
        db_data = {'urlhash': url_hash, 'url': url, 'timescanned': timestamp, 'numscans': 1}
    else:
        exists = True
        db_data['timescanned'] = timestamp

    s3 = S3('glimpsefiles')
    s3_key = s3.get_key(remote_path)

    # Don't update if update==false or doesn't exist
    if 'update' in event.keys():
        if str(event['update']).lower() != 'true':
            if exists:
                return return_data
    else:
        if exists:
            return return_data


    glimpse = gd.GlimpseDriver()
    try:
        glimpse.driver.get(url)
        glimpse.screenshot(local_path)
        s3.upload_file(s3_key, local_path)

        db_data['effectiveurl'] = glimpse.driver.current_url
        db_data['title'] = glimpse.driver.title
        if exists:
            db_data['numscans'] += 1
        else:
            db_data['numscans'] = 1
        db.put(db_data)

        return return_data

    except WebDriverException as e:
        return {'error_message': e.msg}
