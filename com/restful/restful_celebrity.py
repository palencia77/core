'''
Created on 30/06/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.tools.tools_response import *
from com.services.services_bee import *
from com.services.services_celebrity import *
from com.services.services_security import *
from com.services.services_cause import *

'''
@summary: Service that registers a new celebrity
@param access_token:
@param name, description, email, telephone
@param web_site, address, facebook, twitter,
@param google_plus, with_resources, resources  
@return: message: ok or error
@return: id_celebrity: The celebrity created
@status: Tested 25/08/2014
'''
@services_app.route('/celebrity/register', methods=['POST'])
def restful_celebrity_register():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token'])  # validating token
        # Owner data:
        owner = get_user_by_token(data['access_token'])
        # General data validation:
        if (data['name'] is not None and data['description'] is not None and
            data['with_resource'] is not None and
            data['email'] is not None and
            data['telephone'] is not None and
            data['address'] is not None):
            # Call to method that save the celebrity:
            id_celebrity = register_celebrity(data['name'], data['description'], owner, data['email'],
                                              data['telephone'], data['web_site'], data['facebook'],
                                              data['twitter'], data['google_plus'], data['address'],
                                              data['resources'], data['with_resource'])          
        else:
            raise Exception('You must provide all data of the celebrity')
        data = {}
        data['message'] = 'ok'
        data['id_celebrity'] = id_celebrity
        return make_template_response(data, 'celebrity/b_register.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: Service that update a celebrity
@param access_token:
@param id_celebrity: 
@param name, description, email, telephone
@param web_site, address, facebook, twitter,
@param google_plus, with_resources, resources 
@return: message: ok or error
@status: Tested 14/07/2014
'''
@services_app.route('/celebrity/update', methods=['POST'])
def restful_update_celebrity():
    data = {}
    try:
        data = json.loads(request.data)
        #validating token:
        validate_token(data['access_token'])
        #validating id of the celebrity:
        if data['id_celebrity'] is not None:
            celebrity = get_celebrity_by_id(data['id_celebrity'])
        else:
            raise Exception('You must provide the id of the celebrity')
        #User data:
        user = get_user_by_token(data['access_token'])
        #validate_administrator_permissions(celebrity, user)
        # General data validation:
        if (data['name'] is not None and data['description'] is not None and
            data['with_resource'] is not None and
            data['email'] is not None and
            data['telephone'] is not None and
            data['address'] is not None):
            # Call to method that save the celebrity:
            update_celebrity(celebrity, data['name'], data['description'], user, 
                                                    data['email'], data['telephone'], data['web_site'], 
                                                    data['facebook'], data['twitter'], data['google_plus'], 
                                                    data['address'], data['resources'], data['with_resource'])          
        else:
            raise Exception('You must provide all data of the celebrity')
        data = {}
        data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
