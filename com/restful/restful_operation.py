'''
Created on 26/06/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.services.services_post import *
from com.services.services_operation import *
from com.services.services_security import *
from com.services.services_request_friendship import *
from com.services.services_notification import *
from com.services.services_cause import *
from com.services.services_bee import *
from com.services.services_award import *
from com.services.services_interaction import *
from com.tools.tools_response import *
from com.tools.app_types import *

'''
@summary: restfult service that receives a request for action love about a cause or post
@param access_token:
@param id_bee: the bee performs longline action
@param id_post_destination, id_bee_destination, id_comment_destination: the bee, post or comment
       on which the action takes love
@param app: MOBILE, SOCIAL or LANDINGPAGE
@return: ok
@status: tested 26/06/2014
'''
@services_app.route('/operation/love/action', methods=['POST'])
def restful_operation_love_action():
    data={}
    try:
        data = json.loads(request.data)
        #Validating access token
        if data['app'] == APP_MOBILE:      
            validate_token_mobile(data['access_token'])
        else:
            validate_token(data['access_token'])
        if data['id_bee'] is None:
            raise Exception('You must provide the id of the bee')
        validate_token_owner(data['access_token'], data['id_bee'])
        bee = get_bee_by_id(data['id_bee'])
        
        #looking for the type of operation and type of notification object
        operation_type = get_operation_type('OTLA') 
        notification_type = get_notification_type('NTLA')
        result = {}
        result['message'] = 'ok'
        result['target_love_meter'] = None
        #Determining upon whom the action is executed
        if data['id_post_destination'] is not None:
            post_destination = get_post_by_id(data['id_post_destination'])
            #validates if the user already performed this operation:
            # TO DO: CONSIDERAR REALIZAR ESTA VALIDACION BUSCANDO EN EL LOVE_REFS DEL OBJETO:
            if there_is_operation_on_post(bee, post_destination, operation_type) is False:
                create_operation_post(bee, post_destination, operation_type)
                description = bee.name + ' ha dado Love tu publicacion'

                #Increasing the attributes of the post:
                post_love_counter_increase(post_destination)
                post_save_executor_love_action(post_destination, bee.id)
                # We validate this not performing an action on itself:
                if post_destination.owner.id != bee.id:
                    create_notification_destination_post(bee, post_destination.owner, post_destination, description, notification_type)
                    #Calculate the love_coin and love_score to be increased:
                    if isinstance(post_destination.owner, Cause):
                        interaction = get_interaction_by_name_and_type("LOVE", "ITPOCA")
                        # Increasing the cause love_meter:
                        cause = cause_receive_love(post_destination.owner, interaction.value)
                        # Save the cause love meter to the response:
                        result['target_love_meter'] = cause.love_meter
                    elif isinstance(post_destination.owner, Celebrity):
                        interaction = get_interaction_by_name_and_type("LOVE", "ITPOCE")
                    elif isinstance(post_destination.owner, Partner):
                        interaction = get_interaction_by_name_and_type("LOVE", "ITPOPA")
                    else:  # isinstance(post_destination.owner, Person):
                        interaction = get_interaction_by_name_and_type("LOVE", "ITPOBEE")
                        # Increasing the bee destination love_score and love_coin:
                        bee_increment_love_score(post_destination.owner, interaction.value)
                        bee_increment_love_coin(post_destination.owner, interaction.value)
                    # Apply the increment to the bee:
                    bee = bee_increment_love_score(bee, interaction.value)
                    bee = bee_increment_love_coin(bee, interaction.value)
                    #creating interaction log to the Post
                    create_interaction_log_post(bee, interaction, interaction.value, post_destination)
                # Make the response template:
                result['bee_love_coin'] = bee.love_coin
                result['bee_love_score'] = bee.love_score
                return make_template_response(result, 'operation/s_love_action.json')
            else:
                raise Exception('This user has already performed this operation')

        elif data['id_bee_destination'] is not None:
            bee_destination = get_cause_by_id(data['id_bee_destination'])
            if there_is_operation_on_bee(bee, bee_destination, operation_type) is False:
                create_operation_bee(bee, bee_destination, operation_type)
                description = bee.name + ' ha dado Love a tu causa'
                create_notification_destination_bee(bee, bee_destination, description, notification_type)
                #Increasing the attributes of the bee cause:
                bee_love_counter_increase(bee_destination)
                bee_save_executor_love_action(bee_destination, bee.id)
                #Calculate the love_coin and love_score to be increased:
                interaction = get_interaction_by_name_and_type("LOVE", "ITCA")
                # Increasing the cause love_meter:
                cause = cause_receive_love(bee_destination, interaction.value)
                #creating interaction log for Bee
                create_interaction_log_bee(bee, interaction, interaction.value, bee_destination)
                # Save the cause love meter to the response:
                result['target_love_meter'] = cause.love_meter
                # Apply the increment to the bee:
                bee = bee_increment_love_score(bee, interaction.value)
                bee = bee_increment_love_coin(bee, interaction.value)
                # Make the response template:
                result['bee_love_coin'] = bee.love_coin
                result['bee_love_score'] = bee.love_score
                return make_template_response(result, 'operation/s_love_action.json')
            else:
                raise Exception('This user has already performed this operation')

        elif data['id_comment_destination'] is not None:
            comment_destination = get_postcomment_by_id(data['id_comment_destination'])
            if get_operation_comment_by_attributes(bee, comment_destination, operation_type) is False:
                create_operation_comment(bee, comment_destination, operation_type)
                description = bee.name + ' a dado Love a tu comentario'

                #Increasing the attributes of the comment:
                comment_love_counter_increase(comment_destination)
                comment_save_executor_love_action(comment_destination, bee.id)
                # We validate this not performing an action on itself:
                if comment_destination.owner.id != bee.id:
                    create_notification_destination_comment(bee, comment_destination.owner, comment_destination, description, notification_type)
                    #Calculate the love_coin and love_score to be increased:
                    if isinstance(comment_destination.parent.owner, Cause):
                        interaction = get_interaction_by_name_and_type("LOVE", "ITPOCA")
                        # Increasing the cause love_meter:
                        cause = cause_receive_love(comment_destination.parent.owner, interaction.value)
                        # Save the cause love meter to the response:
                        result['target_love_meter'] = cause.love_meter
                    elif isinstance(comment_destination.parent.owner, Celebrity):
                        interaction = get_interaction_by_name_and_type("LOVE", "ITPOCE")
                    elif isinstance(comment_destination.parent.owner, Partner):
                        interaction = get_interaction_by_name_and_type("LOVE", "ITPOPA")
                    else:  # isinstance(post_destination.parent.owner, Person):
                        interaction = get_interaction_by_name_and_type("LOVE", "ITPOBEE")
                        # Increasing the bee destination love_score and love_coin:
                        bee_increment_love_score(comment_destination.owner, interaction.value)
                        bee_increment_love_coin(comment_destination.owner, interaction.value)
                    #creating interaction log for Bee
                    create_interaction_log_comment(bee, interaction, interaction.value, comment_destination)
                    # Apply the increment to the bee:
                    bee = bee_increment_love_score(bee, interaction.value)
                    bee = bee_increment_love_coin(bee, interaction.value)
                # Make the response template:
                result['bee_love_coin'] = bee.love_coin
                result['bee_love_score'] = bee.love_score
                return make_template_response(result, 'operation/s_love_action.json')
            else:
                raise Exception('This user has already performed this operation')

        else:
            raise Exception('You must to provide the id of object destination')
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: restfult service that receives a request for follow
@param access_token:
@param id_bee: The bee that performs the operation
@param id_bee_destination: The bee that will send the request
@return: ok
@status: tested 30/06/2014
'''
@services_app.route('/operation/follow', methods=['POST'])
def restful_operation_follow():
    data={}
    try:
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)
        
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
        
        owner = get_bee_by_id(id_bee)
        
        #looking for the type of operation and type of notification object
        operation_type = get_operation_type('OTFO')
        notification_type = get_notification_type('NTFS')          
        result = {}
        result['message']= 'ok'
        
        
        if data['id_bee_destination'] is None:
            raise Exception('You must provide the bee_destination')
        else:
            bee_destination = get_bee_by_id(data['id_bee_destination'])
            
            if isinstance(bee_destination, Person) and isinstance(owner, Person):
                request_friendship = get_request_friendship_by_attributes(owner, bee_destination, 'pending')
                if not request_friendship: 
                    create_operation_bee(owner, bee_destination, operation_type)
                    create_request_friendship(owner, bee_destination)
                    description = owner.name + ' Te ha enviado una solicitud de amistad'
                    create_notification_destination_bee(owner, bee_destination, description, notification_type)
                    return make_ok_response(result)
                else:
                    raise Exception('You have sent a friend request')                                                             
            
            elif isinstance(bee_destination, Partner) or isinstance(bee_destination, Celebrity) or isinstance(bee_destination, Cause):
                description = owner.name + ' Te sigue ahora'
                create_operation_bee(owner, bee_destination, operation_type) 
                create_notification_destination_bee(owner, bee_destination, description, notification_type)
                bee_follow(owner, bee_destination)
                return make_ok_response(result)
            else:
                raise Exception('Not have permission to perform this action')                                       
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: restful service that allows love donates to a cause
@param access_token:
@param id_bee: The bee that performs the operation
@param id_bee_destination: the bee that is directed operation (cause)
@return: ok
@status: tested 01/07/2014
'''
@services_app.route('/operation/love/give', methods=['POST'])
def restful_operation_love_give():
    data={}
    try :
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)
        
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
        
        #look the bee object
        owner = get_bee_by_id(id_bee)
        
        if data['quantity_love'] is None:
            raise Exception('Must specify the amount of love you wish to donate')
        else:
            quantity_love = data['quantity_love']                        
        
        #looking for the type of operation
        operation_type = get_operation_type('OTGL')
        notification_type = get_notification_type('NTGL')            
        result = {}
        result['message']= 'ok'
                
        if data['id_bee_destination'] is None:
            raise Exception('You must provide the bee to which you love action takes wing')
        else:
            bee_destination = get_cause_by_id(data['id_bee_destination'])
            if isinstance(owner, Person):
                if quantity_love > owner.love_score:
                    raise Exception('The amount of love is to donate more than your love score')
                else:
                    cause_receive_love(bee_destination, quantity_love)
                    bee_decrement_love_score(owner,quantity_love)
                    description = owner.name + ' Ha donado' + str(quantity_love) + 'love'
                    create_operation_bee(owner, bee_destination, operation_type)
                    create_notification_destination_bee(owner, bee_destination, description, notification_type)                                            
                    return make_ok_response(result)
            else:
                raise Exception('Must provide a valid bee_destination')             
                                  
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
       
'''
@summary: restful service that allows accept or decline a friend request
@param access_token:
@param id_bee: The bee that performs the operation
@param id_bee_destination: the bee that is directed operation (person)
@param operation_type: codename example: 'OTAF'
@return: ok
@status: tested 02/07/2014
'''
@services_app.route('/operation/friend_request/response', methods=['POST'])
def restful_operation_respond_friend_request():
    data={}
    try :
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)
        
        if data['id_bee'] is None:
            user = get_user_by_token(access_token)
            id_bee = user.parameters['id_bee']
        else:
            id_bee = data['id_bee']
        
        #look the bee object
        owner = get_bee_by_id(id_bee)
        
        #looking for the type of operation
        if data['operation_type'] is None:
            raise Exception('Must provide a type of operation')
        else:
            codename = data['operation_type']        
            operation_type = get_operation_type(codename)
                                 
        result = {}
        result['message']= 'ok'
        
        if data['id_request_friendship'] is None:
            raise Exception('You must provide id_request_friendship')
        else:            
            request_friendship = get_request_friendship_by_id(data['id_request_friendship'])
            bee_destination = request_friendship.owner
            
            if codename == 'OTAF':                
                notification_type = get_notification_type('NTAF')               
                update_status_request_friendship(request_friendship, 'approve')
                create_operation_bee(owner, bee_destination, operation_type)
                description = owner.name + ' Ha aceptado tu solicitud de amistad'
                create_notification_destination_bee(owner, bee_destination, description, notification_type)                    
                bee_approve_friendship(owner, bee_destination)                                                              
                return make_ok_response(result)
            elif codename == 'OTRF':
                update_status_request_friendship(request_friendship, 'reject')
                create_operation_bee(owner, bee_destination, operation_type)
                return make_ok_response(result)
            else:
                raise Exception('Type of operation not valid')
                
        raise Exception('Must provide a valid bee_destination')             
           
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: Service restful allows you to lock a bee (add it to the blacklist)
@param access_token:
@param id_bee: The bee that performs the operation (Cause, Partner, Celebrity or Person) *Required
@param id_bee_destination: the bee that is directed operation
@return: message ok
@status: tested 03/07/2014
'''   
@services_app.route('/operation/block/bee', methods=['POST'])
def restful_operation_block_bee():
    data={}
    try :
        data = json.loads(request.data)
        access_token=data['access_token']
        validate_token(access_token)#validating token
        if 'id_bee' in data:
            if data['id_bee'] is None:
                id_bee = data['id_bee']
                owner = get_bee_by_id(id_bee)
            else:
                raise Exception('You must provide the id of bee')
        else: 
            Exception('You must provide the id of bee')
       
        #looking for the type of operation
        operation_type = get_operation_type('OTBB')
        if data['id_bee_destination'] is None:
            raise Exception('You must provide the id_bee_destination')
        else:
            bee_destination = get_bee_by_id(data['id_bee_destination'])
            response = there_is_bee_blocked(owner,data['id_bee_destination'])
            if not response:
                bee_block_relationships(owner, data['id_bee_destination'])
                create_operation_bee(owner, bee_destination, operation_type)
                data = {}
                data['message'] = 'ok'
                return make_template_response(data,'ok.json') 
            else:
                raise Exception('The bee has been blocked')
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
 
