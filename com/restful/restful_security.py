'''
Created on 18/06/2014
  
@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.services.services_security import *
from com.services.services_resource import *
from com.services.services_bee import *
from com.tools.tools_general import *
from com.tools.tools_response import *
from com.tools.app_types import *
from com.tools.objects_status import *

'''
@summary: Service that validate an user
@param login: 
@param password: 
@param app: ("MOBILE", "BACKEND", "LANDINGPAGE")
@return: string access_token
'''
@services_app.route('/user/validate', methods=['POST'])
def restful_validate_user():
    data = {}
    try:
        data = json.loads(request.data)
        if 'app' in data:
            result = validate_credentials(data['login'], data['password'], data['app'])
        else:
            raise Exception('You must app')           
        return make_template_response(result, 'security/g_user_validate.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: service receiving a request to register a user and send a response
@param login:
@param password:
@param email: 
@param full_name
@param gender:
@param type:
@param app: 
@param avatar: 
@param phone: 
@return: access_token,login, email, full_name,type
@status: validated 
'''
@services_app.route('/user/register', methods=['POST'])
def restful_user_register():
    data = {}
    try:
        data = json.loads(request.data)
        validate_uniqueness_login(data['login'], data['app']) #Validates that the login is not registered
        if 'app' in data:
            if 'avatar' in data:                      
                result = register_user(data['login'], data['password'], data['email'],
                                       data['full_name'], data['gender'], data['birthday'],
                                       data['type'], data['app'], data['phone'], data['avatar'],
                                       False, None, None, None)
            else:
                result = register_user(data['login'], data['password'], data['email'],
                                       data['full_name'], data['gender'], data['birthday'],
                                       data['type'], data['app'], data['phone'], None,
                                       False, None, None, None)
            result['message'] = "ok"
            return make_template_response(result, 'security/g_user_register.json')
        else:
            raise Exception('You must app')  
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: service that return data from a user
@param access_token:
@param app: ("MOBILE", "BACKEND", "LANDINGPAGE")
'''
@services_app.route('/user/view', methods=['GET'])
def restful_user_view():
    data = {}
    data = {'access_token' : request.args.get('access_token'), 'app': request.args.get('app') }
    avatar_src = None
    #Validating access token
    if data['app'] == APP_MOBILE:       
        validate_token_mobile(data['access_token'])
    else:
        validate_token(data['access_token'])
    user = get_user_by_token(data['access_token'])
    if data['app'] == APP_BACKEND:
        if 'avatar' in user['parameters']:
            avatar_resource = get_resource_by_id(user['parameters']['avatar'])
            avatar_src = 'data:' + avatar_resource.content_type + ';base64,' + str(resize_image(avatar_resource.binary_content,18,20))
        user.avatar_src = avatar_src    
    return make_template_response(user, 'security/g_user_view.json')

'''
@summary: Service receives the request to change the password and sends the response
@param access_token:
@param id_user: 
@param old_password: 
@param new_password: 
@status: validate
'''
@services_app.route('/user/update/password', methods=['POST'])
def restful_change_password():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token'])
        if data['id_user'] is not None:
            user = get_user_by_id(data['id_user'])
        else:
            user = get_user_by_token(data['access_token'])
        
        user_update_password(user, data['old_password'], data['new_password'])
        data = {}
        data['message']= 'ok'
        return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: Service that validate an user from social network
@param id_social_network: 
@param full_name:
@param email:   
@param gender:
@param red_name:
@param app: ("MOBILE", "BACKEND", "LANDINGPAGE")
@return: string access_token
'''
@services_app.route('/user/social_network/validate', methods=['POST'])
def restful_validate_user_from_social_network():
        try:
            result = ""
            data = {}
            data = json.loads(request.data)
            if 'app' in data:
                if data['app'] is not None:
                    #validate_uniqueness_login(data['email'], data['app'])
                    result = validate_user_from_social_network(data['email'], data['app'], data['network_name'],data['id_social_network'],data['image_social_network'])
                    if result is None:
                        result = register_user(data['email'], None, data['email'], data['full_name'],
                                               data['gender'], None, USER_FRONTEND, data['app'], None, None,
                                               True, data['id_social_network'], data['network_name'],
                                               data['image_social_network'])
            return make_template_response(result, 'security/g_user_validate.json')
        except Exception as e:
            data = {}
            data['error'] = e
            return make_error_response(data)
        
        