''' 
@summary: service that return all celebrities by a status and name
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of celebrities per page
@param status: 
@param name_filter: Empty or String 
@status: tested
'''
@services_app.route('/celebrity/find/all', methods=['GET'])
def restful_celebrity_by_status():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'), 'page_size':request.args.get('page_size'),
                'page_number':request.args.get('page_number'), 'status':request.args.get('status'),
                'name_filter':request.args.get('name_filter')}        
        # Validating access token
        access_token = data['access_token']
        validate_token(access_token)
        result = get_paginated_celebrities_by_status_and_name(data['status'], data['name_filter'], data['page_number'], data['page_size'])
        celebrity_result = result['content']
        celebrity_content = []
        for celebrity in celebrity_result:
            id_avatar = ""
            avatar_src = ''
            id_cover = ""
            id_promotional_photo = ""
            id_promotional_video = ""
            if 'avatar' in celebrity['parameters']:
                id_avatar = celebrity['parameters']['avatar']
                avatar_resource = get_resource_by_id(id_avatar)
                avatar_src = 'data:' + avatar_resource.content_type + ';base64,' + str(resize_image(avatar_resource.binary_content,30,35))
            if 'cover' in celebrity['parameters']:
                id_cover = celebrity['parameters']['cover']
            if 'promotional_photo' in celebrity['parameters']:
                id_promotional_photo = celebrity['parameters']['promotional_photo']
            if 'promotional_video' in celebrity['parameters']:
                id_promotional_video = celebrity['parameters']['promotional_video']
                            
            new_content = {'id_celebrity': celebrity['id'], 'name': celebrity['name'], 
                           'description': celebrity['description'], 'owner': celebrity['owner'], 
                           'email': celebrity['email'], 'telephone': celebrity['telephone'],
                           'web_site': celebrity['web_site'], 'facebook': celebrity['facebook'],
                           'twitter': celebrity['twitter'], 'google_plus': celebrity['google_plus'], 
                           'address': celebrity['address'], 'love_counter': celebrity['love_counter'],
                           'created_date': celebrity['created_date'], 'cover': id_cover, 'avatar': id_avatar, 
                           'promotional_photo': id_promotional_photo, 'promotional_video': id_promotional_video,
                           'status': celebrity['status'], 'avatar_src': avatar_src
                           }
            celebrity_content.append(new_content)
            result['content'] = celebrity_content
        return make_template_response(result, 'celebrity/b_find_by_status.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: Service that update status of a Celebrity
@param access_token:
@param id_celebrity
@param status
@return: message: ok or error
@status:
'''
@services_app.route('/celebrity/update/status', methods=['POST'])
def restful_celebrity_update_status():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        user = get_user_by_token(data['access_token'])
        #Celebrity data:
        if data['id_celebrity'] is not None:
            celebrity = get_celebrity_by_id(data['id_celebrity'])
        else:
            raise Exception('You must provide id of the bee to be removed')
        #Administration validation:
        #=======================================================================
        # if (isinstance(celebrity,Celebrity)):
        #     validate_administrator_permissions(celebrity,user)
        # else: #is instance of Cause:
        #     if celebrity.owner != user:
        #         raise Exception('You do not have permissions to perform this action')
        #=======================================================================
        
        if data['status'] is None:
                raise Exception('You must provide the status')
        else:                    
            celebrity_update_status(celebrity,data['status'])
            data = {} 
            data['message'] = 'ok'
            return make_ok_response(data)   
            
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

''' 
@summary: service that search paginated celebrities (optional: by name) associated or no with one cause
@param access_token: String
@param id_cause: String
@param associated: True or False
@param name_filter: Empty or String
@param page_number:
@param page_size:
@status: Tested (22/08/14)
'''
@services_app.route('/celebrity/cause_association/find', methods=['GET'])
def restful_celebrity_cause_association_find():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'), 'id_cause':request.args.get('id_cause'),
                'associated':request.args.get('associated'), 'name_filter':request.args.get('name_filter'),
                'page_number':request.args.get('page_number'), 'page_size':request.args.get('page_size')}        
        # Validating access token
        access_token = data['access_token']
        validate_token(access_token)
        if data['id_cause'] is not None:
            cause = get_cause_by_id(data['id_cause'])
        else:
            raise Exception('You must provide id of the cause')
        if data['associated'] == "True":
            result = get_celebrities_associated_to_cause(cause, data['name_filter'], data['page_number'], data['page_size'])
        else:
            result = get_celebrities_not_associated_to_cause(cause, data['name_filter'], data['page_number'], data['page_size'])
        celebrity_result = result['content']
        celebrity_content = []
        for celebrity in celebrity_result:
            avatar = ""
            avatar_src = ''
            if 'avatar' in celebrity['parameters']:
                avatar = celebrity['parameters']['avatar']
                avatar_resource = get_resource_by_id(avatar)
                avatar_src = 'data:' + avatar_resource.content_type + ';base64,' + str(resize_image(avatar_resource.binary_content,30,35))
            content = {'id_celebrity': celebrity['id'], 'name': celebrity['name'], 'telephone': celebrity['telephone'], 'avatar_src': avatar_src }
            celebrity_content.append(content)
        result['content'] = celebrity_content
        return make_template_response(result, 'celebrity/g_find_cause_association.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: service that return followed celebrities by a bee
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of celebrities per page
@param id_bee:
@status: tested 03/07/2014
'''
@services_app.route('/find/followed/celebrities/by/bee', methods=['GET'])
def restful_celebrity_find_by_bee():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'), 'page_size': request.args.get('page_size'),
                'page_number': request.args.get('page_number'), 'id_bee': request.args.get('id_bee')}
        #Validating access token
        access_token = data['access_token']
        validate_token(access_token)
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
            user = get_user_by_token(access_token)
            bee = get_bee_by_id(id_bee)
            page_number = int(data['page_number'])
            page_size = int(data['page_size'])
            #Geting bee_celebrities
            bee_celebrities_result = get_relationships_of_a_bee(bee, page_number, page_size, Celebrity)
            return make_template_response(bee_celebrities_result, 'celebrity/s_find_by_bee.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)