'''
@summary: restful service that receives a FLY action
@param access_token:
@param id_bee: The bee that performs the operation (Cause, Partner, Celebrity or Person) *Required
@param id_post_destination, id_bee_destination, id_award_destination: the bee, post or award
       on which the action takes Fly
@param app: MOBILE, SOCIAL or LANDINGPAGE
@return: ok
@status: tested 04/07/2014
'''
@services_app.route('/operation/fly/action', methods=['POST'])
def restful_operation_fly_action():
    data = {}
    try:
        data = json.loads(request.data)
        #Validating access token
        if data['app'] == APP_MOBILE:
            validate_token_mobile(data['access_token'])
        else:
            validate_token(data['access_token'])
        if data['id_bee'] is None:
            raise Exception('You must provide the id of the bee')
        validate_token_owner(data['access_token'], data['id_bee'])
        bee = get_bee_by_id(data['id_bee'])

        #Looking for the type of operation and type of notification object
        operation_type = get_operation_type('OTFLY') 
        notification_type = get_notification_type('NTFLY')            
        result = {}
        result['message'] = 'ok'
        result['target_love_meter'] = None
        #Determining upon whom the action is executed
        if data['id_post_destination'] is not None:
            post_destination = get_post_by_id(data['id_post_destination'])
            create_operation_post(bee, post_destination, operation_type)
            description = bee.name + ' hizo Fly a tu publicacion'
            #Increasing the attributes of the post:
            post_fly_counter_increase(post_destination)  # increase fly counter
            post_add_fly_refs(post_destination, bee.id)  # post adds to the refs that we perform the bee fly
            # We validate this not performing an action on itself:
            if post_destination.owner.id != bee.id:
                create_notification_destination_post(bee, post_destination.owner, post_destination, description, notification_type)
                #Calculate the love_coin and love_score to be increased:
                if isinstance(post_destination.owner, Cause):
                    interaction = get_interaction_by_name_and_type("FLY", "ITPOCA")
                    create_interaction_log_post(bee, interaction, interaction.value, post_destination)
                    # Increasing the cause love_meter:
                    cause = cause_receive_love(post_destination.owner, interaction.value)
                    # Save the cause love meter to the response:
                    result['target_love_meter'] = cause.love_meter
                elif isinstance(post_destination.owner, Celebrity):
                    interaction = get_interaction_by_name_and_type("FLY", "ITPOCE")
                    # TO DO: INCREMENT POINT OF CELEBRITY
                elif isinstance(post_destination.owner, Partner):
                    interaction = get_interaction_by_name_and_type("FLY", "ITPOPA")
                    # TO DO: INCREMENT POINT OF PARTNER
                else:  # isinstance(post_destination.owner, Person):
                    interaction = get_interaction_by_name_and_type("FLY", "ITPOBEE")
                    # Increasing the bee destination love_score and love_coin:
                    bee_increment_love_score(post_destination.owner, interaction.value)
                    bee_increment_love_coin(post_destination.owner, interaction.value)

                # We create the interaction log:
                create_interaction_log_post(bee, interaction, interaction.value, post_destination)
                # Apply the increment to the bee:
                bee = bee_increment_love_score(bee, interaction.value)
                bee = bee_increment_love_coin(bee, interaction.value)
            # Make the response template:
            result['bee_love_coin'] = bee.love_coin
            result['bee_love_score'] = bee.love_score
            return make_template_response(result, 'operation/s_fly_action.json')

        elif data['id_bee_destination'] is not None:
            bee_destination = get_cause_by_id(data['id_bee_destination'])
            create_operation_bee(bee, bee_destination, operation_type)
            description = bee.name + ' hizo Fly a tu Causa'
            create_notification_destination_bee(bee, bee_destination, description, notification_type)
            # Increasing the attributes of the bee cause:
            cause_fly_counter_increase(bee_destination)  # increase fly counter
            bee_save_executor_fly_action(bee_destination, bee.id)
            # Calculate the love_coin and love_score to be increased:
            interaction = get_interaction_by_name_and_type("FLY", "ITCA")
            #creating interaction log for Bee
            create_interaction_log_bee(bee, interaction, interaction.value, bee_destination)
            # Increasing the cause love_meter:
            cause = cause_receive_love(bee_destination, interaction.value)
            # Save the cause love meter to the response:
            result['target_love_meter'] = cause.love_meter
            # Apply the increment to the bee:
            bee = bee_increment_love_score(bee, interaction.value)
            bee = bee_increment_love_coin(bee, interaction.value)
            # Make the response template:
            result['bee_love_coin'] = bee.love_coin
            result['bee_love_score'] = bee.love_score
            return make_template_response(result, 'operation/s_fly_action.json')

        elif data['id_award_destination'] is not None:
            award_destination = get_award_by_id(data['id_award_destination'])
            create_operation_award(bee, award_destination, operation_type)
            #Increasing the attributes of the bee:
            award_fly_counter_increase(award_destination)  # increase fly counter
            award_save_executor_fly_action(award_destination, bee.id)
            #Calculate the love_coin and love_score to be increased:
            interaction = get_interaction_by_name_and_type("FLY", "ITAW")
            #creating interaction log for award
            create_interaction_log_award(bee, interaction, interaction.value, award_destination)
            # Apply the increment to the bee:
            bee = bee_increment_love_score(bee, interaction.value)
            bee = bee_increment_love_coin(bee, interaction.value)
            # Make the response template:
            result['bee_love_coin'] = bee.love_coin
            result['bee_love_score'] = bee.love_score
            return make_template_response(result, 'operation/s_fly_action.json')

        else:
            raise Exception('You must to provide the id of object destination')
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)  

