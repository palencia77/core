'''
Created on 10/09/2014

@author: palencia77
'''

import json
import simplejson
import requests

#Test configuration------------------------------------------------------------ 
global_login = 'Francelys' #Required
#------------------------------------------------------------------------------ 

#We get a new access token
data = {}
data['login'] = global_login

result = requests.get("http://localhost:5000/user/recover/password", params=data)

print "=========================="
print "=======TEST RESULT========"
print "=========================="
print result.json()