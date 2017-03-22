'''
Created on 26/06/2014

@author: palencia77
'''
from com.data.models import *
import base64
from bson.objectid import ObjectId

'''
@summary: Method that created resources in post
@param post:
@param bee:
@param resource: 
@status: Tested
'''
def create_resource_in_post(post,bee,resource):
    resource = Resource(name=resource['name'],text=resource['text'],
                        binary_content=base64.b64decode(resource['binary_content']),
                        content_type=resource['content_type'],owner=bee,post=post)
    resource.save()
    post.resource_refs.append(resource.id)
    post.save()
    return resource

'''
@summary: Method that created resources in award
@param award:
@param bee:
@param resource: 
@status: 
'''
def create_resource_in_award(award,bee,resource):
    resource = Resource(name=resource['name'],text=resource['text'],
                        binary_content=base64.b64decode(resource['binary_content']),
                        content_type=resource['content_type'],owner=bee,award=award)
    resource.save()
    award.resource_refs.append(resource.id)
    award.save()
    return resource

'''
@summary: Generic method that remove all resources of a object passed as a parameter (object: Post or Bee)
@param object with resources:
'''  
def delete_resources_by_object(object):   
    try:
        resources_number = len(object.resource_refs)
        if (resources_number > 0):
            for id_resource in object.resource_refs:
                resource = get_resource_by_id(id_resource)
                resource.delete()        
    except Exception as e:
        return e 

'''
@summary: Method that get a resource by id
@param id_resource:
@return: Object Resource
'''     
def get_resource_by_id(id_resource):
    resource = Resource.objects.get(id = ObjectId(id_resource))
    return resource 

'''
@summary: Method that created resources in BEE
@param bee:
@param resource: 
@status: in process
'''
def create_resource_bee(bee,resource,*key):
    resource = Resource(name=resource['name'],text=resource['text'],binary_content=base64.b64decode(resource['binary_content']),content_type=resource['content_type'],owner=bee)
    resource.save()
    bee.resource_refs.append(resource.id)
    if isinstance(bee,Cause):
        bee.parameters[str(key[0])]=resource.id
    elif isinstance(bee,Partner):
        bee.parameters[str(key[0])]=resource.id
    elif isinstance(bee,Celebrity):
        bee.parameters[str(key[0])]=resource.id
    elif isinstance(bee,Person):
        bee.parameters[str(key[0])]=resource.id
    bee.save()       
    return resource

'''
@summary: Method that created resources in BEE
@param bee:
@param resource: 
@status: in process
'''
def update_resource_bee(bee,resource,*key):  
    resource = Resource(name=resource['name'],text=resource['text'],binary_content=base64.b64decode(resource['binary_content']),content_type=resource['content_type'],owner=bee)
    resource.save()
    if isinstance(bee,Person):
        bee.resource_refs.append(resource.id)
        bee.save()
    elif isinstance(bee,Cause):
        del bee.parameters
        bee.parameters[str(key[0])]=resource.id
        bee.save()
    elif isinstance(bee,Partner):
        bee.parameters[str(key[0])]=resource.id
        bee.save()
    elif isinstance(bee,Celebrity):
        bee.parameters[str(key[0])]=resource.id
        bee.save()        
    return resource

'''
@summary: Method for searching resources of a BEE
@param bee: Object(bee)
@param page_number: integer
@param page_size: integer
@status: Tested (10/07/2014)
'''
def get_resources_by_bee(bee,page_number = 0, page_size = 3):
        result = {}
        paginate_result = Pagination(Resource.objects.filter(owner = bee).order_by('-created_date'),int(page_number),int(page_size))    
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
@summary: Method that remove a resource of a object Bee or Post
@param object: Object(bee or post)
@param id_resource: string id of the removed resource
'''
def remove_resource(object,resource):
    try:
        id_resource = resource.id
        object_resources = object.resource_refs
        top = len(object_resources)
        for i in range(0,top):
            if(object_resources[i]==id_resource):
                del object.resource_refs[i]
                object.save()
                resource.delete()
                break
        return True    
    except Exception as e:
        return e

'''
@summary: Method for searching resources of a post
@param post: Object(post)
@param page_number: integer
@param page_size: integer
@status: Tested (12/08/2014)
'''
def get_resources_by_post(post ,page_number = 0, page_size = 3):
        result = {}
        paginate_result = Pagination(Resource.objects.filter(post = post).order_by('-created_date'),int(page_number),int(page_size))    
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
@summary: Method for searching resources of a award
@param award: Object(award)
@param page_number: integer
@param page_size: integer
@status: 
'''
def get_resources_by_award(award ,page_number = 0, page_size = 3):
        result = {}
        paginate_result = Pagination(Resource.objects.filter(award = award).order_by('-created_date'),int(page_number),int(page_size))    
        result['page_number'] = page_number
        result['page_size'] = page_size
        result['total_pages'] =  paginate_result.pages 
        result['total_elements'] = paginate_result.total
        result['content'] = paginate_result.items
        result['number_elements'] = len(paginate_result.items)
        result['first_page'] = not paginate_result.has_prev
        result['last_page'] = not paginate_result.has_next
        return result