'''
@summary: restful service that counts the number of operations performed by each point at a time interval 
        by type of operation
@param access_token:
@param bee_destination:
@param operation_type:
@param start_date:
@param end_date:
@param time_unit:
@return: response
@status: tested 10/08/2014
'''
@services_app.route('/operation/count_operation_type', methods=['GET'])
def restful_operation_count_by_operation_type():
    data = {}
    try :
        data = {'access_token' : request.args.get('access_token'), 'bee_destination' : request.args.get('bee_destination')
                , 'operation_type' : request.args.get('operation_type') 
                , 'time_unit' : request.args.get('time_unit')}    
        access_token = data['access_token']
        validate_token(access_token)
        if data['bee_destination'] is None:
            raise Exception('You must provide the id_bee_destination to tell their operations')
        else:
            bee_destination = get_cause_by_id(data['bee_destination'])
            if bee_destination is None:
                raise Exception('invalid bee destination')
            else:
                result = get_operation_count_by_operation_type(bee_destination, data['operation_type'], data['time_unit']);
                response = make_template_response(result, 'operation_count_by_operation_type.json')
                return response
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)

'''
@summary: restfult service that counts the number of operations love and fly performed by each 
        point at a time interval by type of operation and by bee_destination (cause object) or 
        post_destination (post object)
@param access_token:
@param bee_destination or post_destination:
@param operation_type_one:
@param operation_type_two:
@param time_unit:
@return: response
@status: tested 13/08/2014
'''
@services_app.route('/operation/count/by/cause_or_post', methods=['GET'])
def restful_operation_count_by_bee_or_post():
    data = {}
    try :
        data = {'access_token' : request.args.get('access_token'), 'bee_destination' : request.args.get('bee_destination') 
                , 'post_destination' : request.args.get('post_destination')
                , 'operation_type_one' : request.args.get('operation_type_one')
                , 'operation_type_two' : request.args.get('operation_type_two')
                , 'time_unit' : request.args.get('time_unit')}    
        access_token = data['access_token']
        validate_token(access_token)
        if data['bee_destination'] is None and data['post_destination'] is None:
            raise Exception('You must provide the id_bee_destination to tell their operations')
        elif data['bee_destination'] is not None:
            bee_destination = get_cause_by_id(data['bee_destination'])
            result = {}
            result["operation_type_one"] = get_operation_count_by_operation_type(bee_destination, data['operation_type_one'], data['time_unit']);
            result["operation_type_two"] = get_operation_count_by_operation_type(bee_destination, data['operation_type_two'], data['time_unit']);
            response = make_template_response(result, 'operation/count_operations_by_bee_or_post.json')
            return response
        else:
            post_destination = get_post_by_id(data['post_destination'])
            result = {}
            result["operation_type_one"] = get_count_operation_type_by_post(post_destination, data['operation_type_one'], data['time_unit']);
            result["operation_type_two"] = get_count_operation_type_by_post(post_destination, data['operation_type_two'], data['time_unit']);                    
            response = make_template_response(result, 'operation/count_operations_by_bee_or_post.json')
            return response            
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)


