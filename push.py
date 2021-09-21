import sys
import os
import requests

classCode = sys.argv[1]
information = ' '.join(sys.argv[2:])
token = os.environ['token']

url = 'http://pushplus.hxtrip.com/send'
params = {
    'token': token, 
    'title': '上课提醒',
    'content': information,
    'topic': classCode
}
requests.get(url, params)
