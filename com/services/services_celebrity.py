'''
Created on 08/07/2014

@author: palencia77
'''
from com.data.models import *
from com.tools.tools_general import *
from com.services.services_resource import *
from bson.objectid import ObjectId
from com.tools.objects_status import *
from com.tools.project_paths import *

'''
@summary: Method that save a new celebrity
@param name, description, owner, email,
@param telephone, web_site, facebook, twitter,
@param google_plus, address, resources, with_resource 
@return: id_celebrity: The celebrity created
@status: Tested (08/07/2014)
'''
def register_celebrity(name, description, owner, email, telephone, web_site, facebook, twitter,
                       google_plus, address, resources, with_resource=False):
    #Saving basic information of celebrity:
    celebrity = Celebrity(name=name, description=description, owner=owner, email=email,
                          telephone=telephone, web_site=web_site, facebook=facebook, twitter=twitter,
                          google_plus=google_plus, address=address, status=STATUS_OBJECT_ACTIVE)
    celebrity.administrators_refs.append(owner.id)
    celebrity.save()
    
    #Saving the short ulr of the celebrity
    short_url = goo_shorten_url_bitly(CELEBRITY_URL_BASE+str(celebrity.id))
    celebrity.short_url = short_url
    celebrity.save()
    
    #Saving resources:
    if with_resource == "True":
        if 'avatar' in resources:
            if resources['avatar'] is not None:
                avatar = resources['avatar']
                create_resource_bee(celebrity,avatar,"avatar")
        if 'cover' in resources:
            if resources['cover'] is not None:
                cover = resources['cover']
                create_resource_bee(celebrity,cover,"cover")
        if 'promotional_photo' in resources:
            if resources['promotional_photo'] is not None:
                promotional_photo = resources['promotional_photo']
                create_resource_bee(celebrity,promotional_photo,"promotional_photo")
        if 'promotional_video' in resources:
            if resources['promotional_video'] is not None:
                promotional_video = resources['promotional_video']
                create_resource_bee(celebrity,promotional_video,"promotional_video")
    celebrity.save()
    return celebrity.id

'''
@summary: Method to get a celebrity by id
@param id_celebrity:
@return: Object Celebrity
'''
def get_celebrity_by_id(id_celebrity):
    celebrity = Celebrity.objects.get(id = ObjectId(id_celebrity))
    return celebrity

'''
@summary: Method to get the existence of a celebrity
@param id_celebrity:
@return: True or False
'''     
def there_is_celebrity(id_celebrity):
    celebrity = Celebrity.objects.filter(id = ObjectId(id_celebrity))
    if(celebrity.count > 0):
        return True
    else: return False
    
'''
@summary: method that updates the profile information of a celebrity
@param bee: Object(bee)
@param name, description, owner, email,
@param telephone, web_site, facebook, twitter,
@param google_plus, address, resources, with_resource 
@status: Tested 14/07/2014
'''
def update_celebrity(bee, name, description, owner, email, telephone, web_site,
                     facebook, twitter, google_plus, address, resources, with_resource):    
    bee.name = name
    bee.description = description
    bee.owner = owner
    bee.email = email
    bee.telephone = telephone
    bee.web_site = web_site
    bee.facebook = facebook
    bee.twitter = twitter
    bee.google_plus = google_plus
    bee.address = address
    bee.save()
    #Saving resources:
    if with_resource == "True":
        if 'avatar' in resources:
            if resources['avatar'] is not None:
                avatar = resources['avatar']
                create_resource_bee(bee,avatar,"avatar")
        if 'cover' in resources:
            if resources['cover'] is not None:
                cover = resources['cover']
                create_resource_bee(bee,cover,"cover")
        if 'promotional_photo' in resources:
            if resources['promotional_photo'] is not None:
                promotional_photo = resources['promotional_photo']
                create_resource_bee(bee,promotional_photo,"promotional_photo")
        if 'promotional_video' in resources:
            if resources['promotional_video'] is not None:
                promotional_video = resources['promotional_video']
                create_resource_bee(bee,promotional_video,"promotional_video")
    bee.save()
    return bee.id

'''
@summary: Returns all celebrities
@param page_number: 
@param page_size: 
@status: Tested 11/07/2014
'''
''' COMENTED: 29/08/2014 TENTATIVE TO REMOVE
def get_celebrity_all(page_number=1, page_size=7):
    result = {}
    paginate_result = Pagination(Celebrity.objects, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result
'''

'''
@summary: Method seeking paginated celebrities belonging to status and name
@param status: 
@param name_filter: 
@param page_number:    
@param page_size: 
@status: tested
''' 
def get_paginated_celebrities_by_status_and_name(status, name_filter="",page_number=1,page_size=7):
    result = {}
    if status is None:
        celebrities = Celebrity.objects
    else:        
        celebrities = Celebrity.objects.filter(name__icontains=name_filter, status=status).order_by('-created_date')
    paginate_result = Pagination(celebrities, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method that update status of a celebrity
@param celebrity: object
@return: True or Exception
@status: Tested 08/08/2014
'''  
def celebrity_update_status(celebrity,status):
    celebrity.status = status
    celebrity.save()
    return True

'''
@summary: Method seeking celebrities associated to one cause (optional: by name)
@param cause:
@param name_filter: Empty or String
@param page_number:
@param page_size:      
@status: Tested (27/08/2014)
''' 
def get_celebrities_associated_to_cause(cause, name_filter, page_number=1, page_size=7):
    result = {}  
    celebrities = []
    for celebrity in cause.celebrities:
        if celebrity.status == STATUS_OBJECT_ACTIVE and name_filter.lower() in celebrity.name.lower():
            celebrities.append(celebrity)
    paginate_result = Pagination(celebrities, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method seeking celebrities not associated to one cause (optional: by name)
@param cause:
@param name_filter: Empty or String  
@param page_number:
@param page_size:  
@status: Tested (27/08/2014)
''' 
def get_celebrities_not_associated_to_cause(cause, name_filter, page_number=1, page_size=7):
    result = {}
    id_celebrities = []
    for celebrity in cause.celebrities:
        id_celebrities.append(celebrity.id)
    celebrities = Celebrity.objects.filter(name__icontains=name_filter, status=STATUS_OBJECT_ACTIVE, id__nin=id_celebrities)
    paginate_result = Pagination(celebrities, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result