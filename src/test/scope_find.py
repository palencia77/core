'''
Created on 30/06/2014

@author: palencia77
'''
#===============================================================================
# TEST SCOPE/SUBSCOPE FIND
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_id_scope = "53bb416b66084508f16dd433"
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
    
    #SubScope data:
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_scope'] = global_id_scope
    result = requests.get("http://localhost:5000/scope/find", params=data)
    scope_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print scope_result
    
else:
    print "Error: Failed to generate the token"