'''
Created on 08/07/2014

@author: palencia77
'''
from flask import request
from flask import json
from flask import abort
from com.restful.__init__ import services_app
from com.tools.tools_response import *
from com.services.services_security import *
from com.services.services_resource import *
from com.services.services_bee import *
from com.services.services_post import *
from com.services.services_award import *
from com.tools.app_types import *


'''
@summary: Method seeking resources having a particular bee
@param access_token:
@param page_number:
@param page_size:
@param id_bee: 
@param resource_width:
@param resource_height: 
@return: resources of a bee
'''
@services_app.route('/resource/find/by/bee', methods=['GET'])
def resful_resource_find_by_bee():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'), 'page_size': request.args.get('page_size'),
                'page_number': request.args.get('page_number'), 'id_bee': request.args.get('id_bee'),
                'resource_width': request.args.get('resource_width'), 'resource_height': request.args.get('resource_height')}
        access_token = data['access_token']
        validate_token(access_token)
        page_number = int(data['page_number'])
        page_size = int(data['page_size'])
        id_bee = data['id_bee']
        if id_bee is None:
            raise Exception('You must provide the bee that generates Post')
        bee = get_bee_by_id(id_bee)
        if bee is None:
            raise Exception('invalid bee')
        result = get_resources_by_bee(bee, page_number, page_size)
        resources_content = []
        for resource in result['content']:
            if data['resource_width'] is not None and data['resource_height'] is not None:
                binary_content = str(resize_image(resource.binary_content, int(data['resource_width']), int(data['resource_height'])))
            else:
                binary_content = str(resize_image(resource.binary_content, 576, 360))
            content = { 'id_resource': str(resource['id']), 'text': resource['text'], 'name': resource['name'],
                        'content_type': resource['content_type'], 'binary_content': binary_content,
                        'created_date': str(resource['created_date']), 'owner': resource['owner'],
                        'love_counter': resource['love_counter'], 'status': resource['status']
                       }
            resources_content.append(content)
        #We added binary_content encoded to the current resource}
        result['content'] = resources_content
        return make_template_response(result, 'resource/g_find_by_bee.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
        
'''
@summary: service that return a resource
@param access_token:
@param id_resource:
@param resource_width:
@param resource_height: 
@status: Tested 11/07/2014
'''
@services_app.route('/resource/find/by/id', methods=['GET'])
def restful_resource_find():
    data = {}
    try :
        data = {'access_token': request.args.get('access_token'), 'id_resource': request.args.get('id_resource'),
                'resource_width': request.args.get('resource_width'), 'resource_height': request.args.get('resource_height') }
        access_token = data['access_token']
        validate_token(access_token)
        id_resource = data['id_resource']
        if id_resource is None:
            raise Exception('You must provide the a resource')
        resource = get_resource_by_id(id_resource)
        if resource is not None:
            if data['resource_width'] is not None and data['resource_height'] is not None:
                binary_content = str(resize_image(resource.binary_content,int(data['resource_width']),int(data['resource_height'])))
            else:
                binary_content = str(base64.b64encode(resource.binary_content))
            resource_result = { 'id_resource': str(resource['id']), 'text': resource['text'], 'name': resource['name'],
                                'content_type': resource['content_type'], 'binary_content': binary_content,
                                'created_date': str(resource['created_date']), 'owner': resource['owner'],
                                'love_counter': resource['love_counter'], 'status': resource['status']
                              }
            return make_template_response(resource_result, 'resource/g_find_by_id.json')
        else:
            raise Exception('bee no have this resource')          
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)   


"""
@summary: Service that allows remove a post comment
@param access_token:
@param id_bee:
@param id_resource:
@return: json data
"""
@services_app.route('/resource/remove/by/bee', methods=['POST'])
def restful_resource_remove_by_bee():
    try:
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)
        
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
        bee = get_bee_by_id(id_bee)
        
        if data['id_resource'] is None:
            raise Exception('You must provide the id of the resource to which you remove')
        else:
            id_resource = data['id_resource']
            resource = get_resource_by_id(id_resource)
            #validating that the resource exist
            if resource is None:
                raise Exception('The comment you want to delete does not exist')
            #comentario en espanol: no se esta seguro  de si se debe validad que el unico que pueda
            #eliminar el resource sea el bee propietario del mismo (la razon de los dos comentarios siguientes).
            #elif (resource.owner != bee):
            #    raise Exception('You do not have permission to delete this resource')
            data = {}
            if remove_resource(bee, resource):
                data['message'] = 'ok'
                return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)    
            
