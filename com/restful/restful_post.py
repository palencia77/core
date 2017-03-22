'''
Created on 20/06/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.tools.tools_response import *
from com.services.services_post import *
from com.services.services_bee import *
from com.services.services_security import *
from com.tools.app_types import *

"""
@summary: This service allows you to save a Post
@param access_token
@param id_bee: Bee Person, Cause, Celebrity or Partner
@param title: 
@param text:
@param with_resource:
@param app:
@param resources: List of resources on Json format
@return: id_post and message
"""
@services_app.route('/post/create', methods=['POST'])
def restful_post_create():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        
        if data['id_bee'] is not None:
            bee = get_bee_by_id(data['id_bee'])
        else:
            raise Exception('You must provide the id of bee that is creating the post')
        
        if data['app'] is None:
            raise Exception('You must provide the app')
        elif data['app'] != APP_BACKEND:
            validate_token_owner(data['access_token'], data['id_bee']) 
        
        post = create_post(bee, data['title'], data['text'], data['with_resource'], data['resources'])
        data = {}
        data['message'] = 'ok'
        data['post'] = post
        return make_template_response(data, 'post/b_create.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: service that receives data for the removal of a post
@param access_token:
@param id_bee:
@param id_post: 
@status: tested 14/08/2014
'''
@services_app.route('/post/remove', methods=['POST'])
def restful_post_remove():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token'])
        if data['id_bee'] is None:
            raise Exception('You must provide the bee that is removing this post')
        
        if data['app'] is None:
            raise Exception('You must provide the app')
        elif data['app'] != APP_BACKEND:
            validate_token_owner(data['access_token'], data['id_bee'])
        
        post = get_post_by_id(data['id_post'])
        if data['id_bee'] != str(post.owner.id):
            raise Exception('Does not have permission to perform this action')
        else:
            remove_post(post)
            data = {}
            data['message'] = 'ok'
            return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: service RESTful that update a post
@param access_token
@param id_post:
@param id_bee:
@param title: 
@param text:
@param resources_to_remove:
@param resources_to_add:
@param with_resource: 
@return: ok or exception message
@status: 14/08/2014
'''
@services_app.route('/post/update', methods=['POST'])
def restful_post_update():
    data = {}
    try:
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)
        if data['id_bee'] is not None:
            bee = get_bee_by_id(data['id_bee'])
        else:
            raise Exception('You must provide the bee that is removing this post')
        #if('Comprobar operaciones del token')
        id_post = data['id_post']
        post = get_post_by_id(id_post)
        if bee.id != post.owner.id:
            raise Exception('Access denied!')
        else:
            update_post(post, data['title'], data['text'])
            #Validation for the resources removed or added:
            if data['with_resource'] == 'True':
                # If exists resources to remove:
                if len(data['resources_to_remove']) > 0:
                    for id_resource in data['resources_to_remove']:
                        resource = get_resource_by_id(id_resource)
                        remove_resource(post, resource)
                # If exists resources to add:
                if len(data['resources_to_add']) > 0:
                    for resource in data['resources_to_add']:
                        create_resource_in_post(post, bee, resource)
            data = {}
            data['message'] = 'ok'
            return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)


'''
@summary: service that receives data for the update of a post
@param access_token:
@param id_bee:
@param id_post: 
@param text:
@status: 
'''
@services_app.route('/post/update/social', methods=['POST'])
def restful_post_update_social():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token'])
        if data['id_bee'] is None:
            raise Exception('You must provide the bee that is removing this post')
        validate_token_owner(data['access_token'], data['id_bee'])
        
        post = get_post_by_id(data['id_post'])
        if data['id_bee'] != str(post.owner.id):
            raise Exception('Does not have permission to perform this action')
        if data['text'] is None:
            raise Exception('You must provide the text of post')    
        else:
            update_text_post (post,data['text'])
            data = {}
            data['message'] = 'ok'
            return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
    
''' 
@summary: service that return post by id
@param access_token:
@param id_post: 
@status: tested 02/09/2014
'''
@services_app.route('/post/find/by_id', methods=['GET'])
def restful_post_find_by_id():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'), 'id_post': request.args.get('id_post')}
        #Validating access token:
        access_token = data['access_token']
        validate_token(access_token)
        if data['id_post'] is not None:
            post = get_post_by_id(data['id_post'])
            return make_template_response(post, 'post/g_find_by_id.json')
        else:
            raise Exception('You must provide the id post')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: service that return publications by their bee owner
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of publications per page
@param id_bee:
@param app: Mobile, Backend or Landingpage
@status: tested 03/07/2014
'''
@services_app.route('/find/posts/by/bee', methods=['GET'])
def restful_post_find_by_bee():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'),
                'page_size': request.args.get('page_size'),
                'page_number': request.args.get('page_number'),
                'id_bee': request.args.get('id_bee'), 'app': request.args.get('app')}
        #Validating access token
        if data['app'] == APP_MOBILE:
            validate_token_mobile(data['access_token'])
        else:
            validate_token(data['access_token'])

        if data['id_bee'] is None:
            user = get_user_by_token(data['access_token'])
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
        bee = get_bee_by_id(id_bee)
        page_number = int(data['page_number'])
        page_size = int(data['page_size'])
        #Geting posts:
        post_result = get_posts(bee.id, page_number, page_size)
        return make_template_response(post_result, 'post/g_find_by_bee.json')

    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)