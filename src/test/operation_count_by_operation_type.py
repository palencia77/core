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
global_bee_destination = "53c7f460e5ec721ad82dc93b" #Required
global_operation_type = "OTLA" #Required
global_start_date = "2014-01-25 17:00:38" #Required
global_end_date = "2014-06-30 17:04:08" #Required
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
    data['bee_destination'] = global_bee_destination
    data['operation_type'] = global_operation_type
    data['start_date'] = global_start_date
    data['end_date'] = global_end_date
    data['time_unit'] = global_time_unit
    
    result = requests.get("http://localhost:5000/operation/count_operation_type", params=data)
    operation_count = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print operation_count
    
else:
    print "Error: Failed to generate the token"