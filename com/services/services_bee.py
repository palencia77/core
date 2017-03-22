'''
Created on 20/06/2014

@author: palencia77
'''
from com.data.models import *
from bson.objectid import ObjectId

'''
@summary: Method to get a bee by id
@param id_bee:
@return: Object Bee
'''
def get_bee_by_id(id_bee):
    bee = Bee.objects.get(id=ObjectId(id_bee))
    return bee

'''
@summary: Method to get a bee by id and status
@param id_bee:
@return: Object Bee
'''
def get_bee_by_id_and_status(id_bee,status):
    bee = Bee.objects(Q(id=ObjectId(id_bee)) & (Q(status=status) | Q(status='PENDING')))
#     bee = Bee._get_collection().find({
#                                       "$and":
#                                             [
#                                               {"_id": ObjectId(id_bee)},
#                                               {"$or":[
#                                                        {"status":status},
#                                                        {"status":"PENDING"}
#                                                      ]
#                                               }
#                                             ]
#                                     })[0]
    return bee[0]

'''
@summary: Method to get a bee by id
@param id_bee:
@return: Object Bee
'''
def get_bee_by_owner(user_owner):
    bee = Bee.objects.get(owner=user_owner)
    return bee

'''
@summary: Method increase love_counter in bee
@param Object Bee
'''
def bee_love_counter_increase(bee):
    bee.love_counter += 1
    bee.save()

'''
@summary: Method to get the existence of a bee
@param id_bee:
@return: True or False
'''     
def there_is_bee(id_bee):
    bee=[]
    bee = Bee.objects.filter(id=ObjectId(id_bee))
    if bee.count > 0:
        return True
    else:
        return False
    
'''
@summary: Method that update the profile of a particular bee
@param id_bee:
@param name:
@param geographic_location:
'''
def bee_update_profile(bee,name,geographic_location):  
    bee.name=name
    bee.geographic_location=geographic_location
    bee.save()

'''
@summary: Method guarding the bee bee followed by
@param bee: object Bee
@param bee_followed : object Bee 
'''    
def bee_follow(bee, bee_followed):
    bee.bee_refs.append(bee_followed.id)
    bee.save()
    
    
'''
@summary: Method that creates the relationship of friendship
@param bee: object Bee
@param bee_followed : object Bee 
'''    
def bee_approve_friendship(bee1, bee2):
    bee1.bee_refs.append(bee2.id)
    bee2.bee_refs.append(bee1.id)
    bee1.save()
    bee2.save()

'''
@summary: Method to get a person by id
@param id_bee:
@return: Object Person
'''
def get_person_by_id(id_bee):
    bee = Person.objects.get(id = ObjectId(id_bee))
    return bee 

'''
@summary: Method seeking of the relationships of a bee according to the type 
          of relationship (Person, Partner, Celebrity or Cause)
@param bee: object Bee
@param page_number: integer
@param page_size: integer
@param Class: (Person, Celebrity or Cause)
@status: result 
'''

def get_relationships_of_a_bee(bee, page_number=1, page_size=3, Class=None):
        result = {}
        paginate_result = Pagination(Class.objects.filter(id__in = bee.bee_refs).order_by('-created_date'), int(page_number), int(page_size))
        result['page_number'] = page_number
        result['page_size'] = page_size
        result['total_pages'] =  paginate_result.pages 
        result['total_elements'] = paginate_result.total
        result['content'] = paginate_result.items
        result['number_elements'] = len(paginate_result.items)
        result['first_page'] = not paginate_result.has_prev
        result['last_page'] = not paginate_result.has_next
        return result
     
'''
@summary: Method that counts the number of relationships of a bee according to 
          the type of relationship (person, Partner, Celebrity or cause)
@param Class: (Person, Partner, Celebrity or Cause)    
@return: bee_friends.count()
'''    
def get_count_relationships_of_a_bee (bee, Class = None):
    bee_relationships = Class.objects.filter(id__in = bee.bee_refs)
    return bee_relationships.count()

'''
@summary: Method that allows adding a bee to blacklist
@param Bee: Object Type
@param id_bee_blocked: type string
'''
def bee_block_relationships(bee, id_bee_blocked):
    bee.bee_blocked_refs.append(id_bee_blocked)
    bee.save()
    
'''
@summary: Method that allows adding a bee to blacklist
@param Bee: Object Type
@param id_bee_blocked: type string
'''
def there_is_bee_blocked(bee, id_bee_blocked):
    for id in bee.bee_blocked_refs:
        if str(id) == id_bee_blocked:
            return True
        else:
            return False
