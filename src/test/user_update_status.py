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
global_login = 'diony@gmail.com' #Required
global_password = '19104894' #Required
global_id_user = "58c0adf56e95522270722f99" #Required
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password
data['app']="SOCIAL"

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
        
    #Cause data:
    data = {}
    data['id_user'] = global_id_user
    data['access_token'] = validate_result['access_token']
    data['status'] = STATUS_OBJECT_ACTIVE
    
    result = requests.post("http://localhost:5000/user/update/status", data=json.dumps(data))
    user_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print user_result
    
else:
    print "Error: Failed to generate the token"