'''
Created on 22/08/2014

@author: palencia77
'''
#===============================================================================
# TEST PARTNERS ASSOCIATED OR NO WITH ONE CAUSE (OPTIONAL FILTER BY NAME)
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_id_cause = '53ee6997ad0e7c3371f60372' #Required
global_associated = "True" #Required: True or False
global_name_filter = ""
global_page_number = 1
global_page_size = 7
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
    data['id_cause'] = global_id_cause
    data['associated'] = global_associated
    data['name_filter'] = global_name_filter
    data['page_number'] = global_page_number
    data['page_size'] = global_page_size
    
    result = requests.get("http://localhost:5000/partner/cause_association/find", params=data)
    cause_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print cause_result
    
else:
    print "Error: Failed to generate the token"