'''
Created on 08/07/2014

@author: palencia77
'''
#===============================================================================
# TEST SUB_SCOPES_BY_SCOPE FIND
#===============================================================================

import json
import simplejson
import requests
from com.tools.objects_status import *

#Test configuration------------------------------------------------------------ 
global_login = 'Francelys' #Required
global_password = '12345' #Required
global_id_scope = "53ee62faad0e7c3371f6034e" #Required
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
    data['id_scope'] = global_id_scope
    data['page_number'] = 1
    data['page_size'] = 10
    data['name_filter'] = ""
    data['status'] = STATUS_OBJECT_ACTIVE
    result = requests.get("http://localhost:5000/scope/sub_scopes/find", params=data)
    sub_scopes_by_scope_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print sub_scopes_by_scope_result
    
else:
    print "Error: Failed to generate the token"