'''
Created on 18/07/2014

@author: palencia77
'''
#===============================================================================
# TEST CAUSE STATUS FIND
#===============================================================================

import json
import simplejson
import requests
from com.tools.objects_status import *

#Test configuration------------------------------------------------------------ 
global_login = 'f.heredia@domain.com' #Required
global_password = '20349918' #Required
global_status = STATUS_OBJECT_ACTIVE #Required
global_page_number = 1 #Required
global_page_size = 2 #Required
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
    data['access_token'] = validate_result['access_token']
    data['page_number'] = global_page_number
    data['page_size'] = global_page_size
    data['status'] = global_status
    data['name_filter'] = ""
    
    result = requests.get("http://localhost:5000/cause/status/find", params=data)
    cause_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print cause_result
    
else:
    print "Error: Failed to generate the token"