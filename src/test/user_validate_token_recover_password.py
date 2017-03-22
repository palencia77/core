'''
Created on 10/09/2014

@author: palencia77
'''

import json
import simplejson
import requests

data = {}
#Access token type recover password "ATRP" and status 
data['access_token'] = 'iAwl311G52gONN8FVd5fMXzYtgi3Cc2jN959woicTdlQKZkIMyJshnlkeCXTtCZwzXlm4h6JrvIYjQdVNEL9bhWHfz9uGn0m65uoDgWdIzDOMh8jMYn2VzRi1miuXxpTEtn0DX5uveaj8wVCEUAG237GJIBBUMCwB1HsPgb3YjbFuGr4nefnjigKdnaQlAVoL87uFAgHq2tdNimOtFyy9XQOYvg39ciyuSy2hnUKEeFsWS1jbWsQMDG3DKqhv8DU23tjM0Cro25DSSO1AOFJkQuue7lP9pADNqaSaPMa7ybW4H4dzeixFFMKsBc0STVlXehJzIt84GehyBU3PL6clwjX21z68TZ'

result = requests.get("http://localhost:5000/user/validate_token/recover_password", params=data)

print "=========================="
print "=======TEST RESULT========"
print "=========================="
print result.json()