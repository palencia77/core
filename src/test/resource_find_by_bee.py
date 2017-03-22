'''
Created on 30/06/2014

@author: palencia77
'''
#===============================================================================
# TEST FIND RESOURCES BY BEE
#===============================================================================

import json
import simplejson
import requests

#Test configuration
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_id_bee = '53aaebdee5ec721a6e7e64b8' #Required
global_page_number = 1 #Required
global_page_size = 3 #Required

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
    #get resources of a bee
    data= {}
    data['access_token'] = validate_result['access_token']
    data['page_number'] = global_page_number
    data['page_size'] = global_page_size
    data['id_bee'] = global_id_bee
    result = requests.get("http://localhost:5000/resource/find_by_bee", params=data)
    resources_result = result.json()
            
    print "==TEST RESULT=="
    print "=========================="
    print resources_result

else:
    print "Error: Failed to generate the token"