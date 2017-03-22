'''
Created on 26/06/2014

@author: palencia77
'''
#===============================================================================
# TEST BEE TIMELINE
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'j.palencia@domaincom' #Required
global_password = '19104894' #Required
global_page_number = 1 #Required
global_page_size = 20 #Required
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password
id_bee = '53e23dfbad0e7c18462a9118'
result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
    
    #We get the bee timeline publications
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_bee'] = id_bee
    data['page_number'] = global_page_number
    data['page_size'] = global_page_size
    
    result = requests.get("http://localhost:5000/bee/post/owner/find", params=data )
    timeline_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print json.dumps(timeline_result, indent=4, sort_keys=True)
    
else:
    print "Error: Failed to generate the token"