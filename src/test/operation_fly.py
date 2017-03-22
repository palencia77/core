'''
Created on 04/07/2014

@author: palencia77
'''
import json
import simplejson
import requests

#Test configuration
global_login = 'palencia_77@hotmail.com' #Required
global_password = '12345678' #Required
global_id_bee = '547785caad0e7c2ff9f520dc' #Required
global_app = "SOCIAL"
global_id_bee_destination = '541b1c6900cce84f362bc750' #Required
global_id_post_destination = '5478a190ad0e7c2a908149cf' #Required
global_id_award_destination = '54737ca5ad0e7c122947db05' #Required

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password
data['app'] = global_app

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
        
    #We create a new love action for cause
    data2 = {}
    data2['access_token'] = validate_result['access_token']
    data2['id_post_destination'] = None
    data2['id_award_destination'] = global_id_award_destination
    data2['id_bee_destination'] = None
    data2['id_bee'] = global_id_bee
    data2['app'] = global_app
    result = requests.post("http://localhost:5000/operation/fly/action", data=json.dumps(data2))
    fly_action_result = result.json()
            
    print ""
    print "==TEST RESULT FOR FLY ACTION=="
    print "=============================="
    print fly_action_result

else:
    print "Error: Failed to generate the token"
