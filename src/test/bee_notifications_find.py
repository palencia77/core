'''
Created on 30/06/2014

@author: palencia77
'''
import json
import simplejson
import requests

#Test configuration
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_id_bee = '53aaebdee5ec721a6e7e64b8' #Required
global_page_number = 1 #Required
global_page_size = 2 #Required
global_notification_status = 'pending' #Required

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']
    
    #We create a new post
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_bee'] = global_id_bee
    data['text'] = 'This is the content of the post'
    resource={}
    data['resource'] = resource
    
    result = requests.post("http://localhost:5000/post/create", data=json.dumps(data))
    
    #We create a new operation type and notification type
    data= {}
    requests.get("http://localhost:5000/operation/operation_type", data=json.dumps(data))
    
        
    #We create a new operation follow
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_bee_destination'] = '53aaebdee5ec721a6e7e64b8'
    data['id_bee'] = global_id_bee        
    result = requests.post("http://localhost:5000/operation/follow", data=json.dumps(data))
            
        #We create a new operation type and notification type
    data= {}
    data['access_token'] = validate_result['access_token']
    data['page_number'] = global_page_number
    data['page_size'] = global_page_size
    data['id_bee'] = global_id_bee
    data['notification_status'] = global_notification_status
    result = requests.get("http://localhost:5000/notification/find", params=data)
    notifications_result = result.json()
            
    print ""
    print "==TEST RESULT NOTIFICATIONS FIND="
    print "=========================="
    print notifications_result

else:
    print "Error: Failed to generate the token"