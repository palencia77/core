'''
Created on 30/06/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.services.services_bee import *
from com.services.services_notification import *
from com.services.services_security import *
from com.tools.tools_response import *
from com.services.services_operation import *
  
'''
@summary: Method seeking comments having a particular post
@param access_token:
@param page_number:
@param page_size:
@param id_bee:
@param notification_status:
@param app:
@return: notifications of a bee
'''
@services_app.route('/notification/find/by/bee', methods=['GET'])
def restful_notification_find_by_bee():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'),
                'page_size': request.args.get('page_size'),
                'page_number': request.args.get('page_number'),
                'id_bee': request.args.get('id_bee'),
                'notification_status': request.args.get('notification_status'),
                'app': request.args.get('app')}
        validate_token(data['access_token'])
        if data['id_bee'] is None:
            raise Exception('You must provide the id of bee')
        else:
            bee = get_bee_by_id(data['id_bee'])
        validate_token_owner(data['access_token'], data['id_bee'])
        result = get_notifications_by_bee(bee, data['notification_status'], int(data['page_number']), int(data['page_size']))
        return make_template_response(result, 'notification/s_find_by_bee.json')
    except Exception as e:
        return {'error': e}
        
'''
@summary: restful service that allows read a notification
@param access_token:
@param id_bee: The bee that performs the operation
@param id_notification:
@param app:
@return: ok
@status: 
'''
@services_app.route('/notification/read', methods=['POST'])
def restful_notification_read():
    data = {}
    try:
        data = json.loads(request.data)
        if data['id_notification'] is None:
            raise Exception('You must provide id_notification')
        validate_token(data['access_token'])
        if data['id_bee'] is None:
            raise Exception('You must provide the id of bee')
        validate_token_owner(data['access_token'], data['id_bee'])
        notification = get_notification_by_id(data['id_notification'])
        update_status_notification(notification, STATUS_NOTIFICATION_READ)
        result = {}
        result['message'] = 'ok'
        return make_ok_response(result)
                            
    except Exception as e:
        return {'error': e}

'''
@summary: Method that count the notifications by status
@param access_token:
@param id_bee:
@param notification_status:
@param app:
@return: notification_counter
'''
@services_app.route('/notification/count/by/status', methods=['GET'])
def restful_notification_count_by_status():
    try:
        data = {'access_token': request.args.get('access_token'),
                'id_bee': request.args.get('id_bee'),
                'notification_status': request.args.get('notification_status'),
                'app': request.args.get('app')}
        validate_token(data['access_token'])
        if data['id_bee'] is None:
            raise Exception('You must provide the id of bee')
        else:
            bee_reader = get_bee_by_id(data['id_bee'])
        validate_token_owner(data['access_token'], data['id_bee'])
        result = count_notifications_by_status(bee_reader, data['notification_status'])
        return make_template_response(result, 'notification/s_count_by_status.json')
    except Exception as e:
        return {'error': e}