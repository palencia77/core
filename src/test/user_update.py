'''
Created on 20/06/2014

@author: palencia77
'''
import json
import requests
access_token ='EeeBhnuuyWiWDpoTAcUfOPRtey45mZcbc25u6P9CQd6ooabnj7UFJBIz2gbxBXSd6vSf2GY8JIvRjclyAMs4XbENDl9Ls581vPbHEaHJTNcz8ObPEIP3SsOA84qwDcSH1T5xkrYBfixcGNbFIgLxN8UOeXvUdA4g8kygcgFwRDhaguZJ0gDHa4zSGgQQRfJXaAkrbaG1sq8JZ06xkHPulmu2PGRwnL5pTkzmsRVNyOotQPvlt6GfnhiAQ7jVbCA6A6WRU1WaDxwO6p4rtAXFKfO73MKGtJDgMYfaEzrXwKKg3Y7cvzmo3TLphpbUFWgJRTPwnL0lodKOHXoci1q33t'
payload = {'id_user':'540885929b560f1dc772a87f', 'email':'h.francelys@gemail.com',
           'full_name':'Francelys Elimar Heredia',
           'gender':'Femenino', 'access_token':access_token, 'birthday':'2014-09-18T04:30:00.000Z', 'phone':'122232'}
r = requests.post("http://localhost:5000/user/update", data = json.dumps(payload))
print r.json()