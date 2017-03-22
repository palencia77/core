'''
Created on 26/06/2014

@author: palencia77
'''
from com.data.models import *
from bson.objectid import ObjectId

'''
@summary: Method that creates a request_friendship
@param owner: type object (Bee)
@param destination: type object (Bee)
@param status: string
'''
def create_request_friendship(owner, destination):
    request = RequestFriendship(owner=owner, destination=destination)
    request.save()
   
'''
@summary: Method that allows you to find a friend request given some attributes
@param owner: type object (Bee)
@param destination: type object (Bee)
@param status: string
@return array of objects request_friendship or false
'''    
def get_request_friendship_by_attributes(owner, destination, status):
    request_friendship = RequestFriendship.objects.filter(owner=owner, destination=destination, status=status)
    if request_friendship.count() > 0:
        return True
    else:
        return False
    
'''
@summary: Method that allows you to find a friend request by id
@param id_request_frinship:
@return request_friendship (object type)
'''    
def get_request_friendship_by_id(id_request_frienship):
    request_friendship = RequestFriendship.objects.get(id = ObjectId(id_request_frienship))
    return request_friendship
   
'''
@summary: Method that allows to update the status of a friend request
@param request_friendship: type object (RequestFriendship)
@param status: string
'''    
def update_status_request_friendship(request_friendship, status):
    request_friendship.status = status
    request_friendship.save() 