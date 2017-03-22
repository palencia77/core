'''
Created on 10/11/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.tools.tools_response import *
from com.services.services_security import *
from com.services.services_bee import *
from com.services.services_award import *
from com.tools.app_types import *
from com.services.services_cause import *

"""
@summary: This service allows you to save a Post
@param access_token
@param id_bee: Celebrity or Partner
@param title: 
@param text:
@param quantity: 
@param with_resource:
@param resources: List of resources on Json format
@return: id_award and message
"""
@services_app.route('/award/register', methods=['POST'])
def restful_award_register():
    data = {}
    try:
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token) #validating token
        if data['id_bee'] is not None:
            bee = get_bee_by_id(data['id_bee'])
        else:
            raise Exception('You must provide the id of bee that is creating the award')
        id_award = register_award(bee, data['title'], data['text'],data['quantity'],data['amount_love'],data['with_resource'], data['resources'])
        data = {}
        data['message'] = 'ok'
        data['id_award'] = id_award
        return make_template_response(data, 'award/b_register.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: service that receives data for the removal of a award
@param access_token:
@param id_bee:
@param id_award: 
@status: tested 14/08/2014
'''
@services_app.route('/award/update/status', methods=['POST'])
def restful_award_update_status():
    data = {}
    try:
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)
        
        #=======================================================================
        #id_bee = data['id_bee']
        #if id_bee is None:
        #    raise Exception('You must provide the bee that is removing this award')
        # if there_is_bee(id_bee):
        #     if id_bee != str(award.owner.id):
        #         raise Exception('Access denied!')
        #     else:
        #=======================================================================
        award = get_award_by_id(data['id_award'])
        award_update_status(award,data['status'])        
        data = {}
        data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: service RESTful that update a award
