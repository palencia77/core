'''
Created on 27/06/2014

@author: palencia77
'''
#===============================================================================
# TEST GET POSTCOMMENTS
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_page_number = 1 #Required
global_page_size = 2 #Required
global_id_post = "53ac78baad0e7c2899694b52"
global_with_resources = False
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
    
    #We get the bee timeline publications
    data = {}
    data['access_token'] = validate_result['access_token']
    data['page_number'] = global_page_number
    data['page_size'] = global_page_size
    data['id_post'] = global_id_post
    data['with_resources'] = global_with_resources
    
    result = requests.get("http://localhost:5000/comment/find", params=data )
    get_postcomments_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print get_postcomments_result
    
else:
    print "Error: Failed to generate the token"