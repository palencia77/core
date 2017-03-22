'''
Created on 22/08/2014

@author: palencia77
'''
#===============================================================================
# TEST CAUSE UPDATE PARTNER ASSOCIATION
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'j.palencia@domain.com' #Required
global_password = '19104894' #Required
global_id_cause = '53ee68aaad0e7c3371f6036d' #Required
global_partners_to_add = ['53f77311ad0e7c24ed084bd9','53f7734dad0e7c24ed084bdb','53f790aaad0e7c24ed084be0'] #Required
global_partners_to_remove = [] #Required
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
    data['partners_to_add'] = global_partners_to_add
    data['partners_to_remove'] = global_partners_to_remove
    
    result = requests.post("http://localhost:5000/cause/update/partners", data=json.dumps(data))
    cause_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print cause_result
    
else:
    print "Error: Failed to generate the token"