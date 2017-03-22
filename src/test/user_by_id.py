'''
Created on 03/09/2014

@author: palencia77
'''

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'f.heredia@domain.com' #Required
global_password = '20349918' #Required
global_id_user = '540612dc9b560f2b3507f2bb'
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
    data['access_token'] = validate_result['access_token']
    data['id_user'] = global_id_user
    
    
    result = requests.get("http://localhost:5000/user/find/by_id", params=data)
    user_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print user_result
    
else:
    print "Error: Failed to generate the token"