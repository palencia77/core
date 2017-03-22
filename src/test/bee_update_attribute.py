'''
Created on 25/11/2014

@author: palencia77
'''
import json
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'jorgechaviel@gmail.com' #Required
global_password = '123456' #Required
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
    data = {}
    geographic_location={}
    data['id_bee'] = '5473887ee5ec727347f5fe37'
    data['access_token'] = validate_result['access_token']
    data['attribute'] = 'email'
    data['value'] = "jorgechaviel@gmail.com"
    result = requests.post("http://localhost:5000/bee/update/attribute", data=json.dumps(data))
    print result.status_code
    print ""
    print "==TEST RESULT Bee update Attribute="
    print "=========================="
    print result.json()
else:
    print "Error: Failed to generate the token"
   