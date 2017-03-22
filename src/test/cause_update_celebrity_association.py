'''
Created on 22/08/2014

@author: palencia77
'''
#===============================================================================
# TEST CAUSE UPDATE CELEBRITY ASSOCIATION
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'j.palencia@domain.com' #Required
global_password = '19104894' #Required
global_id_cause = '53ee6997ad0e7c3371f60372' #Required
global_celebrities_to_add = ['53fca780ad0e7c15079ef789','53fca73ead0e7c15079ef785'] #Required
global_celebrities_to_remove = ['53fde211ad0e7c0cdde70474'] #Required
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
    data['celebrities_to_add'] = global_celebrities_to_add
    data['celebrities_to_remove'] = global_celebrities_to_remove
    
    result = requests.post("http://localhost:5000/cause/update/celebrities", data=json.dumps(data))
    cause_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print cause_result
    
else:
    print "Error: Failed to generate the token"