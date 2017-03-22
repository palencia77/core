'''
Created on 20/06/2014

@author: palencia77
'''
import json
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_old_password = '19104894' #Required
global_new_password = '87654321' #Required
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
    data['access_token'] = validate_result['access_token']
    data['old_password'] = global_old_password
    data['new_password'] = global_new_password
    
    result = requests.post("http://localhost:5000/user/change_password", data = json.dumps(data))
    change_password_result =  result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print change_password_result
    
else:
    print "Error: Failed to generate the token"
