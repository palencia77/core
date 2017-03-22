'''
Created on 14/07/2014

@author: palencia77
'''
#===============================================================================
# TEST REMOVE SCOPE
#===============================================================================

import json
import simplejson
import requests

#Test configuration
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_id_sub_scope = '53c53a4fe5ec7218ae91102b' #Required

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
        
    #We remove the scope
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_subscope'] = global_id_sub_scope        
    result = requests.post("http://localhost:5000/subscope/remove", data=json.dumps(data))
    remove_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print remove_result
else:
    print "Error: Failed to generate the token"
