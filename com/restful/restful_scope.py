'''
Created on 30/06/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.tools.tools_response import *
from com.services.services_security import *
from com.services.services_scope import *
import base64

'''
@summary: Service that registers a new scope
@param access_token:
@param name, description, activation_date, closing_date, resource(optional)
@param with_resource: Bool true or false
@return: message:
@return: id_scope: The scope created
@status: Tested
'''
@services_app.route('/scope/register', methods=['POST'])
def restful_scope_register():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        if data['name'] is not None and data['description']:
            id_scope = register_scope(data['name'],data['description'],
                                      data['activation_date'],data['closing_date'], data['resource'], 
                                      data['with_resource'], data['color'])
        else:
            raise Exception('You must provide the name and description of the scope')
        data = {}
        data['message'] = 'ok'
        data['id_scope'] = id_scope
        return make_template_response(data,'scope/b_register.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: Service that registers a new subscope
@param access_token:
@param name, description, activation_date, closing_date, id_scope, resource(optional)
@param with_resource: Bool true or false
@return: message:
@return: id_subscope: The SubScope created
@status: Tested
'''
@services_app.route('/subscope/register', methods=['POST'])
def restful_subscope_register():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        if (data['name'] is not None and data['description']):
            if data['id_scope'] is not None:
                scope_parent = get_scope_by_id(data['id_scope'])
                id_scope = register_subscope(data['name'],data['description'],
                                             data['activation_date'],data['closing_date'], data['resource'], 
                                             scope_parent, data['with_resource'])
            else:
                raise Exception('You must provide the id of scope parent to subscope')
        else:
            raise Exception('You must provide the name and description of the scope')
        data = {}
        data['message'] = 'ok'
        data['id_scope'] = id_scope
        return make_template_response(data,'scope/b_register.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
     
'''
@summary: Method to find and show a particular scope or subscope
@param access_token:
@param id_scope: id of scope or subscope
@status: JSON data of scope/subscope
'''
@services_app.route('/scope/find', methods=['GET'])
def resful_scope_find_id():
    data={}
    try :
        data = {'access_token':request.args.get('access_token'),
                'id_scope':request.args.get('id_scope')}
        access_token = data['access_token']
        validate_token(access_token)
        id_scope = data['id_scope']
        if id_scope is None:
            raise Exception('You must provide an identifier Scope')
        result = get_scope_by_id(id_scope)
        return make_template_response(result, 'scope/view.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: Method to find and show a particular scope or subscope
@param access_token:
@param id_scope: id of scope or subscope
@param name_filter:
@param status:
@status: JSON data of scope with or without subscopes
'''
@services_app.route('/scope/all', methods=['GET'])
def resful_scopes_find_all():
    data={}
    try :
        data = {'access_token':request.args.get('access_token'),
                'status':request.args.get('status'),
                'name_filter':request.args.get('name_filter'),
                'page_number':request.args.get('page_number'),
                'page_size':request.args.get('page_size'),
                }
        validate_token(data['access_token'])
        scope_result = get_scopes(data['name_filter'],data['status'],data['page_number'], data['page_size'])
        scope_content = []
        for scope in scope_result['content']:
            logo = ""
            if scope.logo is not None:
                logo = {'id_logo' : scope.logo.id,
                        'name' : scope.logo.name,
                        'text' : scope.logo.text,
                        'binary_content' : str(resize_image(scope.logo.binary_content,30,35)),
                        'content_type' : scope.logo.content_type
                        }
            content = { 'id': scope.id, 
                        'name': scope.name,
                        'description': scope.description,
                        'creation_date': scope.creation_date,
                        'activation_date': scope.activation_date,
                        'closing_date': scope.closing_date,
                        'status': scope.status,
                        'color': scope.color,
                        'logo' : logo
                        }
            scope_content.append(content)
            #We added sub_scopes to the current scope
            scope_result['content'] = scope_content
        return make_template_response(scope_result, 'scope/find_all.json')            
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)     
    
'''
@summary: Method to find and show the subscopes by one scope
@param access_token:
@param id_scope: id of scope
@status: JSON data of subscopes
'''
@services_app.route('/scope/sub_scopes/find', methods=['GET'])
def resful_sub_scopes_by_scope_find():
    try :
        data = {'access_token':request.args.get('access_token'),
                'id_scope':request.args.get('id_scope'),
                'name_filter':request.args.get('name_filter'),
                'status':request.args.get('status'),
                'page_number':request.args.get('page_number'),
                'page_size':request.args.get('page_size')
                }       
        validate_token(data['access_token']) 
        if data['id_scope'] is None:
            raise Exception('You must provide an identifier Scope')
        scope = get_scope_by_id(data['id_scope'])
        #result = {}
        result = get_sub_scopes_by_scope(scope,data['name_filter'],data['status'],data['page_number'], data['page_size'])
        subscope_content = []
        for subscope in result['content']:
            logo = None
            #result['content']
            if subscope.logo is not None:
                logo = {'id_logo' : subscope.logo.id,
                        'name' : subscope.logo.name,
                        'text' : subscope.logo.text,
                        'binary_content' : str(resize_image(subscope.logo.binary_content,30,35)),
                        'content_type' : subscope.logo.content_type
                        }
            else:
                logo = {'id_logo': None,
                        'name': None,
                        'text': None,
                        'binary_content': None,
                        'content_type': None
                        }

            content = {'id': subscope.id,
                       'name': subscope.name,
                       'description': subscope.description,
                       'parent': subscope.parent.id,
                       'creation_date': subscope.creation_date,
                       'activation_date': subscope.activation_date,
                       'closing_date': subscope.closing_date,
                       'status': subscope.status,
                       'logo': logo
                       }
            subscope_content.append(content)
            #We added sub_scopes to the current scope
        result['content'] = subscope_content  
        return make_template_response(result, 'scope/b_find_subscopes_by_scope.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data) 

"""
@summary: Service that allows remove a subscope
@param access_token:
@param id_subscope:
@return: ok or error message
@status: building
"""
@services_app.route('/subscope/remove', methods=['POST'])
def restful_subscope_remove():
    try :
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)
        #Geting the user:
        user = get_user_by_token(access_token)
        
        if data['id_subscope'] is None:
            raise Exception('You must provide the id of the sub-scope to which you remove')
        #We remove the sub-scope:
        removed = remove_subscope_by_id(data['id_subscope'])
        if removed  == True:
            data = {}
            data['message'] = 'ok'
            return make_ok_response(data)
        else: 
            raise Exception
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)  
    
"""
@summary: Service that allows remove a scope
@param access_token:
@param id_scope:
@return: ok or error message
@status: building
"""
@services_app.route('/scope/remove', methods=['POST'])
def restful_scope_remove():
    try :
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)
        
        if data['id_scope'] is None:
            raise Exception('You must provide the id of the scope to which you remove')
        #We remove the scope:
        removed = remove_scope_by_id(data['id_scope'])
        if removed == True:
            data = {}
            data['message'] = 'ok'
            return make_ok_response(data)
        else: 
            raise Exception        
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: Service that update a scope
@param access_token, id_scope
@param name, description, activation_date, closing_date, resource(optional)
@param with_resource: Bool true or false
@return: message:
@return: ok or error message 
@status: Tested
'''
@services_app.route('/scope/update', methods=['POST'])
def restful_scope_update():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        if data['id_scope'] is None:
            raise Exception('You must provide the id of the scope which you want to update')
        #Scope to be updated:
        scope = get_scope_by_id(data['id_scope'])
        #General data validation
        if (data['name'] is not None and data['description']):
            id_scope = update_scope(scope,data['name'],data['description'],
                                      data['activation_date'],data['closing_date'], data['resource'], 
                                      data['with_resource'], data['color'])
        else:
            raise Exception('You must provide the name and description of the scope')
        data = {}
        data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: Service that update a subscope
@param access_token, id_scope, id_subscope
@param name, description, activation_date, closing_date, resource(optional)
@param with_resource: Bool true or false
@return: message:
@return: ok or error message 
@status: Tested
'''
@services_app.route('/subscope/update', methods=['POST'])
def restful_subscope_update():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        if data['id_subscope'] is None:
            raise Exception('You must provide the id of the scope which you want to update')
        #Scope to be updated:
        subscope = get_scope_by_id(data['id_subscope'])
        #General data validation
        if data['name'] is not None and data['description'] is not None and data['id_scope'] is not None:
            scope = get_scope_by_id(data['id_scope'])
            update_subscope(subscope,scope,data['name'],data['description'],
                                      data['activation_date'],data['closing_date'], data['resource'], 
                                      data['with_resource'])
        else:
            raise Exception('You must provide the name and description of the scope')
        data = {}
        data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: Service that update status of a Scope
@param access_token:
@param id_scope
@param status
@return: message: ok or error
@status:
'''
@services_app.route('/scope/update/status', methods=['POST'])
def restful_scope_update_status():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        #Scope data:
        if data['id_scope'] is not None:
            scope = get_scope_by_id(data['id_scope'])
        else:
            raise Exception('You must provide id of the scope to be removed')
               
        if data['status'] is None:
                raise Exception('You must provide the status')
        else:                    
            scope_update_status(scope,data['status'])
            data = {} 
            data['message'] = 'ok'
            return make_ok_response(data)               
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)


'''
@summary: Service that update status of a SubScope
@param access_token:
@param id_subscope
@param status
@return: message: ok or error
@status:
'''
@services_app.route('/subscope/update/status', methods=['POST'])
def restful_subscope_update_status():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token'])  # validating token
        # Scope data:
        if data['id_subscope'] is not None:
            subscope = get_subscope_by_id(data['id_subscope'])
        else:
            raise Exception('You must provide id of the SubScope to be removed')

        if data['status'] is None:
            raise Exception('You must provide the status')
        else:
            subscope_update_status(subscope, data['status'])
            data = {}
            data['message'] = 'ok'
            return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)