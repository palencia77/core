'''
Created on 10/09/2014

@author: palencia77
'''

import json
import simplejson
import requests

data = {}
#Access token type recover password "ATRP" and status 
data['access_token'] = 'Oof1Sq5eYFKvDJe5OJJFED2k1aX6AeGFVEGN7iEmNog50WvUa5T9nV0mbKBzPDUaI2kDHErYb7mnjzAaI8sogpcM2J2AsqI4rcxAjuJYYhaWXqY6UY1qzVss8mLgxG1liGn0KXXJsAhrVQ4hwHiQ2s1a6UgHgXtHRXEkMmjVlE1MveGgrjTnoqW592HVQtZK2iYLNLJ5n7eUKRVXgHSBl0GF1qk0AQWqWLXzw7YndXxYVePN0STYlZWKMA06J9o9avev72ILR8'
data['password'] = '12345'

result = requests.post("http://localhost:5000/user/update/password", data = json.dumps(data))

print "=========================="
print "=======TEST RESULT========"
print "=========================="
print result.json()