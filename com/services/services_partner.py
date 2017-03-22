'''
Created on 08/07/2014

@author: palencia77
'''
from flask import request
from com.restful.__init__ import services_app
from com.data.models import *
from bson.objectid import ObjectId
from com.services.services_resource import *
from com.tools.objects_status import *
from com.tools.tools_general import *
from com.tools.project_paths import *

'''
@summary: Method that save a new partner
@param name, description, geographic_location, resources, with_resource, owner
@return: id_partner: The partner created
@status: Tested
'''
def register_partner(name, description, owner, email, telephone, web_site, address, facebook, twitter, google_plus, resources, with_resource):
    partner = Partner(name=name, description=description, owner=owner, email=email, telephone=telephone, web_site=web_site, address=address, status=STATUS_OBJECT_ACTIVE, facebook=facebook, twitter=twitter, google_plus=google_plus)
    partner.administrators_refs.append(owner.id)
    partner.save()
    short_url = goo_shorten_url_bitly(PERSON_URL_BASE+str(partner.id))
    partner.short_url = short_url
    partner.save()
    
    # Saving resources:
    if with_resource == "True":     
        if 'avatar' in resources:
            if resources['avatar'] is not None:
                avatar = resources['avatar']
                create_resource_bee(partner, avatar, "avatar")
        if 'cover' in resources:
            if resources['cover'] is not None:
                cover = resources['cover']
                create_resource_bee(partner, cover, "cover")
        if 'promotional_photo' in resources:
            if resources['promotional_photo'] is not None:
                promotional_photo = resources['promotional_photo']
                create_resource_bee(partner, promotional_photo, "promotional_photo")
        if 'promotional_video' in resources:
            if resources['promotional_video'] is not None:
                promotional_video = resources['promotional_video']
                create_resource_bee(partner, promotional_video, "promotional_video")
    partner.save()
    return partner.id

'''
@summary: Method update a partner
@param partner, name, description, geographic_location
@status: Tested
'''
def update_partner(partner, name, description, email, telephone, web_site, address, facebook, twitter, google_plus, resources, with_resource):
    partner.name = name
    partner.description = description
    partner.email = email
    partner.telephone = telephone
    partner.web_site = web_site
    partner.address = address 
    partner.facebook = facebook
    partner.twitter = twitter
    partner.google_plus = google_plus 
    partner.save()
    
    # Saving resources:
    if with_resource == "True":     
        if 'avatar' in resources:
            if resources['avatar'] is not None:
                avatar = resources['avatar']
                create_resource_bee(partner, avatar, "avatar")
        if 'cover' in resources:
            if resources['cover'] is not None:
                cover = resources['cover']
                create_resource_bee(partner, cover, "cover")
        if 'promotional_photo' in resources:
            if resources['promotional_photo'] is not None:
                promotional_photo = resources['promotional_photo']
                create_resource_bee(partner, promotional_photo, "promotional_photo")
        if 'promotional_video' in resources:
            if resources['promotional_video'] is not None:
                promotional_video = resources['promotional_video']
                create_resource_bee(partner, promotional_video, "promotional_video")
    return partner.id

'''
@summary: Method that get a partner by id
@param id_partner
@return: partner object
@status: Tested
'''  
def get_partner_by_id(id_partner):
    partner = Partner.objects.get(id=ObjectId(id_partner))
    return partner

'''
@summary: Method seeking paginated partner belonging to status and name
@param status:
@param name_filter: 
@param page_number: 
@param page_size:  
@status: tested
''' 
def get_paginated_partners_by_status_and_name(status, name_filter="", page_number=1, page_size=7):
    result = {}
    if status is None:
        partners = Partner.objects
    else:        
        partners = Partner.objects.filter(name__icontains=name_filter, status=status)
    paginate_result = Pagination(partners, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] = paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method that update status of a partner
@param partner: object
@return: True or Exception
@status: Tested 08/08/2014
'''  
def partner_update_status(partner, status):
    partner.status = status
    partner.save()
    return True

'''
@summary: Method seeking of all partners of a cause (optional: by name)
@param cause:
@param name_filter: Empty or String
@param page_number:
@param page_size:  
@status: Tested (22/08/2014)
''' 
def get_partners_associated_to_cause(cause, name_filter, page_number=1, page_size=7):
    result = {}  
    partners = []
    for partner in cause.partners:
        if partner.status == STATUS_OBJECT_ACTIVE and name_filter.lower() in partner.name.lower():
            partners.append(partner)
    paginate_result = Pagination(partners, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method seeking of all partners of a cause (optional: by name)
@param cause:
@param name_filter: Empty or String
@param page_number: 
@param page_size:  
@status: Tested (22/08/2014)
''' 
def get_partners_not_associated_to_cause(cause, name_filter, page_number=1, page_size=7):
    result = {}
    id_partners = []
    for partner in cause.partners:
        id_partners.append(partner.id)
    partners = Partner.objects.filter(name__icontains=name_filter, status=STATUS_OBJECT_ACTIVE, id__nin=id_partners)
    paginate_result = Pagination(partners, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result
