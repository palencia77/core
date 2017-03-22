'''
Created on 30/06/2014

@author: palencia77
'''
import json
import requests

data = {}
data['login'] = 'ejemplo@ejemplo.com'
data['password'] = '123456'
result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    data = {}
    geographic_location={}
    data['id_bee'] = '53b7039fb797e31d30308291'
    data['access_token'] = validate_result['access_token']
    data['name'] = 'ROSA PEREZ'
    data['gender'] = 'Femenino'
    data['description'] = 'Description x'
    data['full_name'] = 'ROSA PEREZ'
    data['birthday'] = '2014-07-01'
    geographic_location['lat']="-10.555"
    geographic_location['long']="5.90"
    geographic_location['country']="Venezuela"
    data['geographic_location']=geographic_location
    print data
    result = requests.post("http://localhost:5000/bee/update", data=json.dumps(data))
    print result.status_code
    print ""
    print "==TEST RESULT Bee update="
    print "=========================="
    print result.json()
else:
    print "Error: Failed to generate the token"
   