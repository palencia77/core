'''
Created on 02/07/2014

@author: palencia77
'''
#===============================================================================
# TEST BEE FRIENDS FIND
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'j.palencia@domain.com' #Required
global_password = '19104894' #Required
global_id_post = '53ee6bd7ad0e7c3371f6038d'
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
    
    #We get the bee friends
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_post'] = global_id_post
    
    result = requests.get("http://localhost:5000/post/find/by_id", params=data )
    post_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print post_result
    
else:
    print "Error: Failed to generate the token"