'''
Created on 30/06/2014

@author: palencia77
'''
#===============================================================================
# TEST BEE REMOVE
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'j.palencia@domaincom' #Required
global_password = '19104894' #Required
global_id_bee = '53bfef65ad0e7c11f5a9a3cd' #Required
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
        
    #Partner data:
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_bee'] = global_id_bee
    
    result = requests.post("http://localhost:5000/bee/remove", data=json.dumps(data))
    print result.status_code
    bee_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print bee_result
    
else:
    print "Error: Failed to generate the token"