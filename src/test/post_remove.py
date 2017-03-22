'''
Created on 25/06/2014

@author: palencia77
'''
import json
import simplejson
import requests

data = {}
data['login'] = 'palencia77@gmail.com'
data['password'] = '19104894'

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    data = {}
    data['access_token'] = validate_result['access_token']
    print data
    
    data['id_post'] = '53add60ee5ec7236689b855b'
    data['id_bee'] = '53aaebdee5ec721a6e7e64b8'
    
    result = requests.post("http://localhost:5000/post/remove", data=json.dumps(data))
    print result.status_code
    print result.json()