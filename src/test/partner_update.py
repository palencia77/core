'''
Created on 30/06/2014

@author: palencia77
'''
#===============================================================================
# TEST PARTNER UPDATE
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'j.palencia@domain.com' #Required
global_password = '19104894' #Required
global_id_partner = '53bc1eb1ad0e7c243939ce28' #Required
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
    data['id_partner'] = global_id_partner
    data['name'] = 'Pepsico'
    data['description'] = 'Description of the partner'
    data['geographic_location'] = None
    
    result = requests.post("http://localhost:5000/partner/update", data=json.dumps(data))
    partner_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print partner_result
    
else:
    print "Error: Failed to generate the token"