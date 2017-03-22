'''
Created on 20/06/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.tools.tools_response import *
from com.services.services_bee import *
from com.services.services_security import *
from com.services.services_post import *
from com.services.services_comment import *
from com.services.services_celebrity import *
from time import mktime

'''
@summary: service that return data from a bee
@param access_token:
@param id_bee:
@status: Tested 04/07/2014
'''
@services_app.route('/bee/view', methods=['GET'])
def restful_bee_view():
    data = {}
    try:
        data = {'access_token' : request.args.get('access_token'), 'id_bee' : request.args.get('id_bee')}    
        access_token = data['access_token']
        validate_token(access_token)
        
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
        
        bee = get_bee_by_id_and_status(id_bee, STATUS_OBJECT_ACTIVE)

        result = {}
        result['bee'] = bee
        if isinstance(bee, Person):
            result['bee_type'] = 'Person'
            response = make_template_response(result, 'person/g_view.json')
        elif isinstance(bee, Cause):
            result['bee_type'] = 'Cause'
            response = make_template_response(result, 'cause/g_view.json')
        elif isinstance(bee, Partner):
            result['bee_type'] = 'Partner'
            response = make_template_response(result, 'partner/g_view.json')
        else:  # isinstance(bee, Celebrity):
            result['bee_type'] = 'Celebrity'
            response = make_template_response(result, 'celebrity/g_view.json')
        return response
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: service that return publications for the bee timeline
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of publications per page
@param id_bee: 
@status: tested 03/07/2014
'''
@services_app.route('/bee/timeline', methods=['GET'])
def restful_bee_timeline():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'),
                'page_size': request.args.get('page_size'),
                'page_number': request.args.get('page_number'),
                'id_bee': request.args.get('id_bee')}
        #Validating access token
        validate_token(data['access_token'])
        if data['id_bee'] is None or data['id_bee'] == "":
            raise Exception('You must provide the id of bee')
        else:
            id_bee = data['id_bee']
        validate_token_owner(data['access_token'], id_bee) 
        bee = get_bee_by_id(id_bee)        
        #Geting posts
        post_result = get_timeline(bee, int(data['page_number']), int(data['page_size'])) 
        return make_template_response(post_result, 'bee/g_timeline.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: this service update Bee profile
@param access_token:
@param id_bee:
@param gender:
@param full_name:
@param birthday: 
@param geographic_location:     
@return: message ok or error message 
@status: tested 03/07/2014
'''   
@services_app.route('/bee/update', methods=['POST'])
def restful_bee_update():
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
        if isinstance(bee, Person):
            user_update(user, data['gender'], data['full_name'], data['birthday'])
            bee_update_profile(bee, data['name'], data['geographic_location'])
        elif isinstance(bee, Celebrity):
            user_update(user, data['gender'], data['full_name'], data['birthday'])
            update_celebrity(bee, data['name'], data['description'], data['geographic_location'])
        data = {}
        data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
   
'''    
@summary: this service update avatar
@param access_token:
@param resource:
@param id_bee: 
@return: message ok or error message 
@status: tested 03/07/2014
'''
@services_app.route('/bee/avatar/update', methods=['POST'])
def restful_bee_avatar_update():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token'])            
        if data['id_bee'] is None:
            raise Exception('You must provide the id of bee')
            
        validate_token_owner(data['access_token'],  data['id_bee'])
        bee = get_bee_by_id( data['id_bee'])
        if data['resource'] is not None:          
            resource = create_resource_bee(bee, data['resource'], "avatar")
            binary_content = str(resize_image(resource.binary_content,int(150),int(150)))                
            resource_result = { 'id_resource': str(resource['id']), 'text': resource['text'], 'name': resource['name'],
                                'content_type': resource['content_type'], 'binary_content': binary_content,
                                'created_date': str(resource['created_date']), 'owner': resource['owner'],
                                'love_counter': resource['love_counter'], 'status': resource['status']
                              }
            return make_template_response(resource_result, 'resource/g_find_by_id.json')
        else:
            raise Exception('Unable to update the avatar')
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: service cover update 
@param access_token:
@param resource:
@param bee:
@param user:
@param id_bee: 
@return: message ok or error message 
@status: tested 03/07/2014
'''     
@services_app.route('/bee/cover/update', methods=['POST'])
def restful_bee_cover_update():
    data={}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token'])#validating token
        if data['id_bee'] is  None:
            raise Exception('You must provide the id of bee')
        bee = get_bee_by_id(data['id_bee'])
        
        if data['resource'] is not None:
            resource = create_resource_bee(bee, data['resource'], "cover")
            binary_content = str(resize_image(resource.binary_content,int(938),int(140)))                
            resource_result = { 'id_resource': str(resource['id']), 'text': resource['text'], 'name': resource['name'],
                                    'content_type': resource['content_type'], 'binary_content': binary_content,
                                    'created_date': str(resource['created_date']), 'owner': resource['owner'],
                                    'love_counter': resource['love_counter'], 'status': resource['status']
                                  }
            return make_template_response(resource_result, 'resource/g_find_by_id.json')
        else:
            raise Exception('Unable to update the Cover')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''    
@summary: this service update promotional_photo
@param access_token:
@param resource:
@param bee:
@param user:
@param id_bee: 
@return: message ok or error message 
@status: tested 03/07/2014
'''
@services_app.route('/bee/promotional_photo/update', methods=['POST'])
def restful_bee_promotional_photo_update():
    data={}
    try:
        data = json.loads(request.data)
        resource=data['resource']
        access_token=data['access_token']
        validate_token(access_token)#validating token
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
            user = get_user_by_token(access_token)
        bee = get_bee_by_id(id_bee)
        if resource is not None:
            if isinstance(bee, Cause) or isinstance(bee, Celebrity) or isinstance(bee, Partner):
                result_resource = create_resource_bee(bee, resource, "promotional_photo")
            data = {}
            data['message'] = 'ok'
            return make_ok_response(data)
        else:
            raise Exception('Unable to update the Promotional Photo')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: service promotional_video update 
@param access_token:
@param resource:
@param bee:
@param user:
@param id_bee: 
@return: message ok or error message 
@status: tested 03/07/2014
'''   
@services_app.route('/bee/promotional_video/update', methods=['POST'])
def restful_bee_promotional_video_update():
    data = {}
    try :
        data = json.loads(request.data)
        resource = data['resource']
        access_token = data['access_token']
        validate_token(access_token)#validating token
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
            user = get_user_by_token(access_token)
        bee = get_bee_by_id(id_bee)
        data = {}
        if resource is not None:
            if isinstance(bee, Cause) or isinstance(bee, Celebrity) or isinstance(bee, Partner):
                result_resource = create_resource_bee(bee, resource, "promotional_video")
            data = {}
            data['message'] = 'ok'
            return make_ok_response(data)
        else:
            raise Exception('Unable to update the Promotional Video')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: service document update 
@param access_token:
@param resource:
@param bee:
@param user:
@param id_bee: 
@return: message ok or error message 
@status: tested 03/07/2014
'''  
@services_app.route('/bee/document/update', methods=['POST'])
def restful_bee_document_update():
    data = {}
    try:
        data = json.loads(request.data)
        resource = data['resource']
        access_token = data['access_token']
        validate_token(access_token)#validating token
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
            user = get_user_by_token(access_token)
        bee = get_bee_by_id(id_bee)
        data = {}
        if resource is not None:
            if isinstance(bee, Cause):
                result_resource = create_resource_bee(bee, resource, "document")
            data = {}
            data['message'] = 'ok'
            return make_ok_response(data)
        else:
            raise Exception('Unable to update the Document')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)         
    
''' 
@summary: service that return friends of a bee Person
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of friends per page
@param id_bee: 
@status: tested 03/07/2014
'''
@services_app.route('/find/friends/by/bee', methods=['GET'])
def restful_bee_friends_find():
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
        #Geting bee_friends
        bee_friends_result = get_relationships_of_a_bee(bee, page_number, page_size, Person)
        bee_friends_content = []
        for bee_friend in bee_friends_result['content']:
            #We search friends counter for each friend
            friends_counter = get_count_relationships_of_a_bee(bee_friend, Person)
            content = {'id_person': str(bee_friend['id']), 'name': bee_friend['name'], 
                       'gender': bee_friend['owner'].gender, 'love_score': bee_friend['love_score'],
                       'post_counter': bee_friend['post_counter'], 'created_date': str(bee_friend['created_date']), 
                       'birthday': bee_friend['owner'].birthday,
                       'friends_counter': str(friends_counter),
                       'geographic_location': bee_friend['geographic_location']}
            bee_friends_content.append(content)
            #We added friends_counter to the current bee friends
        bee_friends_result['content'] = bee_friends_content
        return make_template_response(bee_friends_result, 'bee/s_find_friends.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: this service update the list of administrators in particular a bee
@param access_token:
@param id_bee:
@param id_administrator:
@param operation:
@return: message ok or error message 
@status: tested 03/07/2014
'''   
@services_app.route('/bee/administrators/update', methods=['POST'])
def restful_bee_administrators_update():
    data = {}
    try :
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)#validating token
        user = get_user_by_token(access_token)
        if data['id_bee'] is None:
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
            bee = get_bee_by_id(id_bee)
        if bee.owner == user:
            if isinstance(bee, Cause) or isinstance(bee, Celebrity) or isinstance(bee, Partner):
                update_administrators_of_a_bee(bee, data['id_administrator'], data['operation'])
                data = {}
                data['message'] = 'ok'
                return make_ok_response(data)
            else: 
                raise Exception('bee no is type Cause, Celebrity or Partner')
        else: 
            raise Exception('bee has no authority to perform this operation')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

