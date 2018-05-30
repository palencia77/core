'''
Created on 20/06/2014

@author: palencia77
'''
import json
import requests

''' 
# frontend user for social app
payload = {'login': 'palencia77@domain.com', 'password': '19104894',
           'email': 'palencia77@domain.com', 'full_name': 'Jesus Palencia',
           'gender': 'Masculino', 'type': 'FRONTEND', 'birthday': None, 'phone': None, 'app': 'SOCIAL'}
'''

# admin user for backend app
payload = {'login': 'admin', 'password': '19104894',
           'email': 'admin@domain.com', 'full_name': 'Mr. Banckend Admin',
           'gender': 'Masculino', 'type': 'BACKEND', 'birthday': None, 'phone': None, 'app': 'BACKEND'}
r = requests.post("http://localhost:5000/user/register", data=json.dumps(payload))
print r.json()
