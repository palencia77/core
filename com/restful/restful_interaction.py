
from flask import request
from flask import json
from com.services.services_interaction import *
from com.services.services_bee import *
from com.tools.tools_response import *
from com.services.services_security import validate_token

'''
@summary: restful service that receives a request for create a interaction 
@param name:
@param codename: 
@return: ok
@status: tested 20/11/2014
'''
@services_app.route('/interaction/create', methods=['POST'])
def restful_interacion_create():
    data={}
    try :
        data = json.loads(request.data)
        validate_token(data['access_token'])
        interaction_type = get_interaction_type(data['codename'])
        result = create_interaction(data['name'],interaction_type)
        result = {}
        result['message']= 'ok'
        return make_ok_response(result)
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
  
'''
@summary: RESTful service that receives a request for get all interaction
@return: ok
@status: tested 26/06/2014
'''
@services_app.route('/interaction/find/all', methods=['GET'])
def restful_interacions_group_by_type():
    data = {}
    result = []
    try :
        data = {'access_token' : request.args.get('access_token')}    
        validate_token(data['access_token'])
        types_interactions = get_interactions_types_by_status(STATUS_OBJECT_ACTIVE)
        for type_interaction in types_interactions:
            interactions = get_interactions_by_status(type_interaction,STATUS_OBJECT_ACTIVE)
            content = { 'id':type_interaction.id, 'name':type_interaction.name, 
                       'interactions':interactions}
            result.append(content)
        return make_template_response(result, 'interaction/b_find_all.json')
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
    

'''
@summary: restful service that receives a request for update a interaction 
@param access_token:
@param id_interaction: 
@param value: 
@return: ok
@status: 
'''
@services_app.route('/interaction/update', methods=['POST'])
def restful_interacion_update():
    data={}
    try :
        data = json.loads(request.data)
        validate_token(data['access_token'])
        for interaction in data['interactions']:
            result = get_interaction_by_id(interaction['id_interaction'])
            update_interaction(result,int(interaction['value']))
        result = {}
        result['message']= 'ok'
        return make_ok_response(result)
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)


'''
@summary: restful service weekly ranking
@param :
@return: result
@status: tested
'''
@services_app.route('/interaction/weekly/ranking', methods=['GET'])
def restful_interation_weekly_ranking():
    data = {}
    result = {}
    try :
        data = {'access_token' : request.args.get('access_token')}
        access_token = data['access_token']
        validate_token(access_token)
        result = get_interaction_count_by_type()
        for i in range(0, len(result['content']['result'])):
            bee = get_bee_by_id(result['content']['result'][i]['_id']['bee_person'])
            result['content']['result'][i]['_id']['name'] = bee.name
            if len(bee.parameters) > 0:
                if bee.parameters['avatar'] is not None:
                    result['content']['result'][i]['_id']['id_avatar'] = bee.parameters['avatar']
            if bee.short_url is not None:
                result['content']['result'][i]['_id']['short_url'] = bee.short_url
        response = make_template_response(result, 'interaction/interaction_count_by_interaction_type.json')
        return response
    except Exception as e:
        data['error'] = e
        return make_error_response(data)
