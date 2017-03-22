'''
Created on 01/07/2014

@author: palencia77
'''
import json
import simplejson
import requests

#Test configuration
global_login = 'f.heredia123@domain.com' #Required
global_password = '20349918' #Required
global_id_bee = '53b313779b560f154e13d4ea' #Required

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
               
    #We create a new operation friend_request_response
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_notification'] = '53b2bbb99b560f12cf5cf064'
    data['id_bee'] = global_id_bee        
    result = requests.post("http://localhost:5000/notification/read", data=json.dumps(data))
    friend_request_result = result.json()
            
    print ""
    print "==TEST RESULT NOTIFICATION READ="
    print "=========================="
    print friend_request_result

else:
    print "Error: Failed to generate the token"
