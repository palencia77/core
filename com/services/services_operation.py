'''
Created on 26/06/2014

@author: palencia77
'''
import datetime
from com.data.models import *
from bson.objectid import ObjectId

'''
@summary: Method that allows you to find the type of operation for codename
@param codename: attribute that enables a nickname for the type of operation
@return: Object object OperationType 
'''
def get_operation_type(codename):
    operation_type = OperationType.objects.get(codename=codename)
    return operation_type

'''
@summary: Method that creates a operation_log
@param owner: type object
@param post_destination: type object Post
@param operation_type: type object
'''
def create_operation_post(owner, post_destination, operation_type):
    operation = OperationPost(owner=owner, post_destination=post_destination, operation_type=operation_type)
    operation.save()

'''
@summary: Method that creates a operation_log
@param owner: type object
@param bee_destination: type object Bee
@param operation_type: type object
'''                
def create_operation_bee(owner, bee_destination, operation_type):
    operationBee = OperationBee(owner=owner, bee_destination=bee_destination, operation_type=operation_type)
    operationBee.save()

'''
@summary: Method that creates a operation_log
@param owner: type object
@param award_destination: type object Bee
@param operation_type: type object
'''
def create_operation_award(owner, award_destination, operation_type):
    operationAward = OperationAward(owner=owner, award_destination=award_destination, operation_type=operation_type)
    operationAward.save()
    
'''
@summary: Method that creates a operation_log
@param owner: type object
@param comment_destination: type object Comment
@param operation_type: type object
'''                
def create_operation_comment(owner, comment_destination, operation_type):
    operationComment = OperationComment(owner=owner, comment_destination=comment_destination, operation_type=operation_type)
    operationComment.save()
    
'''
@summary: Method to check if there was an operation on a publication of a bee(person)
@param owner: type object
@param post_destination: type object, one of the two is null
@param operation_type: type object
@return: True or False
'''
def there_is_operation_on_post(owner, destination, operation_type):
    operation = OperationPost.objects.filter(owner=owner, post_destination=destination, operation_type=operation_type)
    if operation.count() > 0:
        return True          
    else:
        return False    

'''
@summary: Method to check if there was an operation on a bee(cause) of a bee(person)
@param owner: type object
@param bee_destination: type object
@param operation_type: type object
@return: True or False
'''     
def there_is_operation_on_bee(owner, destination, operation_type):
    operation = OperationBee.objects.filter(owner=owner,bee_destination=destination, operation_type=operation_type)               
    if operation.count() > 0:
        return True          
    else:
        return False   
    
'''
@summary: Method that allows for operationComment by attributes
@param owner: type object
@param comment_destination: type object
@param operation_type: type object
@return: True or False
'''     
def get_operation_comment_by_attributes(owner, destination, operation_type):  
    operation = OperationComment.objects.filter(owner=owner,comment_destination=destination, operation_type=operation_type)
    if (operation.count() > 0):
        return True          
    else:
        return False
    
'''
@summary: Method that counts the number of operations performed by each point at a time interval 
        by one type of operation
@param bee_destination: type object
@param operation_type: type String
@param time_unit: type String (year/month/day)
@return: result
'''     
def get_operation_count_by_operation_type(bee_destination, operation_type, time_unit = "day"):
    result = {}
    
    if(time_unit=="day" or time_unit is None):
        operation = OperationBee._get_collection().aggregate( [ 
                                { "$match" : { "bee_destination" : ObjectId(bee_destination.id), "operation_type" : operation_type } } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }, "month" : {"$month" : "$created_date" }, "day" : {"$dayOfMonth" : "$created_date" } } ,"amount" : { "$sum" :1 } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ])       
    elif(time_unit=="month"):
        operation = OperationBee._get_collection().aggregate( [ 
                                { "$match" : { "bee_destination" : ObjectId(bee_destination.id), "operation_type" : operation_type } } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }, "month" : {"$month" : "$created_date" }} ,"amount" : { "$sum" :1 } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ])
    else:
        operation = OperationBee._get_collection().aggregate( [ 
                                { "$match" : { "bee_destination" : ObjectId(bee_destination.id), "operation_type" : operation_type } } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }} ,"amount" : { "$sum" :1 } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ])            
    result['content'] = operation
    result['time_unit'] = time_unit
    return result        

