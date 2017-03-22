'''
Created on 25/06/2014

@author: palencia77
'''
#===============================================================================
# TEST REMOVE RESOURCE
#===============================================================================

import json
import simplejson
import requests

#Test configuration
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_id_bee = '53aaebdee5ec721a6e7e64b8' #Required
global_id_resource = '53bf01d7e5ec722c906e5012' #Required

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
        
    #We remove the comment
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_bee'] = global_id_bee
    data['id_resource'] = global_id_resource        
    result = requests.post("http://localhost:5000/bee/resource/remove", data=json.dumps(data))
    remove_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print remove_result
else:
    print "Error: Failed to generate the token"
