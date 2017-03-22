'''
Created on 25/06/2014

@author: palencia77
'''
import json
import simplejson
import requests

#Test configuration
global_login = 'palencia_77@hotmail.com' #Required
global_password = '12345678' #Required
global_id_bee = '547785caad0e7c2ff9f520dc' #Required
global_app = "SOCIAL"

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password
data['app'] = global_app

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()

if 'access_token' in validate_result:
    print validate_result

    '''
    #We create a new post
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_bee'] = global_id_bee
    data['text'] = 'This is the content of the post'
    resource={}
    data['resource'] = resource

    result = requests.post("http://localhost:5000/post/create", data=json.dumps(data))
    post_result = result.json()
    
    #We create a new operation type
    data= {}
    requests.get("http://localhost:5000/operation/operation_type", data=json.dumps(data))
    
    if 'id_post' in post_result:             
               
        #We create a new love action post
        data = {}
        data['access_token'] = validate_result['access_token']
        data['id_post_destination'] = post_result['id_post']
        data['id_bee'] = global_id_bee
        
        result = requests.post("http://localhost:5000/operation/love/action", data=json.dumps(data))
        print result.status_code
        love_action_result = result.json()
                
        print "==TEST RESULT FOR POST=="
        print "=========================="
        print love_action_result
        
        
        #We create a new post comment
        data = {}
        data['access_token'] = validate_result['access_token']
        data['id_post'] = post_result['id_post']
        data['id_bee'] = global_id_bee
        data['text'] = 'This is a comment on a post'
        result = requests.post("http://localhost:5000/postcomment/create", data=json.dumps(data))
        comment_result = result.json()
        
        if 'id_comment' in comment_result:
            #We create a new love action comment
            data = {}
            data['access_token'] = validate_result['access_token']
            data['id_comment_destination'] = comment_result['id_comment']
            data['id_bee'] = global_id_bee
            result = requests.post("http://localhost:5000/operation/love/action", data=json.dumps(data))
            print ""
            print "==TEST RESULT FOR COMMENT=="
            print "=========================="
            print  result.json()
            
        else:
            print "Error: Failed to generate the comment"                  
    else:
        print "Error: Failed to generate the post"
    '''
        
    #We create a new love action for cause
    data = {}
    data['access_token'] = validate_result['access_token']
    data['id_post_destination'] = '5478a190ad0e7c2a908149cf'
    data['id_bee_destination'] = None
    data['id_comment_destination'] = None
    data['id_bee'] = global_id_bee
    data['app'] = global_app
    result = requests.post("http://localhost:5000/operation/love/action", data=json.dumps(data))
    love_action_result = result.json()

    print ""
    print "==TEST RESULT=="
    print "=========================="
    print love_action_result

else:
    print "Error: Failed to generate the token"
