'''
Created on 19/08/2014

@author: palencia77
'''
import json
import simplejson
import requests

#Test configuration
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    
    #We create a new operation type
    data= {}
    requests.get("http://localhost:5000/operation/operation_type", data=json.dumps(data))
            
    #We create a new operation logout
    data = {}
    data['access_token'] = validate_result['access_token']  
    result = requests.post("http://localhost:5000/operation/logout", data=json.dumps(data))
    logout_result = result.json()
            
    print ""
    print "==TEST RESULT LOGOUT="
    print "=========================="
    print logout_result

else:
    print "Error: Failed to generate the token"
