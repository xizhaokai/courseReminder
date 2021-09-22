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
# 1.需要明確，微信知否支持回車換行。
# 2.如果支持，需要在這邊處理。這個脚本可以理解是發信息到微信的。
# 可以在excel裏面需要換行的地方配置為$.
# 然後這裏
# 李强$11223 
# ==>
# 李强
# 11223 
# 1.需要明確，微信知否支持回車換行。
# 2.如果支持，需要在這邊處理。這個脚本可以理解是發信息到微信的。
# 可以在excel裏面需要換行的地方配置為$.
# 然後這裏
# 李强$11223 
# ==>
# 李强
# 11223 
params['content'] = str.replace(params['content'], '$', '\n')
requests.get(url, params)
