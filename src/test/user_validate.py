'''
Created on 30/06/2014

@author: palencia77
'''
# ===============================================================================
# TEST USER VALIDATE
# ===============================================================================

import json
import requests

# Test configuration------------------------------------------------------------
global_login = 'palencia77@domain.com'  # Required
global_password = '19104894'  # Required
global_app = 'SOCIAL'  # Required
# ------------------------------------------------------------------------------

# We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password
data['app'] = global_app

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()
print validate_result
