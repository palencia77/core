'''
Created on 25/06/2014

@author: palencia77
'''
import json
import simplejson
import requests

#Test configuration
global_login = 'f.heredia@domain.com' #Required
global_password = '20349918' #Required
global_id_bee = '53b197e79b560f2cdf69123e' #Required

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:    
       
    #We create a new operation type and notification type
    data= {}
    requests.get("http://localhost:5000/operation/operation_type", data=json.dumps(data))
            
    #We create a new operation follow
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_bee_destination'] = '53b1e1c69b560f4c83a85b25'
    data['id_bee'] = global_id_bee
    data['quantity_love'] = 100        
    result = requests.post("http://localhost:5000/operation/give_love", data=json.dumps(data))
    follow_result = result.json()
            
    print ""
    print "==TEST RESULT GIVE LOVE="
    print "=========================="
    print follow_result

else:
    print "Error: Failed to generate the token"