'''
@summary: service that return a binary resource 
@param access_token:
@param id_resource:
@param resource_width:
@param resource_height:
@param app: Mobile, Landingpage or Backend 
@status: Tested 11/07/2014
'''
@services_app.route('/resource/view', methods=['GET'])
def restful_resource_view():
    data = {}
    try :
        data = {'access_token' : request.args.get('access_token'), 'id_resource': request.args.get('id_resource'),
                'app': request.args.get('app'), 'resource_width': request.args.get('resource_width'),
                'resource_height': request.args.get('resource_height')}
        #Validating access token
        if data['app'] == APP_MOBILE:
            validate_token_mobile(data['access_token'])
        else:
            validate_token(data['access_token'])
        id_resource = data['id_resource']
        if id_resource is None:
            raise Exception('You must provide the a resource')
        
        resource = get_resource_by_id(id_resource)
        if resource is not None:
            if data['resource_width'] is not None and data['resource_height'] is not None:
                response = make_response(resize_image_mobile(resource.binary_content,
                                                             int(data['resource_width']),
                                                             int(data['resource_height'])))
            else:
                response = make_response(resize_image_mobile(resource.binary_content, 267, 167))
            
            response.headers['Content-Type'] = resource['content_type']
            response.headers['Content-Disposition'] = '%s' % resource['name']
            return response            
        else:
            abort(500)         
    except Exception as e:
        abort(500)
        
'''
@summary: service that return a public binary resource 
@param id_resource:
@param resource_width:
@param resource_height:
@status: Tested 11/07/2014
'''
@services_app.route('/resource/public/view', methods=['GET'])
def restful_resource_public_view():
    data = {}
    try:
        data = {'id_resource': request.args.get('id_resource'),
                'resource_width': request.args.get('resource_width'),
                'resource_height': request.args.get('resource_height')}
        id_resource = data['id_resource']
        if id_resource is None:
            raise Exception('You must provide the a resource')
        resource = get_resource_by_id(id_resource)
        if resource is not None:
            if data['resource_width'] is not None and data['resource_height'] is not None:
                response = make_response(resize_image_mobile(resource.binary_content,
                                                             int(data['resource_width']),
                                                             int(data['resource_height'])))
            else:
                response = make_response(resource.binary_content)
            response.headers['Content-Type'] = resource['content_type']
            response.headers['Content-Disposition'] = '%s' % resource['name']
            return response            
        else:
            abort(500)         
    except Exception as e:
        abort(500)
        