'''
@summary: Method that counts the number of operations in the post of a cause for every point in a
         time interval for operation type
@param owner: type object
@param operation_type: type String
@param time_unit: type String (year/month/day)
@return: result
'''     
def get_operation_count_on_post_by_operation_type(owner, operation_type, time_unit = "day"):
    result = {}
    
    if(operation_type=="OTLA"):
        if(time_unit=="day" or time_unit is None):
            operation = Post._get_collection().aggregate( [ 
                                { "$match" : { "owner" : ObjectId(owner.id)} } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }, "month" : {"$month" : "$created_date" }, "day" : {"$dayOfMonth" : "$created_date" } } ,"amount" : { "$sum" :"$love_counter" } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ])
        elif(time_unit=="month"):
            operation = OperationBee._get_collection().aggregate( [ 
                                { "$match" : { "bee_destination" : ObjectId(owner.id)} } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }, "month" : {"$month" : "$created_date" }} ,"amount" : { "$sum" : "$love_counter" } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ])
        else:
            operation = OperationBee._get_collection().aggregate( [ 
                                { "$match" : { "bee_destination" : ObjectId(owner.id) } } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }} ,"amount" : { "$sum" :"$love_counter" } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ]) 
    else:
        if(time_unit=="day" or time_unit is None):
            operation = Post._get_collection().aggregate( [ 
                                { "$match" : { "owner" : ObjectId(owner.id)} } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }, "month" : {"$month" : "$created_date" }, "day" : {"$dayOfMonth" : "$created_date" } } ,"amount" : { "$sum" :"$fly_counter" } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ])
        elif(time_unit=="month"):
            operation = OperationBee._get_collection().aggregate( [ 
                                { "$match" : { "bee_destination" : ObjectId(owner.id)} } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }, "month" : {"$month" : "$created_date" }} ,"amount" : { "$sum" : "$fly_counter" } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ])
        else:
            operation = OperationBee._get_collection().aggregate( [ 
                                { "$match" : { "bee_destination" : ObjectId(owner.id) } } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }} ,"amount" : { "$sum" :"$fly_counter" } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ])         
    result['content'] = operation
    result['time_unit'] = time_unit
    return result 

'''
@summary: Method that counts the number of operations performed by each point at a time interval 
        by one type of operation and by post_destination
@param post_destination: type object
@param operation_type: type String
@param time_unit: type String (year/month/day)
@return: result
@status: tested 15/09/2014
'''     
def get_count_operation_type_by_post(post_destination, operation_type, time_unit = "day"):
    result = {}
    
    if(time_unit=="day" or time_unit is None):
        operation = OperationPost._get_collection().aggregate( [ 
                                { "$match" : { "post_destination" : ObjectId(post_destination.id), "operation_type" : operation_type } } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }, "month" : {"$month" : "$created_date" }, "day" : {"$dayOfMonth" : "$created_date" } } ,"amount" : { "$sum" :1 } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ])       
    elif(time_unit=="month"):
        operation = OperationPost._get_collection().aggregate( [ 
                                { "$match" : { "post_destination" : ObjectId(post_destination.id), "operation_type" : operation_type } } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }, "month" : {"$month" : "$created_date" }} ,"amount" : { "$sum" :1 } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ])
    else:
        operation = OperationPost._get_collection().aggregate( [ 
                                { "$match" : { "post_destination" : ObjectId(post_destination.id), "operation_type" : operation_type } } , 
                                { "$group" : {"_id" : { "year" : {"$year" : "$created_date" }} ,"amount" : { "$sum" :1 } } }, 
                                { "$sort" : { "_id" : 1 } } 
                                ])            
    result['content'] = operation
    result['time_unit'] = time_unit
    return result 