'''
Created on 08/07/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.tools.tools_response import *
from com.services.services_security import *
from com.services.services_partner import *
from com.services.services_bee import *
from com.services.services_cause import *

'''
@summary: Service that registers a new partner
@param access_token:
@param name, description, resources, geographic_location
@return: message: ok or error
@return: id_partner: The partner created
@status: Tested 08/07/2014
'''
@services_app.route('/partner/register', methods=['POST'])
def restful_partner_register():
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
            data['web_site'] is not None and
            data['address'] is not None):
            # Call to method that save the partner:
            id_partner = register_partner(data['name'], data['description'], owner,
                                        data['email'], data['telephone'], data['web_site'], data['address'], data['facebook'], data['twitter'], data['google_plus'], data['resources'], data['with_resource'])
        else:
            raise Exception('You must provide all data of the partner')
        data={}
        data['message'] = 'ok'
        data['id_partner'] = id_partner
        return make_template_response(data, 'partner/b_register.json')
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)

'''
@summary: Service that update a partner
@param access_token:
@param id_partner, name, description, geographic_location
@return: message: ok or error
@status: 
'''
@services_app.route('/partner/update', methods=['POST'])
def restful_partner_update():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token'])  # validating token
        user = get_user_by_token(data['access_token'])
        # Partner data:
        if data['id_partner'] is not None:
            partner = get_partner_by_id(data['id_partner'])
        else:
            raise Exception('You must provide id of the partner')
        # Administration validation:
        #validate_administrator_permissions(partner, user)
        # General data validation:
        if (data['name'] is not None and data['description'] is not None):
            # Call to method that update the partner:                        
            update_partner(partner, data['name'], data['description'], data['email'], data['telephone'], data['web_site'], data['address'], data['facebook'], data['twitter'], data['google_plus'], data['resources'], data['with_resource'])
        else:
            raise Exception('You must provide all data of the partner')
        data={}
        data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)   
    
''' 
@summary: service that return all partners by estatus and name
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of partners per page
@param status: 
@param name_filter: Empty or String 
@status: tested
'''
@services_app.route('/partner/find/all', methods=['GET'])
def restful_partner_by_status():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'), 'page_size':request.args.get('page_size'),
                'page_number':request.args.get('page_number'), 'status':request.args.get('status'),
                'name_filter':request.args.get('name_filter')}        
        # Validating access token
        access_token = data['access_token']
        validate_token(access_token)
        status = data['status']
        result = get_paginated_partners_by_status_and_name(status, data['name_filter'], data['page_number'], data['page_size'])
        partner_result = result['content']
        partner_content = []
        for partner in partner_result:
            avatar = ""
            avatar_src = ''
            cover = ""
            promotional_photo = ""
            promotional_video = ""
            if 'avatar' in partner['parameters']:
                avatar = partner['parameters']['avatar']
                avatar_resource = get_resource_by_id(avatar)
                avatar_src = 'data:' + avatar_resource.content_type + ';base64,' + str(resize_image(avatar_resource.binary_content,30,35))
            if 'cover' in partner['parameters']:
                cover = partner['parameters']['cover']
            if 'promotional_photo' in partner['parameters']:
                promotional_photo = partner['parameters']['promotional_photo']
            if 'promotional_video' in partner['parameters']:
                promotional_video = partner['parameters']['promotional_video']
                            
            new_content = {'id_partner': partner['id'], 'name': partner['name'], 'email': partner['email'],
                           'telephone': partner['telephone'], 'web_site': partner['web_site'], 'address': partner['address'],
                       'description': partner['description'], 'love_counter': partner['love_counter'],
                       'created_date': partner['created_date'], 'status': partner['status'], 'cover': cover,
                       'avatar': avatar, 'promotional_photo': promotional_photo,
                       'promotional_video': promotional_video, 'avatar_src': avatar_src, 'facebook':partner['facebook'], 'twitter':partner['twitter'], 'google_plus':partner['google_plus']
                       }
            partner_content.append(new_content)
            result['content'] = partner_content
        return make_template_response(result, 'partner/find_by_status.json')
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)  

'''
@summary: Service that update status of a Partner
@param access_token:
@param id_partner
@param status
@return: message: ok or error
@status:
'''
@services_app.route('/partner/update/status', methods=['POST'])
def restful_partner_update_status():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token'])  # validating token
        user = get_user_by_token(data['access_token'])
        # Partner data:
        if data['id_partner'] is not None:
            partner = get_partner_by_id(data['id_partner'])
        else:
            raise Exception('You must provide id of the bee to be removed')
        # Administration validation:
        #=======================================================================
        # if (isinstance(partner, Partner)):
        #     validate_administrator_permissions(partner, user)
        # else:  # is instance of Cause:
        #     if partner.owner != user:
        #         raise Exception('You do not have permissions to perform this action')
        #=======================================================================
        
        if data['status'] is None:
                raise Exception('You must provide the status')
        else:                    
            partner_update_status(partner, data['status'])
            data = {} 
            data['message'] = 'ok'
            return make_ok_response(data)   
            
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
    
''' 
@summary: service that searches paginated partners (optional: by name) associated or no with one cause
@param access_token: String
@param id_cause: String
@param associated: True or False
@param name_filter: Empty or String
@param page_number:
@param page_size:  
@status: Tested (29/08/14)
'''
@services_app.route('/partner/cause_association/find', methods=['GET'])
def restful_partners_by_cause():
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
            result = get_partners_associated_to_cause(cause,data['name_filter'],data['page_number'],data['page_size'])
        else:
            result = get_partners_not_associated_to_cause(cause,data['name_filter'],data['page_number'],data['page_size'])
        partner_result = result['content']
        partner_content = []
        for partner in partner_result:
            avatar = ""
            avatar_src = ''
            if 'avatar' in partner['parameters']:
                avatar = partner['parameters']['avatar']
                avatar_resource = get_resource_by_id(avatar)
                avatar_src = 'data:' + avatar_resource.content_type + ';base64,' + str(resize_image(avatar_resource.binary_content,30,35))
            content = {'id_partner': partner['id'], 'name': partner['name'], 'telephone': partner['telephone'], 'avatar_src': avatar_src }
            partner_content.append(content)
        result['content'] = partner_content
        return make_template_response(result, 'partner/g_find_cause_association.json')
    except Exception as e:
        data['error'] = e
        return make_error_response(data)        

'''
@summary: service that return followed partners by a bee
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of partners per page
@param id_bee:
@status: tested 03/07/2014
'''
@services_app.route('/find/followed/partners/by/bee', methods=['GET'])
def restful_partner_find_by_bee():
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
            #Geting bee_partners
            bee_partners_result = get_relationships_of_a_bee(bee, page_number, page_size, Partner)
            return make_template_response(bee_partners_result, 'partner/s_find_by_bee.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)