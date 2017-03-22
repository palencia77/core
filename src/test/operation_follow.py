'''
Created on 25/06/2014

@author: palencia77
'''
import json
import simplejson
import requests

#Test configuration
global_login = 'f.heredia@domain.com' #Required
global_password = '20349918' #Required
global_id_bee = '53b32d8e9b560f214a9d843e' #Required

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    
    #We create a new operation type and notification type
    data= {}
    requests.get("http://localhost:5000/operation/operation_type", data=json.dumps(data))
            
    #We create a new operation follow
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_bee_destination'] = '53b313779b560f154e13d4ea'
    data['id_bee'] = global_id_bee        
    result = requests.post("http://localhost:5000/operation/follow", data=json.dumps(data))
    follow_result = result.json()
            
    print ""
    print "==TEST RESULT FOLLOW="
    print "=========================="
    print follow_result

else:
    print "Error: Failed to generate the token"
