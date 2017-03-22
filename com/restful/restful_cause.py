'''
Created on 30/06/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.tools.tools_response import *
from com.services.services_security import *
from com.services.services_cause import *
from com.services.services_bee import *
from com.services.services_security import *
from com.services.services_scope import *
from com.services.services_contact import *
from com.services.services_resource import *
from com.services.services_partner import *
from com.services.services_celebrity import *
from com.services.services_award import *
from com.tools.tools_general import *
from com.tools.app_types import *
import base64
import random

'''
@summary: Service that registers a new cause
@param access_token:
@param name, description, resources, risk_classification,
@param geographic_location, goal, id_subscope, start_date, 
@param closing_date, love_goal, ambassadors,
@param beneficiary, id_responsible, contacts,
@return: message: ok or error
@return: id_cause: The cause created
@status: Tested 11/07/2014
'''
@services_app.route('/cause/register', methods=['POST'])
def restful_cause_register():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        #Owner data:
        owner = get_user_by_token(data['access_token'])
        
        #Comented: 29/07/2014===================================================
        # if data['id_responsible'] is not None:
        #     responsible = get_person_by_id(data['id_responsible'])
        # else:
        #     raise Exception('You must provide the id of the responsible of the cause')
        # #Ambassador data validation:
        # for id_ambassador in data['ambassadors']:
        #     if not there_is_bee(id_ambassador):
        #         raise Exception('The bee ambassador: '+id_ambassador+ ' does not exist')
        #=======================================================================
        
        #Scope data validation:
        if data['id_subscope'] is not None:
            scope = get_scope_by_id(data['id_subscope'])
        else:
            raise Exception('Scope not found')
        #General data validation:
        if (data['name'] is not None and data['description'] is not None and data['goal'] is not None and
            data['contacts'] is not None and data['beneficiary'] is not None and
            data['with_resource'] is not None):
            geographic_location = None
            if 'geographic_location' in data:
                geographic_location = data['geographic_location']
            
            #Call to method that save the cause:
            id_cause = register_cause(data['name'],data['description'],data['resources'],geographic_location,data['goal'],scope,
                           None,data['closing_date'],data['love_goal'],
                           None,data['contacts'],data['beneficiary'],owner,None,
                           data['risk_classification'],data['url_promotional_video'],data['with_resource'])
        else:
            raise Exception('You must provide all data of the cause')
        data = {}
        data['message'] = 'ok'
        data['id_cause'] = id_cause
        return make_template_response(data,'cause/b_register.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

''' 
@summary: service that return causes of a bee
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of friends per page
@param id_bee: 
@status: building
'''
@services_app.route('/find/cause/by/bee', methods=['GET'])
def restful_causes_by_bee():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'),'page_size':request.args.get('page_size'), 
                'page_number':request.args.get('page_number'),'id_bee':request.args.get('id_bee')}        
       
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
          
            #We added friends_counter to the current bee friends
            bee_cause_result = get_relationships_of_a_bee(bee, page_number, page_size, Cause)
            return make_template_response(bee_cause_result, 'cause/g_find_by_bee.json')
    
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)    
    
''' 
@summary: Service of the search for causes not follow a bee and belong to the following scopes of this bee.
@param access_token:
@param id_bee: 
@status: building
'''
@services_app.route('/find/suggested/cause/by/scope/of/bee', methods=['GET'])
def restful_causes_by_scopes_of_a_bee_find():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'), 'id_bee':request.args.get('id_bee')}        
        #Validating access token
        access_token = data['access_token']
        validate_token(access_token)
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        elif(there_is_bee(data['id_bee'])==False):
            raise Exception('Bee not found')    
        else:
            id_bee = data['id_bee']
            bee = get_bee_by_id(id_bee)          
            bee_causes_result = get_causes_by_scopes_of_a_bee(bee)           
            return make_template_response(bee_causes_result, 'cause/s_find_suggested_by_scope_of_bee.json')
    
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data) 
    
'''
@summary: Service that update a cause
@param access_token, id_cause
@param name, description, risk_classification,
@param geographic_location, goal, id_subscope, start_date, 
@param closing_date, love_goal, ambassadors,
@param beneficiary, id_responsible, url_promotional_video
@return: message: ok or error
@status: Tested 09/07/2014
'''
@services_app.route('/cause/update', methods=['POST'])
def restful_cause_update():
    data = {}
    new_contacts = []
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token      
        user = get_user_by_token(data['access_token'])

        ###VALIDAR QUE EL USUARIO SEA ADMINISTRADOR#####
        #cause to update
        cause = get_cause_by_id(data['id_cause'])
#===============================================================================
# 
#         if data['id_responsible'] is not None:
#             responsible = get_person_by_id(data['id_responsible'])
#         else:
#             raise Exception('You must provide the id of the responsible of the cause')
#         #Ambassador data validation:
#         if data['ambassadors'] is not None:
#             for id_ambassador in data['ambassadors']:
#                 if not there_is_bee(id_ambassador):
#                     raise Exception('The bee ambassador: '+id_ambassador+ ' does not exist')
#===============================================================================
        #Scope data validation:
        if data['id_subscope'] is not None:
            scope = get_scope_by_id(data['id_subscope'])
        else:
            raise Exception('Scope not found')
        #General data validation:
        if (data['name'] is not None and data['description'] is not None and
            data['goal'] is not None and data['beneficiary'] is not None and
            data['contacts'] is not None and data['url_promotional_video'] is not None):
            
            geographic_location = None
            if 'geographic_location' in data:
                geographic_location = data['geographic_location']
            
            for contact in data['contacts']:
                if contact['id_contact'] is not None:
                    obj_contact = get_contact_by_id(contact['id_contact'])
                    update_contact(obj_contact,contact['name'],contact['email'],contact['mobile_phone'],contact['telephone'],contact['address'],contact['organization'])
                else:
                    new_contacts.append(contact)     
                    
            #Call to method that update the cause:
            update_cause(cause,data['name'],data['description'],data['resources'],
                         geographic_location,data['goal'],scope,
                         None,data['closing_date'],data['love_goal'],
                         None,data['beneficiary'],None,
                         data['risk_classification'],new_contacts,data['url_promotional_video'],data['with_resource'])
            
            if data['remove_contacts'] is not None:
                for contact in data['remove_contacts']:
                    contact_remove = get_contact_by_id(contact['id_contact'])
                    cause_remove_contact(cause,contact_remove)
        else:
            raise Exception('You must provide all data of the cause')
        
        data = {}
        data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data['error'] = e
        return make_error_response(data)

''' 
@summary: service that return causes of a scope or subscope
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of friends per page
@param id_scope: 
@status: building
'''
@services_app.route('/cause/scope/find', methods=['GET'])
def restful_causes_by_scope():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'),'page_size':request.args.get('page_size'), 
                'page_number':request.args.get('page_number'),'id_scope':request.args.get('id_scope')}        
       
        #Validating access token
        access_token = data['access_token']
        validate_token(access_token)
        #Get the scope
        if data['id_scope'] is not None:
            scope = get_scope_by_id(data['id_scope'])
        else:
            raise Exception('You must provide the id of the scope or subscope')
        
        if isinstance(scope,SubScope):
        #We must get the causes because is instance of SubScope:
            result = get_paginated_causes_by_subscope(scope,data['page_number'],data['page_size'])
        else:
        #We must get the subscopes and then the causes:
            result = get_paginated_causes_by_scope(scope,data['page_number'],data['page_size'])
            
        return make_template_response(result,'cause/g_find_by_scope.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
''' 
@summary: service that return causes by a status
@param access_token:
@param page_number: Number of the page to return
@param page_size: Number of causes per page
@param app: (MOBILE, BACKEND or LANDINPAGE)
@param name_filter:
@param status: 
@status: Tested (18/07/14)
'''
@services_app.route('/cause/status/find', methods=['GET'])
def restful_causes_by_status():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'),'page_size':request.args.get('page_size'), 
                'page_number':request.args.get('page_number'),'status':request.args.get('status'), 'app':request.args.get('app'), 'name_filter':request.args.get('name_filter')}        
        #Validating access token
        if data['app'] == APP_MOBILE:        
            validate_token_mobile(data['access_token'])
        else:
            validate_token(data['access_token'])
        
        status = data['status']
        result = get_paginated_causes_by_status(status,data['name_filter'],data['page_number'],data['page_size'])
        causes_result = result['content']
        cause_content = []
        for cause in causes_result:
            avatar = ""
            avatar_src = ''
            cover = ""
            promotional_photo = ""
            promotional_video = ""
            geographic_location = None
            document = ""
            if 'avatar' in cause['parameters']:
                avatar = cause['parameters']['avatar']
                avatar_resource = get_resource_by_id(avatar) 
                avatar_src ='data:'+avatar_resource.content_type+';base64,'+str(resize_image(avatar_resource.binary_content,30,35))
            if 'cover' in cause['parameters']:
                cover = cause['parameters']['cover']
            if 'promotional_photo' in cause['parameters']:
                promotional_photo = cause['parameters']['promotional_photo']
            if 'promotional_video' in cause['parameters']:
                promotional_video = cause['parameters']['promotional_video']
            if 'document' in cause['parameters']:
                document = cause['parameters']['document']
            if cause['geographic_location'] == {}:
                geographic_location = None
            else:
                geographic_location = cause['geographic_location']
            
                
            new_content = {'id_cause': cause['id'], 'name': cause['name'], 
                       'description': cause['description'] , 'goal': cause['goal'], 
                       'id_subscope': cause['sub_scope'].id, 'id_scope': cause['sub_scope'].parent.id,
                       'sub_scope_name': cause['sub_scope'].name, 'owner': cause['owner'],
                       'love_counter': cause['love_counter'], 'fly_counter': cause['fly_counter'],
                       'created_date': cause['created_date'], 'start_date': cause['start_date'],
                       'closing_date': cause['closing_date'], 'finish_date': cause['finish_date'],
                       'love_meter': cause['love_meter'], 'love_goal': cause['love_goal'],
                       'beneficiary': cause['beneficiary'], 'risk_classification': cause['risk_classification'],
                       'url_promotional_video': cause['url_promotional_video'], 'status': cause['status'],
                       'contacts': cause['contacts'], 'cover': cover,
                       'avatar': avatar, 'promotional_photo': promotional_photo,
                       'promotional_video': promotional_video,
                       'document': document, 'color': cause['sub_scope'].parent.color,
                       'avatar_src': avatar_src, 'partners': cause['partners'],'celebrities': cause['celebrities'], 'short_url':cause['short_url'], 'geographic_location':geographic_location
                       }
            cause_content.append(new_content)
        result['content'] = cause_content
        if data['app'] == APP_MOBILE:
            return make_template_response(result,'cause/m_status_find.json')
        else:
            return make_template_response(result,'cause/b_status_find.json')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)      
    
'''
@summary: Service that update status of a Cause
@param access_token:
@param id_cause
@param status
@return: message: ok or error
@status: Tested 08/08/2014
'''
@services_app.route('/cause/update/status', methods=['POST'])
def restful_cause_update_status():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        user = get_user_by_token(data['access_token'])
        #Cause data:
        if data['id_cause'] is not None:
            cause = get_bee_by_id(data['id_cause'])
        else:
            raise Exception('You must provide id of the bee to be removed')
        #=======================================================================
        # #Administration validation:
        # if (isinstance(cause,Cause)):
        #     validate_administrator_permissions(cause,user)
        # else: #is instance of Cause:
        #     if cause.owner != user:
        #         raise Exception('You do not have permissions to perform this action')
        #=======================================================================
        
        if data['status'] is None:
                raise Exception('You must provide the status')
        else:                    
            cause_update_status(cause,data['status'])
            data = {} 
            data['message'] = 'ok'
            return make_ok_response(data)   
            
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
''' 
@summary: service that update the partners associate to a cause
@param access_token:
@param id_cause: 
@param partners_to_add: id_partners List
@param partners_to_remove: id_partners List
@status: Tested 22/08/2014
'''
@services_app.route('/cause/update/partners', methods=['POST'])
def restful_cause_update_partenrs():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        user = get_user_by_token(data['access_token'])
        #Cause data:
        if data['id_cause'] is not None:
            cause = get_bee_by_id(data['id_cause'])
        else:
            raise Exception('You must provide id of the cause to be updated')
        #Administration permissions validation:
        #=======================================================================
        # if (isinstance(cause,Cause)):
        #     validate_administrator_permissions(cause,user)
        # else: #is instance of Cause:
        #     if cause.owner != user:
        #         raise Exception('You do not have permissions to perform this action')
        #=======================================================================
        # If exists partners to add:
        if len(data['partners_to_add']) > 0:
            for id_partner in data['partners_to_add']:
                partner = get_partner_by_id(id_partner)
                if partner not in cause.partners:
                    cause_create_partner_association(cause, partner)
        # If exists partners to remove:
        if len(data['partners_to_remove']) > 0:
            for id_partner in data['partners_to_remove']:
                cause_remove_partner_association(cause, id_partner)
        #The response:
        data = {} 
        data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
''' 
@summary: service that update the celebrities associate to a cause
@param access_token:
@param id_cause: 
@param celebrities_to_add: id_celebrities List
@param celebrities_to_remove: id_celebrities List
@status: Tested 27/08/2014
'''
@services_app.route('/cause/update/celebrities', methods=['POST'])
def restful_cause_update_celebrities():
    data = {}
    try:
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        user = get_user_by_token(data['access_token'])
        #Cause data:
        if data['id_cause'] is not None:
            cause = get_bee_by_id(data['id_cause'])
        else:
            raise Exception('You must provide id of the cause to be updated')
        #=======================================================================
        # #Administration permissions validation:
        # if (isinstance(cause,Cause)):
        #     validate_administrator_permissions(cause,user)
        # else: #is instance of Cause:
        #     if cause.owner != user:
        #         raise Exception('You do not have permissions to perform this action')
        #=======================================================================
        # If exists celebrities to add:
        if len(data['celebrities_to_add']) > 0:
            for id_celebrity in data['celebrities_to_add']:
                celebrity = get_celebrity_by_id(id_celebrity)
                if celebrity not in cause.celebrities:
                    cause_create_celebrity_association(cause, celebrity)
        # If exists celebrity to remove:
        if len(data['celebrities_to_remove']) > 0:
            for id_celebrity in data['celebrities_to_remove']:
                cause_remove_celebrity_association(cause, id_celebrity)
        #The response:
        data = {} 
        data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)

''' 
@summary: service that return causes for the landing page
@param access_token:
@param name_filter: 
@param app: ("MOBILE", "BACKEND", "LANDINGPAGE")
@param level_data:
@param page_number: Number of the page to return
@param page_size: Number of causes per page
@status: Tested (04/09/2014)
'''
@services_app.route('/cause/find/all', methods=['GET'])
def restful_cause_find_all():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'),'page_size':request.args.get('page_size'), 
                'page_number':request.args.get('page_number'), 'app':request.args.get('app'), 'name_filter':request.args.get('name_filter'), 'level_data':request.args.get('level_data')}        
        #Validating access token
        access_token = data['access_token']
        validate_token(access_token)
        result = get_paginated_causes_active_and_solved(data['name_filter'],data['page_number'],data['page_size'])
        
        if data['level_data'] == str(0):
            return make_template_response(result,'cause/l_find_all.json')
        if data['level_data'] == str(1):
            return make_template_response(result,'cause/s_find_all.json')
        else:
            raise Exception('This app have no permissions to perform this action');
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
''' 
@summary: service that return causes for the landing page
@param access_token:
@param name_filter: 
@param app: ("MOBILE", "BACKEND", "LANDINGPAGE")
@param page_number: Number of the page to return
@param page_size: Number of causes per page
@status: Tested (04/09/2014)
'''
@services_app.route('/cause/find/all/by/status', methods=['GET'])
def restful_cause_find_all_by_status():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'),'page_size':request.args.get('page_size'), 
                'page_number':request.args.get('page_number'),'status':request.args.get('status'), 'app':request.args.get('app'), 'name_filter':request.args.get('name_filter')}        
        #Validating access token
        validate_token(data['access_token'])
        result = get_paginated_causes_by_status(data['status'],data['name_filter'],data['page_number'],data['page_size'])
        
        if data['app'] == APP_SOCIAL:
            return make_template_response(result,'cause/s_find_all_by_status_0.json')
        else:
            raise Exception('This app have no permissions to perform this action');
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
    
    
''' 
@summary: service that return data of one cause for landing page
@param access_token:
@param id_cause: 
@param app:
@status: Tested (05/09/2014)
'''
@services_app.route('/cause/landingpage/find_by/id', methods=['GET'])
def restful_cause_landing_page_by_id():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'),'id_cause':request.args.get('id_cause'), 
                'app':request.args.get('app')}
        #Validating access token
        access_token = data['access_token']
        validate_token(access_token)
        if data['id_cause'] is None:
            raise Exception("You must provide the id of the cause")
        else:
            result = get_cause_by_id(data['id_cause'])
        if data['app'] == APP_LANDING:
            return make_template_response(result,'cause/l_find_by_id.json')
        else:
            raise Exception('This app have no permissions to perform this action');
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
''' 
@summary: service that return causes for the landing page
@param access_token:
@param name_filter: 
@param app: ("MOBILE", "BACKEND", "LANDINGPAGE")
@param page_number: Number of the page to return
@param page_size: Number of causes per page
@status: Tested (04/09/2014)
'''
@services_app.route('/cause/all/locations', methods=['GET'])
def restful_cause_find_all_locations():
    data = {}
    try:
        data = {'access_token':request.args.get('access_token'),'page_size':request.args.get('page_size'), 
                'page_number':request.args.get('page_number'), 'app':request.args.get('app'), 'name_filter':request.args.get('name_filter')}        
        #Validating access token
        access_token = data['access_token']
        validate_token(access_token)
        result = get_paginated_causes_active_and_solved(data['name_filter'],data['page_number'],data['page_size'])
        if data['app'] == "APP_LANDING":
            return make_template_response(result,'cause/l_find_all_locations.json')
        else:
            raise Exception('This app have no permissions to perform this action');
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)
    
''' 
@summary: service that update the awards associate to a cause
@param access_token:
@param id_cause: 
@param awards_to_add: id_awards List
@param awards_to_remove: id_awards List
@status: Tested 27/08/2014
'''
@services_app.route('/cause/update/awards', methods=['POST'])
def restful_cause_update_awards():
    data = {}
    try:
        count = 0
        data = json.loads(request.data)
        validate_token(data['access_token']) #validating token
        user = get_user_by_token(data['access_token'])
        #Cause data:
        if data['id_cause'] is not None:
            cause = get_bee_by_id(data['id_cause'])
        else:
            raise Exception('You must provide id of the cause to be updated')
        #=======================================================================
        # #Administration permissions validation:
        # if (isinstance(cause,Cause)):
        #     validate_administrator_permissions(cause,user)
        # else: #is instance of Cause:
        #     if cause.owner != user:
        #         raise Exception('You do not have permissions to perform this action')
        #=======================================================================
        # If exists celebrities to add:
        if len(data['awards_to_add']) > 0:
            for id_award in data['awards_to_add']:
                award = get_award_by_id(id_award)
                if award not in cause.awards:
                    association_true_result = cause_create_award_association(cause, award)
                    if association_true_result is False:
                        count = count + 1
        # If exists award to remove:
        if len(data['awards_to_remove']) > 0:
            for id_award in data['awards_to_remove']:
                cause_remove_award_association(cause, id_award)
        #The response:
        data = {}
        if count > 0:
            data['message'] = str(count)+" Awards not registered because they have no existence."
        else:
            data['message'] = 'ok'
        return make_ok_response(data)
    except Exception as e:
        data = {}
        data['error'] = e
        return make_error_response(data)