'''
@summary: Service that remove logically a bee (Partner, Cause, Celebrity or Person)
@param access_token:
@param id_bee
@return: message: ok or error
@status: Tested 09/07/2014
'''
@services_app.route('/bee/remove', methods=['POST'])
def restful_bee_remove():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        user = get_user_by_token(data['access_token'])
        #Partner data:
        if data['id_bee'] is not None:
            bee = get_bee_by_id(data['id_bee'])
        else:
            raise Exception('You must provide id of the bee to be removed')
        #Administration validation:
        if isinstance(bee, Cause) or isinstance(bee, Partner) or isinstance(bee, Celebrity):
            validate_administrator_permissions(bee, user)
        else: #is instance of Person:
            if bee.owner != user:
                raise Exception('You do not have permissions to perform this action')
        remove_bee(bee)#Removing the bee
        data = {}
        data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data) 

'''
@summary: this service for update a attribute of Bee profile
@param id_bee:
@param attribute:
@param value of field:    
@return: message ok or error message 
@status: tested 25/11/2014
'''   
@services_app.route('/bee/update/attribute', methods=['POST'])
def restful_bee_update_attribute():
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
        
        if hasattr(bee, data['attribute']):
            type_attribute = str(type(getattr(bee, data['attribute'])))
            bee_attribute = True #si el atributo es propio de bee
        elif hasattr(bee.owner, data['attribute']):
            type_attribute = str(type(getattr(bee.owner, data['attribute'])))
            bee_attribute = False #si el atributo es propio de bee.owner (User) Ej: email
        if ((type_attribute == str(type(data['value']))) or 
            (type_attribute == "<type 'unicode'>" and str(type(data['value'])) == "<type 'str'>")):
            if(bee_attribute):
                bee_update_attribute(id_bee, data['attribute'], data['value'])
            else:
                user_update_attribute(bee.owner.id, data['attribute'], data['value'])
            data['message'] = 'ok'
            return make_ok_response(data)
        else: raise Exception('Type of attribute and type of value does not match')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)


'''
@summary: this service for historial ranking
@param id_bee
@param access_token:
@status: under construction
'''
@services_app.route('/bee/historical/ranking', methods=['GET'])
def restful_bee_historical_ranking():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'), 'id_bee': request.args.get('id_bee'),
                'page_number': request.args.get('page_number'), 'page_size': request.args.get('page_size')}
        access_token = data['access_token']
        validate_token(access_token)#validating token
        page_number = data['page_number']
        page_size = data['page_size']
        bee_ranking_result = bee_get_historical_ranking(page_number, page_size)
        return make_template_response(bee_ranking_result, 'bee/g_historical_ranking.json')
    except Exception as e:
        data['error'] = e
    return make_error_response(data)