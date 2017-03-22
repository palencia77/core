'''
Created on 02/07/2014

@author: palencia77
'''
#===============================================================================
# TEST BEE PARTNERS FIND
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_page_number = 1 #Required
global_page_size = 3 #Required
global_id_bee = '53aaebdee5ec721a6e7e64b8'
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
    
    #We get the bee partners
    data = {}
    data['access_token'] = validate_result['access_token']
    data['page_number'] = global_page_number
    data['page_size'] = global_page_size
    data['id_bee'] = global_id_bee
    
    result = requests.get("http://localhost:5000/bee/partners/find", params=data )
    bee_friends_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print bee_friends_result
    
else:
    print "Error: Failed to generate the token"