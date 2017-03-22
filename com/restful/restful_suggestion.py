'''
Created on 01/07/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.tools.tools_response import *
from com.services.services_security import *
from com.services.services_bee import *
from com.services.services_suggestion import *

'''
@summary: Service that get causes suggested of a bee
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of publications per page
@param id_bee: 
@return: json data of causes
@status: Tested
'''
@services_app.route('/suggest/cause', methods=['GET'])
def restful_suggest_cause():
    data = {}
    try :
        data = {'access_token':request.args.get('access_token'),
                'page_size':request.args.get('page_size'), 
                'page_number':request.args.get('page_number'),
                'id_bee':request.args.get('id_bee')}
        access_token = data['access_token']
        validate_token(access_token)
        
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
            
        #We obtain the bee who wants the suggestions
        bee = get_bee_by_id(id_bee)
        if not isinstance(bee,Cause):
            result = get_suggested_causes(bee, data['page_number'], data['page_size'])
        else:
            raise Exception('A bee cause not have permission to perform this action')
        return make_template_response(result, 'suggestion/suggest_cause.json')
    
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: Service that get persons suggested of a bee
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of publications per page
@param id_bee:
@return: json data of bee's person
@status: Tested
'''
@services_app.route('/suggest/person', methods=['GET'])
def restful_suggest_person():
    data = {}
    try :
        data = {'access_token':request.args.get('access_token'),
                'page_size':request.args.get('page_size'), 
                'page_number':request.args.get('page_number'),
                'id_bee':request.args.get('id_bee')}
        access_token = data['access_token']
        validate_token(access_token)
        
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
            
        #We obtain the bee who wants the suggestions
        bee = get_bee_by_id(id_bee)
        if not isinstance(bee,Cause):
            result = get_suggested_persons(bee, data['page_number'], data['page_size'])
        else:
            raise Exception('A bee cause not have permission to perform this action')
        return make_template_response(result, 'suggestion/suggest_person.json')
    
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: Service that get celebrities suggested of a bee
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of publications per page
@param id_bee:
@return: json data of celebrities
@status: Tested
'''
@services_app.route('/suggest/celebrity', methods=['GET'])
def restful_suggest_celebrity():
    data = {}
    try :
        data = {'access_token':request.args.get('access_token'),
                'page_size':request.args.get('page_size'), 
                'page_number':request.args.get('page_number'),
                'id_bee':request.args.get('id_bee')}
        access_token = data['access_token']
        validate_token(access_token)
        
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
            
        #We obtain the bee who wants the suggestions
        bee = get_bee_by_id(id_bee)
        if not isinstance(bee,Cause):
            result = get_suggested_celebrities(bee, data['page_number'], data['page_size'])
        else:
            raise Exception('A bee cause not have permission to perform this action')
        return make_template_response(result, 'suggestion/suggest_celebrity.json')
    
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: Service that get partner suggested of a bee
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of publications per page
@param id_bee:
@return: json data of partner
@status: Tested
'''
@services_app.route('/suggest/partner', methods=['GET'])
def restful_suggest_partner():
    data = {}
    try :
        data = {'access_token':request.args.get('access_token'),
                'page_size':request.args.get('page_size'), 
                'page_number':request.args.get('page_number'),
                'id_bee':request.args.get('id_bee')}
        access_token = data['access_token']
        validate_token(access_token)
        
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
            
        #We obtain the bee who wants the suggestions
        bee = get_bee_by_id(id_bee)
        if not isinstance(bee,Cause):
            result = get_suggested_partner(bee, data['page_number'], data['page_size'])
        else:
            raise Exception('A bee cause not have permission to perform this action')
        return make_template_response(result, 'suggestion/suggest_partner.json')
    
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
