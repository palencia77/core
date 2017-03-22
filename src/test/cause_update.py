'''
Created on 30/06/2014

@author: palencia77
'''
#===============================================================================
# TEST CAUSE UPDATE
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'j.palencia@domain.com' #Required
global_password = '19104894' #Required
glabal_id_subscope = "53b6b2b7ad0e7c1382fe5572" #Required
global_ambassadors = ['53b42974ad0e7c1885bc844b'] #Required
global_responsible = "j.palencia@domain.com"
global_id_cause = "53bc02d4ad0e7c14c530f7d9" #Required
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
    data['id_cause'] = global_id_cause
    data['access_token'] = validate_result['access_token']
    data['name'] = 'One legg for cristians'
    data['description'] = 'Description of the cause'
    data['risk_classification'] = "ALTO"
    data['geographic_location'] = None
    data['goal'] = "Raising funds to help with Aura's chemotherapy"
    data['id_subscope'] = glabal_id_subscope
    data['start_date'] = None
    data['closing_date'] = None
    data['love_goal'] = 250000
    data['ambassadors'] = global_ambassadors
    data['beneficiary'] = "Aura Montes"
    data['id_responsible'] = global_responsible
    
    result = requests.post("http://localhost:5000/cause/update", data=json.dumps(data))
    cause_result = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print cause_result
    
else:
    print "Error: Failed to generate the token"