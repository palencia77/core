'''
Created on 20/06/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.services.services_post import *
from com.services.services_bee import *
from com.services.services_comment import *
from com.services.services_security import *
from com.services.services_notification import *
from com.tools.tools_response import *

"""
@summary: Service that allows create a new post comment
@param access_token:
@param id_bee:
@param id_post:
@param text:
@return: json data
@status: tested 26/06/2014
"""
@services_app.route('/comment/create', methods=['POST'])
def restful_comment_create():
    data={}
    try :
        data = json.loads(request.data)
        validate_token(data['access_token'])
        if data['id_bee'] is None:
            raise Exception('You must provide the id of bee')
        validate_token_owner(data['access_token'], data['id_bee'])
        comment_owner = get_bee_by_id(data['id_bee'])
        
        if data['id_post'] is None:
            raise Exception('You must provide the id of the post to which you create a post comment')
        comment_parent = get_post_by_id(data['id_post'])
        
        if data['text'] is None:
            raise Exception('You must provide the content text of the post comment')
        result ={}
        result['comment'] = create_postcomment(data['text'], comment_owner, comment_parent)
        notification_type = get_notification_type('NTCO')
        description = comment_owner.name + ' ha comentado tu publicacion'
        create_notification_destination_comment(comment_owner, comment_parent.owner, result['comment'],
                                                description, notification_type)
        result['message'] = 'ok'
        return make_template_response(result, 'comment/s_create.json')
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)

"""
@summary: Service that allows remove a post comment
@param access_token:
@param id_bee:
@param id_comment:
@return: json data
"""
@services_app.route('/comment/delete', methods=['POST'])
def restful_comment_delete():
    try :
        data = json.loads(request.data)
        validate_token(data['access_token'])
        
        if data['id_bee'] is None:
            raise Exception('You must provide the id of the post to which you create a post comment')
        else:
            id_bee = data['id_bee']
            
        validate_token_owner(data['access_token'], id_bee)        
        bee = get_bee_by_id(id_bee)
               
        if data['id_comment'] is None:
            raise Exception('You must provide the id of the post comment to which you remove')
        else:
            comment = get_postcomment_by_id(data['id_comment'])
              
        if (comment.owner != bee):
            raise Exception('You do not have permission to delete the comment')
        else:
            #Deleting the comment
            remove_postcomment(comment)            
            data = {}
            data['message'] = 'ok'
            return make_ok_response(data)
    
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
    
    '''
@summary: Method seeking comments having a particular post
@param access_token:
@param id_post:
@param page_number:
@param page_size: 
@status: result 
'''
@services_app.route('/comment/find/by/post', methods=['GET'])
def resful_get_comments_by_post():
    data={}
    try :
        data = {'access_token':request.args.get('access_token'),
                'page_size':request.args.get('page_size'), 
                'page_number':request.args.get('page_number'), 
                'id_post':request.args.get('id_post')}
        validate_token(data['access_token'])
        page_number = int(data['page_number'])
        page_size = int(data['page_size'])
        id_post = data['id_post']
        if (id_post is None):
            raise Exception('You must provide an identifier Post')
        post = get_post_by_id(id_post)
        if(post is not None):
            result = get_postcomments(post, page_number, page_size)
            return make_template_response(result, 'comment/s_find_by_post.json')
        else: 
            raise Exception('the post does not exist')
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
        # else : raise Exception('Invalid token!') #fin comprobar operaciones del token
        
"""
@summary: Service that allows remove a post comment
@param access_token:
@param id_bee:
@param text:
@param id_comment:
@return: json data
"""
@services_app.route('/comment/edit', methods=['POST'])
def restful_comment_edit():
    try :
        data = json.loads(request.data)
        validate_token(data['access_token'])
        
        if data['id_bee'] is None:
            raise Exception('You must provide the id of the post to which you create a post comment')
            
        validate_token_owner(data['access_token'], data['id_bee'])
        bee = get_bee_by_id(data['id_bee'])
               
        if data['id_comment'] is None or data['text'] is None:
            raise Exception('You must provide the data to which you update')
        else:
            comment = get_postcomment_by_id(data['id_comment'])
        if (comment.owner != bee):
            raise Exception('You do not have permission to delete the comment')
        else:
            #editing the comment
            edit_postcomment(comment,data['text'])            
            data = {}
            data['message'] = 'ok'
            return make_ok_response(data)
    
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)