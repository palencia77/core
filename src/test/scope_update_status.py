'''
Created on 12/09/2014

@author: palencia77
'''
#===============================================================================
# TEST CAUSE UPDATE
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
        
    #Cause data:
    data = {}
    data['id_scope'] = global_id_scope
    data['access_token'] = validate_result['access_token']
    data['status'] = STATUS_OBJECT_ACTIVE
    
    result = requests.post("http://localhost:5000/scope/update/status", data=json.dumps(data))
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print result.json()
    
else:
    print "Error: Failed to generate the token"