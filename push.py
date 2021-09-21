import sys
import os
import requests

token = os.environ['token']
classCode = sys.argv[0]
information = sys.argv[1]

url = 'http://pushplus.hxtrip.com/send'
params = {
    'token': token, 
    'title': '上课提醒',
    'content': information,
    'topic': classCode
}
requests.get(url, params)
