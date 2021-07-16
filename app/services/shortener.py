from werkzeug.wrappers import response
from app import db
import requests, os
from datetime import datetime


def check_short_url(url):    
    result = db.check_short_url(url)
    return result

def save_new_url(url):
    valid_start = url.startswith("http://") or url.startswith("https://")
    if not valid_start:
        url = "http://" + url

    short_url = db.save_new_url(url)
    return short_url

def save_new_access(headers, result):
    body = {
        'headers': dict(headers),
        'short_url': result['short_url'],
        'complete_url': result['complete_url'],
        'created_at': result['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f"),
        'used_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    }
    url = os.environ.get('CLOUD_SEND_TO_QUEUE')
    if url:
        response = requests.post(url, json=body)
        print(response.text)
        return True

    print('No url set for cloud function')
    