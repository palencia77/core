'''
Created on 25/06/2014

@author: palencia77
'''
import json
import simplejson
import requests

#Test configuration
global_login = 'palencia77@gmail.com' #Required
global_password = '19104894' #Required
global_id_bee = '53aaebdee5ec721a6e7e64b8' #Required

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
    post_result = result.json()
    
    if 'id_post' in post_result:
        print "id_post: " + post_result['id_post']
        
        #We create a new post comment
        data = {}
        data['access_token'] = validate_result['access_token']
        data['id_post'] = post_result['id_post']
        data['id_bee'] = global_id_bee
        data['text'] = 'This is a comment on a post'

        result = requests.post("http://localhost:5000/postcomment/create", data=json.dumps(data))
        comment_result = result.json()
        
        if 'id_comment' in comment_result:
            print "=========================="
            print "=======TEST RESULT========"
            print "=========================="
            print comment_result
        else:
            print "Error: Failed to generate the postcomment"
    
    else:
        print "Error: Failed to generate the post"

else:
    print "Error: Failed to generate the token"
