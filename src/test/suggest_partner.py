'''
Created on 26/06/2014

@author: palencia77
'''
#===============================================================================
# TEST SUGGEST PARTNER
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'j.palencia@domain.com' #Required
global_password = '19104894' #Required
global_id_bee = '53b2b69fad0e7c0e16215753'
global_page_number = 1 #Required
global_page_size = 5 #Required
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
    
    #We get the suggested causes for a bee
    data = {}
    data['access_token'] = validate_result['access_token']
    data['page_number'] = global_page_number
    data['page_size'] = global_page_size
    data['id_bee'] = global_id_bee
    
    result = requests.get("http://localhost:5000/suggest/partner", params=data )
    suggest_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print suggest_result
    
else:
    print "Error: Failed to generate the token"