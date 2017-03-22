'''
Created on 18/07/2014

@author: palencia77
'''
#===============================================================================
# TEST CELEBRITY FIND ALL (OPTIONAL: FILTER BY STATUS AND NAME)
#===============================================================================

import json
import simplejson
import requests
from com.tools.objects_status import *

#Test configuration------------------------------------------------------------ 
global_login = 'j.palencia@domain.com' #Required
global_password = '19104894' #Required
global_status = STATUS_OBJECT_ACTIVE #Required
global_name_filter = ""
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
    data['name_filter'] = global_name_filter
    data['status'] = STATUS_OBJECT_ACTIVE
    #data['device'] = "Mobile"
    
    result = requests.get("http://localhost:5000/celebrity/find/all", params=data)
    celebrity_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print celebrity_result
    
else:
    print "Error: Failed to generate the token"