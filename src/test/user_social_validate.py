'''
Created on 30/06/2014

@author: palencia77
'''
#===============================================================================
# USER SOCIAL VALIDATE
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
full_name = 'Maria Carolina' #Required
email = 'mariac@gmail.com' #Required
id_social_network = 'AJGaksaJSHGSkjdshJksDgKJgdkLODiu'
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['full_name'] = full_name
data['email'] = email
data['id_social_network'] = id_social_network

result = requests.post("http://localhost:5000/user/social_network/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
else:
    print "Error: Failed to generate the token"