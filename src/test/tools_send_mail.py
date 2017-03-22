'''
Created on 22/10/2014
@author: palencia77
'''
#===============================================================================
# TEST TOOLS SEND MAIL
#===============================================================================

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'ramon.valera@gmail.com' #Required
global_password = '123456' #Required
global_app = 'Backend' #Required
global_address = 'palencia_77@yahoo.com' #Required
global_subject = 'Asunto del email' #Required
global_text = "Contenido del email" #Required
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
    data['address'] = global_address
    data['subject'] = global_subject
    data['text'] = global_text
    result = requests.post("http://localhost:5000/tools/send_mail", data=json.dumps(data))
    tools_send_mail = result.json()
    print "=========================="
    print "=======TEST RESULT========"
    print "=========================="
    print tools_send_mail
    
else:
    print "Error: Failed to generate the token"