'''
@summary: restful that counts the number of operations in the cause and its posts for every point in a
         time interval for operation type(two types)
@param access_token:
@param id_cause:
@param operation_type_one:
@param operation_type_two:
@param time_unit:
@return: response
@status: tested 18/08/2014
'''
@services_app.route('/operation/count/two_operations/by/cause', methods=['GET'])
def restful_operation_count_two_operations_by_cause():    
    data = {}
    try :
        data = {'access_token' : request.args.get('access_token'), 'id_cause' : request.args.get('id_cause') 
                , 'operation_type_one' : request.args.get('operation_type_one')
                , 'operation_type_two' : request.args.get('operation_type_two')
                , 'time_unit' : request.args.get('time_unit')}    
        access_token = data['access_token']
        validate_token(access_token)
        if data['id_cause'] is None:
            raise Exception('You must provide the id of cause to tell their operations')
        else:
            owner = get_cause_by_id(data['id_cause'])
            if owner is None:
                raise Exception('Invalid owner')
            else:
                result = {}
                result["love_cause"] = get_operation_count_by_operation_type(owner, data['operation_type_one'], data['time_unit']);
                result["fly_cause"] = get_operation_count_by_operation_type(owner, data['operation_type_two'], data['time_unit']);                
                result["love_posts"] = get_operation_count_on_post_by_operation_type(owner, data['operation_type_one'], data['time_unit']);
                result["fly_posts"] = get_operation_count_on_post_by_operation_type(owner, data['operation_type_two'], data['time_unit']);
                response = make_template_response(result, 'operation/count_operations_by_cause.json')
                return response
    except Exception as e:
        data={}
        data['error'] = e
        return make_error_response(data)
    
