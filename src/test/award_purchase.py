'''
Created on 02/12/2014

@author: palencia77
'''
#===============================================================================
# TEST AWARD PURCHASE
#===============================================================================

import json
import simplejson
import requests
from com.tools.objects_status import *

#Test configuration------------------------------------------------------------ 
global_login = 'h.francelys@gmail.com' #Required
global_password = '20349918' #Required
global_id_bee = "5452ad1800cce844dbf0de21" #Required
global_id_award = "53f518a900cce841a3c71587" #Required
global_app = "SOCIAL"
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password
data['app'] = global_app

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
        
    #Cause data:
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_bee'] = global_id_bee
    data['id_award'] = global_id_award
    
    result = requests.post("http://localhost:5000/award/purchase", data = json.dumps(data))
    award_purchase_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print award_purchase_result
    
else:
    print "Error: Failed to generate the token"