'''
@summary: Method to find and show the users 
@param access_token:
@param status:
@param name_filter: 
@param page_number:
@param page_size: 
@param type:
@status: JSON data of subscopes
'''
@services_app.route('/user/find/all', methods=['GET'])
def resful_user_find_all():
    try :
        data = {'access_token': request.args.get('access_token'),
                'status': request.args.get('status'),
                'type': request.args.get('type'),
                'name_filter': request.args.get('name_filter'),
                'page_number': request.args.get('page_number'),
                'page_size': request.args.get('page_size')}
        
        access_token = data['access_token']
        validate_token(access_token)
        if data['status'] is not None:
            result = get_all_user_paginated(data['status'],data['name_filter'],data['type'],data['page_number'],data['page_size'])
            for user in result['content']:
                if 'avatar' in user['parameters']: 
                    avatar_resource = get_resource_by_id(user['parameters']['avatar']) 
                    avatar_src = 'data:' + avatar_resource.content_type + ';base64,' + str(resize_image(avatar_resource.binary_content,30,35))
                    user.avatar_src=avatar_src
        else:
            raise Exception('You must provide all data')
        return make_template_response(result, 'security/b_user_find_all.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data) 

'''
@summary: Method to find and show the subscopes by one scope
@param access_token:
@param status:
@param name_filter: 
@param page_number:
@param page_size: 
@status: JSON data of subscopes
'''
@services_app.route('/user/find/by/id', methods=['GET'])
def resful_user_find_by_id():
    try :
        data = {'access_token': request.args.get('access_token'),
                'id_user': request.args.get('id_user')}
        
        access_token = data['access_token']
        validate_token(access_token)
        if data['id_user'] is not None:
            user = get_user_by_id(data['id_user']) 
            if 'avatar' in user['parameters']:
                avatar_resource = get_resource_by_id(user['parameters']['avatar']) 
                avatar_src = 'data:' + avatar_resource.content_type + ';base64,' + str(resize_image(avatar_resource.binary_content,145,167))
                user.avatar_src=avatar_src                      
        else:
            raise Exception('You must provide all data')
        return make_template_response(user, 'security/b_user.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data) 
    
'''
@summary: service update data of user
@param email:
@param access_token:
@param id_user
@param full_name
@param gender:
@param birthday: 
@param phone:
@status: validated 
'''
@services_app.route('/user/update', methods=['POST'])
def restful_user_update():
    data = {}
    result = False
    try:
        data = json.loads(request.data)
        if 'id_user' in data:
            if data['id_user'] is not None:
                user = get_user_by_id(data['id_user'])  
            else:
                user = get_user_by_token(data['access_token']) 
            if 'avatar' in data:          
                result = update_user(user, data['email'], data['full_name'], data['gender'],
                                     data['birthday'], data['phone'], data['avatar'])
            else:
                result = update_user(user, data['email'], data['full_name'], data['gender'],
                                     data['birthday'], data['phone'], None)
            if result is True:
                data = {} 
                data['message'] = 'ok'
                return make_ok_response(data)
            else:
                raise Exception('An error occurred')
        else:
            raise Exception('You must id_user')  
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: Service that update status of a User
@param access_token:
@param id_user
@param status
@return: message: ok or error
@status: 
'''
@services_app.route('/user/update/status', methods=['POST'])
def restful_user_update_status():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        
        #Cause data:
        if data['id_user'] is not None:
            user = get_user_by_id(data['id_user'])
        else:
            user = get_user_by_token(data['access_token'])
        
        if data['status'] is None:
                raise Exception('You must provide the status')
        else:
            if data['status'] == STATUS_OBJECT_INACTIVE:
                send_confirmation_to_inactivate_account(user)
            else:    
                result = user_update_status(user,data['status'])
                if result == True:
                    data = {} 
                    data['message'] = 'ok'
                    return make_ok_response(data)
                else:
                    raise Exception('An error occurred')       
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: service send an email with password recovery information
@param login: 
@status: tested 09/09/2014
'''
@services_app.route('/user/recover/password', methods=['POST'])
def restful_recover_password():
    data = {}
    try:
        data = json.loads(request.data)
        user = get_user_by_login(data['login'])
        recover_password(user, data['app'])
        data = {}      
        data['message'] = "ok"
        return make_ok_response(data)         
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: service receiving a request to update password a user
@param access_token: type recover password
@param: password
@status: tested 09/09/2014
'''
@services_app.route('/user/recover/password/update', methods=['POST'])
def restful_recover_password_update_data():
    data = {}
    try:
        data = {}  
        data = json.loads(request.data)
        validate_token_recover_password(data['access_token'])
        user = get_user_by_token(data['access_token'])
        recover_password_update_data(user, data['password'], data['access_token'])
        data = {}      
        data['message'] = "ok"
        return make_ok_response(data)         
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: service that validate token type recover password
@param access_token:
@status: tested 09/09/2014
'''
@services_app.route('/user/recover/password/validate', methods=['GET'])
def restful_validate_token_recover_password():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token')}
        validate_token_recover_password(data['access_token'])
        data = {}      
        data['message'] = "ok"
        return make_ok_response(data)         
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: service that activate the bee account
@param access_token:
@status: tested 09/09/2014
'''
@services_app.route('/user/activate/account', methods=['POST'])
def restful_user_activate_account():
    data = {}
    try:
        data = {}
        data = json.loads(request.data)
        if data['access_token'] is None:
            raise Exception('Access denied')
        else:
            validate_token_activate_account(data['access_token'])
            user = get_user_by_token(data['access_token'])
            bee = get_bee_by_owner(user)
            if user_update_status(user, STATUS_OBJECT_ACTIVE) is True and \
               bee_update_status(bee, STATUS_OBJECT_ACTIVE) is True:
                token_update_status(data['access_token'], STATUS_TOKEN_USED)
                data = {}
                data['message'] = "ok"
                return make_ok_response(data)
            else:
                raise Exception('A problem has occurred handling the user attributes')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: service that activate the bee account
@param access_token:
@status: tested 08/12/2014
'''
@services_app.route('/user/inactivate/account', methods=['POST'])
def restful_user_inactivate_account():
    data = {}
    try:
        data = {}
        data = json.loads(request.data)
        if data['access_token'] is None:
            raise Exception('Access denied')
        else:
            validate_token_inactivate_account(data['access_token'])
            user = get_user_by_token(data['access_token'])
            bee = get_bee_by_owner(user)
            if user_update_status(user, STATUS_OBJECT_INACTIVE) is True and \
               bee_update_status(bee, STATUS_OBJECT_INACTIVE) is True:
                token_update_status(data['access_token'], STATUS_TOKEN_USED)
                data = {}
                data['message'] = "ok"
                return make_ok_response(data)
            else:
                raise Exception('A problem has occurred handling the user attributes')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)    
    
'''
@summary: service inactive user session
@param access_token:
@status: tested 06/11/2014
'''
@services_app.route('/user/logout', methods=['POST'])
def restful_logout():
    data = {}
    try:
        data = {}  
        data = json.loads(request.data)
        validate_token(data['access_token'])
        token_update_status(data['access_token'],'INVALID')
        data = {}      
        data['message'] = "ok"
        return make_ok_response(data)         
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)       