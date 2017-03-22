'''
Created on 20/06/2014

@author: palencia77
'''
import json
import simplejson 
import requests
import base64

data = {}
data['login'] = 'rvalera@najoconsultores.com'
data['password'] = 'admin'



result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'token' in validate_result:


    data = {}
    data['access_token'] = validate_result['token']
    
    print data


    result = requests.get("http://localhost:5000/bee/view", params=data )
    q_result = result.json() 
    
    print q_result    