@param access_token
@param id_award:
@param id_bee:
@param title: 
@param text:
@param resources_to_remove:
@param resources_to_add:
@param with_resource: 
@return: ok or exception message
@status: 14/08/2014
'''
@services_app.route('/award/update', methods=['POST'])
def restful_award_update():
    data = {}
    try:
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)
        if data['id_bee'] is not None:
            bee = get_bee_by_id(data['id_bee'])
        else:
            raise Exception('You must provide the bee that is removing this award')
   
        award = get_award_by_id(data['id_award'])
        update_award(award, data['title'], data['text'],data['quantity'],data['amount_love'])
        #Validation for the resources removed or added:
        if data['with_resource'] == 'True':
            # If exists resources to remove:
            if len(data['resources_to_remove']) > 0:
                for id_resource in data['resources_to_remove']:
                    resource = get_resource_by_id(id_resource)
                    remove_resource(award, resource)
            # If exists resources to add:
            if len(data['resources_to_add']) > 0:
                for resource in data['resources_to_add']:
                    create_resource_in_award(award, bee, resource)
        data = {}
        data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
    
''' 
@summary: service that return award by id
@param access_token:
@param id_award: 
@status: tested 02/09/2014
'''
@services_app.route('/award/find/by_id', methods=['GET'])
def restful_award_find_by_id():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'), 'id_award': request.args.get('id_award')}
        #Validating access token:
        access_token = data['access_token']
        validate_token(access_token)
        if data['id_award'] is not None:
            award = get_award_by_id(data['id_award'])
            return make_template_response(award, 'award/g_find_by_id.json')
        else:
            raise Exception('You must provide the id award')
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
@services_app.route('/find/awards/by/bee', methods=['GET'])
def restful_award_find_by_bee():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'),
                'page_size': request.args.get('page_size'),
                'page_number': request.args.get('page_number'),
                'id_bee': request.args.get('id_bee'), 'app': request.args.get('app'), 'status': request.args.get('status')}
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
        page_number = int(data['page_number'])
        page_size = int(data['page_size'])
        #Geting awards:
        award_result = get_awards_by_bee(id_bee,data['status'], page_number, page_size)
        return make_template_response(award_result, 'award/g_find_by_bee.json')

    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

''' 
@summary: service that search paginated awards (optional: by name) associated or no with one cause
@param access_token: String
@param id_bee: String
@param associated: True or False
@param name_filter: Empty or String
@param app
@param page_number:
@param page_size:
@status: 
'''
@services_app.route('/award/bee_association/find', methods=['GET'])
def restful_award_cause_association_find():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'), 'id_bee':request.args.get('id_bee'),
                'associated':request.args.get('associated'),'app': request.args.get('app'), 'name_filter':request.args.get('name_filter'),
                'page_number':request.args.get('page_number'), 'page_size':request.args.get('page_size')}        
        # Validating access token
        access_token = data['access_token']
        validate_token(access_token)
        if data['id_bee'] is not None:
            bee = get_bee_by_id(data['id_bee'])
        else:
            raise Exception('You must provide id of the cause')
        if data['associated'] == "True":
            result = get_awards_associated_to_cause(bee, data['name_filter'], data['page_number'], data['page_size'])
        else:
            result = get_awards_not_associated_to_cause(bee, data['name_filter'], data['page_number'], data['page_size'])
         
        award_result = result['content']
        if data['app'] == "BACKEND":
            award_content = []        
            for award in award_result:
                avatar = ""
                avatar_src = ''
                if award['resource_refs'] != [] :
                    avatar = award['resource_refs'][0]
                    avatar_resource = get_resource_by_id(avatar)
                    avatar_src = 'data:' + avatar_resource.content_type + ';base64,' + str(resize_image(avatar_resource.binary_content,30,35))
                content = {'id_award': award['id'], 'title': award['title'], 'avatar_src': avatar_src }
                award_content.append(content)
            result['content'] = award_content
            return make_template_response(result, 'award/g_find_cause_association.json')
        else:
            return make_template_response(result, 'award/s_find_cause_association.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: service that return awards by status
@param access_token:
@param name_filter:
@param status:
@param app: ("MOBILE", "BACKEND", "LANDINGPAGE", "SOCIAL")
@param page_number: Number of the page to return
@param page_size: Number of awards per page
@status: Tested (18/11/2014)
'''
@services_app.route('/award/find/by/status', methods=['GET'])
def restful_award_find_by_status():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'), 'page_size': request.args.get('page_size'),
                'page_number': request.args.get('page_number'), 'status': request.args.get('status'),
                'app': request.args.get('app'), 'name_filter': request.args.get('name_filter')}
        #Validating access token
        validate_token(data['access_token'])
        result = get_paginated_awards_by_status(data['status'], data['name_filter'], data['page_number'],
                                                data['page_size'])

        if data['app'] == APP_SOCIAL:
            return make_template_response(result, 'award/g_find_by_status.json')
        else:
            raise Exception('This app have no permissions to perform this action')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: this service allows bee purchase a lot of love for a awards
@param id_bee:
@param id_award:   
@return: message ok or error message 
@status: tested 02/12/2014
''' 
@services_app.route('/award/purchase', methods=['POST'])
def restful_award_purchase():
    data={}
    try :
        data = json.loads(request.data)
        access_token=data['access_token']
        validate_token(access_token) #validating token
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
            user = get_user_by_token(access_token)
        bee = get_bee_by_id(id_bee)
        
        if data['id_award'] is None:
            raise Exception('The id of the award is invalid or null')
        else:
            id_award = data['id_award']
            award = get_award_by_id(id_award)
        
        if isinstance(bee, Person):
            if(award.quantity > 0):
                if(bee.love_coin >= award.amount_love):
                    award_purchase(bee,award)
                    data['message'] = 'ok'
                    return make_ok_response(data)
                else: raise Exception('Love coins insufficient for purchase')
            else: raise Exception('Insufficient quantity of this award')
        else: raise Exception('Invalid type of bee')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)    