'''
@summary: restfult service for the user session logout. 
@param access_token:
@return: ok
@status: tested 19/08/2014
'''
@services_app.route('/operation/logout', methods=['POST'])
def restful_operation_logout():
    data={}
    try :
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)
        
        user = get_user_by_token(access_token)
        id_bee = user.parameters['id_bee']
        owner = get_bee_by_id(id_bee)
        
        #looking for the type of operation
        operation_type = get_operation_type('OTLO') 
          
        result = {}
        result['message']= 'ok'
        create_operation_bee(owner, owner, operation_type)
        return make_template_response(result,'ok.json')
    except Exception as e:
        data={}
        data['error'] = e
        return make_template_response(data,'error.json')
            
#===============================================================================
#Solo para uso de pruebas, para guardar un tipo de operacion y 
#un tipo de notificacion (debe ser borrado luego)
#===============================================================================
@services_app.route('/operation/operation_type', methods=['GET'])
def test_save_opration_type():
    operation_type = OperationType(codename='OTLA', name= 'operation love action').save()
    operation_type = OperationType(codename='OTFO', name= 'operation follow').save()
    operation_type = OperationType(codename='OTGL', name= 'operation give love').save()
    operation_type = OperationType(codename='OTAF', name= 'operation approve friendship').save()
    operation_type = OperationType(codename='OTRF', name= 'operation reject friendship').save()
    operation_type = OperationType(codename='OTBB', name= 'operation block bee').save()
    operation_type = OperationType(codename='OTFLY', name= 'operation fly post or cause').save()
    operation_type = OperationType(codename='OTLO', name= 'operation logout').save()
    #celebrity= Celebrity(name='El chavo', description='new celebrity').save()
    #cause = Cause(name='nueva causa', goal='nose').save()
    notification_type = NotificationType(codename='NTLA', name='notification love action').save()
    notification_type = NotificationType(codename='NTFS', name='notification friendship request').save()
    notification_type = NotificationType(codename='NTGL', name='notification give love').save()
    notification_type = NotificationType(codename='NTAF', name='notification approve friendship').save()
    notification_type = NotificationType(codename='NTFLY', name='notification fly post or cause').save()
    notification_type = NotificationType(codename='NTCO', name='notification post comment').save()
    result = {}
    result['message']= 'ok'
    return make_template_response(result,'ok.json')
#------------------------------------------------------------------------------ 
