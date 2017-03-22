import datetime
from com.data.models import *
from bson.objectid import ObjectId
from com.tools.tools_general import *
#from django.core.paginator import Paginator
#import json

'''
@summary: Method that allows you to find the type of interaction for codename
@param codename: attribute that enables a nickname for the type of interaction
@return: Object object interaction_type 
'''
def get_interaction_type(codename):
    interaction_type = InteractionType.objects.get(codename=codename)
    return interaction_type

'''
@summary: Method that allows you to find the interaction for id
@param id_interaction: 
@return:  interaction 
'''
def get_interaction_by_id(id_interaction):
    interaction = Interaction.objects.get(id=ObjectId(id_interaction))
    return interaction

'''
@summary: Method that creates a interaction
@param name:
@param interaction_type: type object
'''
def create_interaction(name, interaction_type):
    Interaction(name=name, interaction_type=interaction_type).save()
    return True

'''
@summary: 
@param status:    
@status: Building
''' 
def get_interactions_types_by_status(status):    
    interactions_type = InteractionType.objects(status=status)
    return interactions_type

'''
@summary: 
@param status:    
@status: Building
'''    
def get_interactions_by_status(interaction_type, status):
    interactions = Interaction.objects(interaction_type=interaction_type, status=status)
    return interactions

'''
@summary: 
@param status:    
@status: Building
'''    
def update_interaction(interaction,value):
    interaction.value = value
    interaction.save()
    return True

'''
@summary: Service that get a interaction by name and type
@param name:
@param type:
@status: Tested 27/11/2014
'''
def get_interaction_by_name_and_type(interaction_name, id_interaction_type):
    interaction_type = get_interaction_type(id_interaction_type)
    interaction = Interaction.objects.get(name=interaction_name, interaction_type=interaction_type)
    return interaction

'''
@summary: Service create interactionlog to bee
@param owner:
@param interaction:
@param interaction_value:
@param destination:
@status: underConstruction
'''
def create_interaction_log_bee(owner, interaction, interaction_value, destination):
    compose_week_year = composing_date()
    interaction_log = InteractionBee(owner=owner, interaction_name=interaction.name, interaction_type=interaction.interaction_type.id, value=interaction_value, bee_destination=destination,interaction_year_week=compose_week_year)
    interaction_log.save()

'''
@summary: Service create interactionlog to post
@param owner:
@param interaction:
@param interaction_value:
@param destination:
@status: underConstruction
'''
def create_interaction_log_post(owner, interaction, interaction_value, destination):
    compose_week_year = composing_date()
    interaction_log = InteractionPost(owner=owner, interaction_name=interaction.name, interaction_type=interaction.interaction_type.id, value=interaction_value, post_destination=destination,interaction_year_week=compose_week_year)
    print "GUARDE"
    interaction_log.save()

'''
@summary: Service create interactionlog to award
@param owner:
@param interaction:
@param interaction_value:
@param destination:
@status: underConstruction
'''
def create_interaction_log_award(owner, interaction, interaction_value, destination):
    compose_week_year = composing_date()
    interaction_log = InteractionAward(owner=owner, interaction_name=interaction.name, interaction_type=interaction.interaction_type.id, value=interaction_value, award_destination=destination, interaction_year_week=compose_week_year)
    interaction_log.save()
'''
@summary: Service create interactionlog to comment
@param owner:
@param interaction:
@param interaction_value:
@param destination:
@status: underConstruction
'''
def create_interaction_log_comment(owner, interaction, interaction_value, destination):
    compose_week_year = composing_date()
    interaction_log = InteractionAward(owner=owner, interaction_name=interaction.name, interaction_type=interaction.interaction_type.id, value=interaction_value, comment_destination=destination,interaction_year_week=compose_week_year)
    interaction_log.save()

'''
summary :this service get ranking
'''
def get_interaction_count_by_type(page_number=1, page_size=3):
    result = {}
    cdate = str(composing_date())
    result_interaction = InteractionLog._get_collection().aggregate( [
                               { "$match" : {"interaction_year_week" : cdate}} ,
                               { "$group" : {"_id" :  {"bee_person" : "$owner","name" : "$owner_name"},"love_score" : { "$sum" :"$value" }}},
                               { "$sort" : { "love_score" : -1} },
                               { "$limit" : 10*int(page_number)},
                               ])
    result['content'] =result_interaction
    return result