'''
@summary: Method that allows adding a bee to a list of those who love action performed 
@param Bee: Object Type
@param id_bee_executor: type string
'''
def bee_save_executor_love_action(bee, id_bee_executor):
    bee.love_refs.append(id_bee_executor)
    bee.save()
    
'''
@summary: Method that allows adding a bee to a list of those who Fly action performed 
@param Bee: Object Type
@param id_bee_executor: type string
'''
def bee_save_executor_fly_action(bee, id_bee_executor):
    bee.fly_refs.append(id_bee_executor)
    bee.save()    
       
'''
@summary: method that allows increases the amount of love_score of a bee
@param bee: type object
@param love_quantity: int
'''
def bee_increment_love_score(bee, love_quantity):
    #Implement the conversion factor to increase the love_score:
    bee.love_score += love_quantity
    bee.save()
    return bee

'''
@summary: method that allows decrement the love_score of a bee
@param bee: type object
@param love_quantity: int
'''
def bee_decrement_love_score(bee, love_quantity):
    bee.love_score -= love_quantity
    bee.save()

'''
@summary: method that allows increases the amount of love_coin of a bee
@param bee: type object
@param love_quantity: int
'''
def bee_increment_love_coin(bee, love_quantity):
    #Implement the conversion factor to increase the love_coin:
    bee.love_coin += love_quantity
    bee.save()
    return bee

'''
@summary: method that allows decrement the love_coin of a bee
@param bee: type object
@param love_quantity: int
'''
def bee_decrement_love_coin(bee, love_quantity):
    bee.love_coin -= love_quantity
    bee.save()

'''
@summary: Method that update the list of administrators in particular a bee
@param bee: type object
@param id_administrator: string
@param operation: string
@return: index if exist or -1 if not exist
'''
def update_administrators_of_a_bee(bee, id_administrator, operation):
    if operation == 'add':
        bee.administrators_refs.append(id_administrator)
    elif get_administrator_of_a_bee(bee, id_administrator) != -1:
        index = get_administrator_of_a_bee(bee, id_administrator)
        del bee.administrators_refs[index]    
    bee.save()
'''
@summary: Method that update the list of administrators in particular a bee
@param bee: type object
@param id_administrator: string
@param operation: string
@return: index if exist or -1 if not exist
'''
def get_administrator_of_a_bee(bee,id_administrator):
    bee_administrarors = bee.administrators_refs
    top = len(bee_administrarors)
    for i in range(0,top):
        if(id_administrator==bee_administrarors[i]):
            return i
    return -1 

'''
@summary: Method to validate if a user has permission to act on behalf of a cause or celebrity
@param bee: type object
@param administrator: type object
@return: Returns an exception should not exist in the list of administrators
@status: Tested 14/07/2014
'''
def validate_administrator_permissions(bee, administrator):
    if administrator.id not in bee.administrators_refs:
        raise Exception('You do not have permission to perform this action')
    else:
        return True
    
'''
@summary: Method that remove logically a bee
@param bee: object
@return: Exception or error
@status: Tested 14/07/2014
'''  
def remove_bee(bee):
    bee.status = "removed"
    bee.save()
    return True

'''
@summary: Method that update the bee status
@param bee: object
@param status:
@return: True or Exception
@status: Tested 11/11/2014
'''
def bee_update_status(bee, status):
    bee.status = status
    bee.status_date = datetime.now
    bee.save()
    return True

'''
@summary: Method that update the specific field on a bee
@param id_bee: field
@param value:
@return: True or Exception
@status: Tested 24/11/2014
'''
def bee_update_attribute(id_bee, field, value):
    Bee._get_collection().update({"_id": ObjectId(id_bee), "status": "ACTIVE"},{"$set": { field: value }})

'''
@summary: Method that historical_ranking on a bee
@param id_bee: field
@param page_number
@param page_sizee
@return: True or Exception
@status: Tested 24/11/2014
'''
def bee_get_historical_ranking(page_number=1, page_size=3):
     result = {}
     paginate_result = Pagination(Person.objects(Q(status='ACTIVE') | Q(status='PENDING')).order_by('-love_score'), int(page_number), int(page_size))
     result['page_number'] = page_number
     result['page_size'] = page_size
     result['total_pages'] =  paginate_result.pages
     result['total_elements'] = paginate_result.total
     result['content'] = paginate_result.items
     result['number_elements'] = len(paginate_result.items)
     result['first_page'] = not paginate_result.has_prev
     result['last_page'] = not paginate_result.has_next
     return result