'''
@summary: Method seeking resources having a particular post
@param access_token:
@param page_number:
@param page_size:
@param id_post:
@param resource_width:
@param resource_height:
@return: resources of a post
'''
@services_app.route('/resource/find/by/post', methods=['GET'])
def resful_get_resources_of_post():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'), 'page_size': request.args.get('page_size'),
                'page_number': request.args.get('page_number'), 'id_post': request.args.get('id_post'),
                'resource_width': request.args.get('resource_width'), 'resource_height': request.args.get('resource_height')}
        access_token = data['access_token']
        validate_token(access_token)
        page_number = int(data['page_number'])
        page_size = int(data['page_size'])
        if data['id_post'] is None:
            raise Exception('You must provide the id of the post to find resources')
        post = get_post_by_id(data['id_post'])
        result = get_resources_by_post(post, page_number, page_size)
        resources_content = []
        for resource in result['content']:
            if data['resource_width'] is not None and data['resource_height'] is not None:
                binary_content = str(resize_image(resource.binary_content,
                                                  int(data['resource_width']),
                                                  int(data['resource_height'])))
            else:
                binary_content = str(resize_image(resource.binary_content, 192, 120))
            content = { 'id_resource': str(resource['id']), 'text': resource['text'], 'name': resource['name'],
                        'content_type': resource['content_type'], 'binary_content': binary_content,
                        'created_date': str(resource['created_date']), 'owner': resource['owner'],
                        'love_counter': resource['love_counter'], 'status': resource['status']
                       }
            resources_content.append(content)
        #We added binary_content encoded to the current resource}
        result['content'] = resources_content
        return make_template_response(result, 'resource/g_find_by_post.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)    
    
'''
@summary: Method seeking resources having a particular post
@param access_token:
@param page_number:
@param page_size:
@param id_award:
@param resource_width:
@param resource_height:
@return: resources of a post
'''
@services_app.route('/resource/find/by/award', methods=['GET'])
def resful_get_resources_of_award():
    data = {}
    try:
        data = {'access_token': request.args.get('access_token'), 'page_size': request.args.get('page_size'),
                'page_number': request.args.get('page_number'), 'id_award': request.args.get('id_award'),
                'resource_width': request.args.get('resource_width'), 'resource_height': request.args.get('resource_height')}
        access_token = data['access_token']
        validate_token(access_token)
        page_number = int(data['page_number'])
        page_size = int(data['page_size'])
        if data['id_award'] is None:
            raise Exception('You must provide the id of the post to find resources')
        award = get_award_by_id(data['id_award'])
        result = get_resources_by_award(award, page_number, page_size)
        resources_content = []
        for resource in result['content']:
            if data['resource_width'] is not None and data['resource_height'] is not None:
                binary_content = str(resize_image(resource.binary_content,
                                                  int(data['resource_width']),
                                                  int(data['resource_height'])))
            else:
                binary_content = str(resize_image(resource.binary_content, 192, 120))
            content = { 'id_resource': str(resource['id']), 'text': resource['text'], 'name': resource['name'],
                        'content_type': resource['content_type'], 'binary_content': binary_content,
                        'created_date': str(resource['created_date']), 'owner': resource['owner'],
                        'love_counter': resource['love_counter'], 'status': resource['status']
                       }
            resources_content.append(content)
        #We added binary_content encoded to the current resource}
        result['content'] = resources_content
        return make_template_response(result, 'resource/g_find_by_award.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data) 
    
'''
@summary: service that return a resource by id of post (cut and / or resized)
@param access_token:
@param id_resource:
@status: Tested 11/07/2014
'''
@services_app.route('/resource/post/find/by/id', methods=['GET'])
def restful_post_resource_by_id():
    data = {}
    POST_MAX_WIDTH = 500
    POST_MAX_HEIGTH = 300
    try :
        data = {'access_token': request.args.get('access_token'), 'id_resource': request.args.get('id_resource'), 'post_max_width': request.args.get('post_max_width'), 'post_max_heigth':request.args.get('post_max_heigth')}
        access_token = data['access_token']
        validate_token(access_token)
        id_resource = data['id_resource']
        if id_resource is None:
            raise Exception('You must provide the a resource')
        resource = get_resource_by_id(id_resource)
        
        if data['post_max_width'] is not None:
            POST_MAX_WIDTH = data['post_max_width']
            
        if data['post_max_heigth'] is not None:
            POST_MAX_HEIGTH = data['post_max_heigth']           
        
        if resource is not None:
            binary_content = base64.b64encode(resource.binary_content)
            with Image(blob=base64.b64decode(binary_content)) as image:
                new_heigth = None
                if image.width > POST_MAX_WIDTH:             
                    proportion = float(image.width)/float(image.height)                          
                    new_heigth = POST_MAX_WIDTH/proportion               
                    binary_content = resize_image(base64.b64decode(binary_content),POST_MAX_WIDTH, int(round(new_heigth)))                 
                #===============================================================
                #     if new_heigth > POST_MAX_HEIGTH:
                #         print "new h es mas grande"
                #         y = float((new_heigth - POST_MAX_HEIGTH)/2)
                #         print round(y)
                #         binary_content = crop_image(base64.b64decode(binary_content), 0, int(round(y)), POST_MAX_WIDTH,POST_MAX_HEIGTH)                
                # elif image.height > POST_MAX_HEIGTH:
                #     y = float((new_heigth - POST_MAX_HEIGTH)/2)
                #     binary_content = crop_image(base64.b64decode(binary_content), 0, y, POST_MAX_WIDTH, image.width)
                #===============================================================
                              
                resource_result = { 'id_resource': str(resource['id']), 'text': resource['text'], 'name': resource['name'],
                                'content_type': resource['content_type'], 'binary_content': binary_content,
                                'created_date': str(resource['created_date']), 'owner': resource['owner'],
                                'love_counter': resource['love_counter'], 'status': resource['status']
                              }
            return make_template_response(resource_result, 'resource/g_find_by_id.json')
        else:
            raise Exception('bee no have this resource')          
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)     