'''
Created on 11/07/2014

@author: palencia77
'''
import json
import simplejson
import requests

#Test configuration
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_id_resource = '53bf01d6e5ec722c906e5011' #Required

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
    #get resource of a bee
    data= {}
    data['access_token'] = validate_result['access_token']
    data['id_resource'] = global_id_resource
    result = requests.get("http://localhost:5000/bee/resource/view", params=data)
    resource_result = result.json()
            
    print "==TEST RESULT=="
    print "=========================="
    print resource_result

else:
    print "Error: Failed to generate the token"