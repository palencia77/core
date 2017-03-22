'''
Created on 18/11/2014

@author: palencia77
'''
#===============================================================================
# TEST AWARD STATUS FIND
#===============================================================================

import json
import simplejson
import requests
from com.tools.objects_status import *

#Test configuration------------------------------------------------------------ 
global_login = 'palencia77@gmail.com' #Required
global_password = '123456' #Required
global_status = "INACTIVE" #Required
global_page_number = 1 #Required
global_page_size = 10 #Required
global_app = "SOCIAL"
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password
data['app'] = global_app

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
    data['app'] = global_app
    
    result = requests.get("http://localhost:5000/award/find/by/status", params=data)
    award_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print award_result
    
else:
    print "Error: Failed to generate the token"