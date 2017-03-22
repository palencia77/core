'''
Created on 30/06/2014

@author: palencia77
'''
#===============================================================================
# TEST SCOPE FIND ALL
#===============================================================================

import json
import simplejson
import requests
from com.tools.objects_status import *

#Test configuration------------------------------------------------------------ 
global_login = 'Francelys' #Required
global_password = '12345' #Required
global_page_number = 1
global_page_size = 10
global_with_subscopes = False
#------------------------------------------------------------------------------ 
#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password
data['app'] = "Backend"

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
    
    #SubScope data:
    data = {}
    data['access_token'] = validate_result['access_token']
    data['page_number'] = global_page_number
    data['page_size'] = global_page_size
    data['status'] = STATUS_OBJECT_ACTIVE
    data['name_filter'] = "Ambiente"
    
    result = requests.get("http://localhost:5000/scope/all", params=data)
    scope_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print scope_result
    
else:
    print "Error: Failed to generate the token"