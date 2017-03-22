'''
Created on 30/06/2014

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
global_login = 'f.heredia@domain.com' #Required
global_password = '20349918' #Required
global_id_cause = "53e4d90e9b560f0c41ed8962" #Required
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
        
    #Cause data:
    data = {}
    data['id_cause'] = global_id_cause
    data['access_token'] = validate_result['access_token']
    data['status'] = STATUS_OBJECT_ACTIVE
    
    result = requests.post("http://localhost:5000/cause/update/status", data=json.dumps(data))
    cause_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print cause_result
    
else:
    print "Error: Failed to generate the token"