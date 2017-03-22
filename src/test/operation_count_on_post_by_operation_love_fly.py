'''
Created on 05/08/2014

@author: palencia77
'''
#===============================================================================
# TEST OPERATION COUNT BY OPERATION TYPE
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_id_cause = "53ea69bde5ec72355cdd01c3" #Required
global_operation_type_one = "OTLA" #Required
global_operation_type_two = "OTFLY" #Required
global_time_unit = "day"
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
        
    #Cause data:
    data = {}
    data['access_token'] = validate_result['access_token']
    data['owner'] = global_id_cause
    data['operation_type_one'] = global_operation_type_one
    data['operation_type_two'] = global_operation_type_two
    data['time_unit'] = global_time_unit
    
    result = requests.get("http://localhost:5000/operation/count_operation_on_post_by_cause", params=data)
    operation_count = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print operation_count
    
else:
    print "Error: Failed to generate the token"