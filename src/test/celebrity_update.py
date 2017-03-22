'''
Created on 09/06/2014

@author: palencia77
'''
#===============================================================================
# TEST CELEBRITY UPDATE
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_id_celebrity = '53bff531ad0e7c11f5a9a3db'
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
        
    #Celebrity data:
    data = {}
    data['access_token'] = validate_result['access_token']
    data['name'] = 'Julian Casablancas'
    data['description'] = 'Cuenta oficial de Julian Casablancas'
    data['geographic_location'] = None
    data['id_celebrity'] = global_id_celebrity
    result = requests.post("http://localhost:5000/celebrity/update", data=json.dumps(data))
    print result.status_code
    celebrity_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print celebrity_result
    
else:
    print "Error: Failed to generate the token"