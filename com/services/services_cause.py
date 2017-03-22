'''
Created on 30/06/2014

@author: palencia77
'''
import re
from flask import request
from com.restful.__init__ import services_app
from com.data.models import *
from bson.objectid import ObjectId
from com.services.services_resource import *
from com.services.services_scope import *
from com.tools.tools_general import *
from com.tools.objects_status import *
from com.tools.project_paths import *
import datetime


'''
@summary: Method to get a cause by id
@param id_cause:
@return: Object cause (bee)
'''    
def get_cause_by_id(id_cause):
    cause = Cause.objects.get(id = ObjectId(id_cause))
    return cause

'''
@summary: Method that increases the love that was donated to a cause
@param cause: type object(bee)
@param quantity_love: int
'''
def cause_receive_love(cause, quantity_love):
    cause.love_meter = cause.love_meter + quantity_love
    cause.save()
    return cause

'''
@summary: Method that save a new cause
@param name, description, resources, owner
@param geographic_location, goal, scope, start_date, 
@param closing_date, love_goal, ambassadors, contacts,
@param beneficiary, responsible, risk_classification
@return: id_cause: The cause created
@status: Tested 07/07/2014
'''
def register_cause(name, description, resources, geographic_location,
                   goal, scope, start_date, closing_date,
                   love_goal, ambassadors, contacts, beneficiary, owner, responsible,
                   risk_classification,url_promotional_video,with_resource=False):
    
    cause_closing_date = None
    if closing_date is not None:
        #cause_closing_date=datetime(*map(int, re.split('[^\d]', str(closing_date))[:-1]))
        cause_closing_date = None
    else:
        cause_closing_date = None   
    #Saving basic information of cause:
    cause = Cause(name=name, description=description, owner=owner, responsible=responsible,
                      geographic_location=geographic_location, goal=goal ,sub_scope=scope,
                      start_date=start_date, closing_date=cause_closing_date, love_goal=love_goal, 
                      beneficiary=beneficiary, risk_classification=risk_classification, 
                      status=STATUS_CAUSE_STANDBY, url_promotional_video=url_promotional_video)
    #Saving the contacts of the cause:
    if contacts != None:
        for contact in contacts:
            contact = Contact(name=contact['name'], email=contact['email'], mobile_phone=contact['mobile_phone'], 
                              telephone=contact['telephone'], organization=contact['organization'], 
                              address=contact['address'])
            contact.save()
            cause.contacts.append(contact)  
    cause.administrators_refs.append(owner.id)
    cause.save()
    
    #Saving the short ulr of the cause
    short_url = goo_shorten_url_bitly(CAUSE_URL_BASE+str(cause.id))
    cause.short_url = short_url
    cause.save()
    #Saving resources:
    if with_resource == "True":     
        if 'avatar' in resources:
            if resources['avatar'] != None:
                avatar = resources['avatar']
                create_resource_bee(cause,avatar,"avatar")
        if  'cover' in resources:
            if resources['cover'] != None:
                cover = resources['cover']
                create_resource_bee(cause,cover,"cover")
        if 'promotional_photo' in resources:
            if resources['promotional_photo'] != None:
                promotional_photo = resources['promotional_photo']
                create_resource_bee(cause,promotional_photo,"promotional_photo")
        if 'promotional_video' in resources:
            if resources['promotional_video'] != None:
                promotional_video = resources['promotional_video']
                create_resource_bee(cause,promotional_video,"promotional_video")
        if 'document' in resources:
            if resources['document'] != None:
                document = resources['document']
                create_resource_bee(cause,document,"document")
    #Saving ambassadors cause:
    #for ambassador in ambassadors:
    #cause.ambassadors.append(ObjectId(ambassador))
    #cause.save()
    return cause.id

'''
@summary: Method that update a cause
@param cause, name, description,
@param geographic_location, goal, scope, start_date, 
@param closing_date, love_goal, ambassadors,
@param beneficiary, responsible, risk_classification
@status: Tested 09/07/2014
'''
def update_cause(cause,name, description, resources, geographic_location,
                   goal, scope, start_date, closing_date,
                   love_goal, ambassadors, beneficiary, responsible, 
                   risk_classification,contacts,url_promotional_video,with_resource=False,): 
    #cause_closing_date=datetime(*map(int, re.split('[^\d]', str(closing_date))[:-1]))
    cause.name = name
    cause.description = description
    cause.responsible = responsible
    cause.geographic_location = geographic_location
    cause.goal = goal
    cause.sub_scope = scope
    cause.start_date = start_date
    cause.closing_date = None
    cause.love_goal = love_goal
    cause.beneficiary = beneficiary
    cause.risk_classification = risk_classification
    cause.url_promotional_video = url_promotional_video 
    #Saving the contacts of the cause:
    if contacts != None:
        for contact in contacts:
            contact = Contact(name=contact['name'], email=contact['email'], mobile_phone=contact['mobile_phone'], 
                              telephone=contact['telephone'], organization=contact['organization'], 
                              address=contact['address'])
            contact.save()
            cause.contacts.append(contact)  
    cause.save()  
    #===========================================================================
    # #ambassadors cause:
    # del cause.ambassadors
    # for ambassador in ambassadors:
    #     cause.ambassadors.append(ObjectId(ambassador))
    #===========================================================================

    #Saving resources:
    if with_resource == "True":     
        if 'avatar' in resources:
            if resources['avatar'] != None:
                avatar = resources['avatar']
                create_resource_bee(cause,avatar,"avatar")
        if  'cover' in resources:
            if resources['cover'] != None:
                cover = resources['cover']
                create_resource_bee(cause,cover,"cover")
        if 'promotional_photo' in resources:
            if resources['promotional_photo'] != None:
                promotional_photo = resources['promotional_photo']
                create_resource_bee(cause,promotional_photo,"promotional_photo")
        if 'promotional_video' in resources:
            if resources['promotional_video'] != None:
                promotional_video = resources['promotional_video']
                create_resource_bee(cause,promotional_video,"promotional_video")
        if 'document' in resources:
            if resources['document'] != None:
                document = resources['document']
                create_resource_bee(cause,document,"document")       
    '''
    #Saving ambassadors cause:
    for ambassador in ambassadors:
        cause.ambassadors.append(ObjectId(ambassador))
    
    '''

'''
@summary: Method seeking of all causes belonging to the scopes that follows a bee 
@param bee: Object(bee)    
@status: Building
'''
def get_causes_by_scopes_of_a_bee(bee):
    result_bee_causes = {}
    bee_causes = []
    for sub_scope in bee.sub_scope_refs:
        causes = []
        causes = Cause.objects.filter(sub_scope = sub_scope, id__nin = bee.bee_refs)
        for cause in causes:
            bee_causes.append(cause)   
    result_bee_causes['content'] = bee_causes
    return result_bee_causes

'''
@summary: Method increase fly_counter in  cause
@param Object cause:
'''       
def cause_fly_counter_increase(cause):
    cause.fly_counter += 1
    cause.save()   
        
'''
@summary: Method seeking of all causes belonging to sub scope
@param subscope:    
@status: Building
''' 
def get_causes_by_subscope(sub_scope):
    causes = Cause.objects.filter(sub_scope = sub_scope)
    return causes

'''
@summary: Method seeking paginated causes belonging to sub scope
@param subscope:    
@status: Building
''' 
def get_paginated_causes_by_subscope(sub_scope,page_number,page_size):
    result = {}
    causes = Cause.objects.filter(sub_scope = sub_scope)
    paginate_result = Pagination(causes, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method seeking paginated causes belonging to scope
@param subscope:    
@status: Building
''' 
def get_paginated_causes_by_scope(scope,page_number,page_size):
    result = []
    subscopes = get_sub_scopes_by_scope(scope)
    for subscope in subscopes:
        causes = list(get_causes_by_subscope(subscope))
        result = list(set(result+causes))
        #result.extend([cause for cause in list_causes if cause not in result])
    paginate_result = Pagination(result, int(page_number), int(page_size))
    result = {}
    result['page_number'] = page_number
    result['page_size'] = page_size
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method seeking paginated causes belonging to status
@param status:    
@status: Building
''' 
def get_paginated_causes_by_status(status,name_filter,page_number,page_size):
    result = {}
    if status == None:
        causes = Cause.objects
    else:        
        causes = Cause.objects(name__icontains=name_filter, status = status)
    paginate_result = Pagination(causes, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary:*** TEMPORAL: Method seeking paginated causes belonging to status TEMPORAL ****
@param status:    
@status: Building
#### BORRAR ##### 19/09/2014
''' 
def get_paginated_causes_active_and_solved(name_filter,page_number,page_size):
    result = {}       
    causes = Cause.objects(name__icontains=name_filter, status__ne=STATUS_CAUSE_STANDBY)
    paginate_result = Pagination(causes, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method that remove a contact of a cause
@param cause: Object(cause)
@param contact: Object(contact)
'''
def cause_remove_contact(cause,contact):
    try:    
        top = len(cause.contacts)
        for i in range(0,top):
            if(cause.contacts[i]==contact):
                del cause.contacts[i]
                cause.save()
                contact.delete()
                break
        return True    
    except Exception as e:
        return e

'''
@summary: Method that update status of a cause
@param cause: object
@return: True or Exception
@status: Tested 08/08/2014
'''  
def cause_update_status(cause, status):
    if status == STATUS_OBJECT_ACTIVE:
        cause.status = status
        cause.start_date = datetime.now()
    if status == STATUS_CAUSE_SOLVED:
        cause.status = status
        cause.finish_date = datetime.now
    cause.save()
    return True

'''
@summary: Method that remove the association between partner and cause
@param cause: Object(Cause)
@param id_partner:
'''
def cause_remove_partner_association(cause,id_partner):
    try:    
        top = len(cause.partners)
        for i in range(0,top):
            if str(cause.partners[i].id)==id_partner:
                del cause.partners[i]
                cause.save()
                break
        return True    
    except Exception as e:
        return e

'''
@summary: Method that create a new association between partner and cause
@param cause: Object(Cause)
@param partner: Object(Partner)
'''
def cause_create_partner_association(cause,partner):
    cause.partners.append(partner)
    cause.save()
    
'''
@summary: Method that remove the association between celebrity and cause
@param cause: Object(Cause)
@param id_celebrity:
'''
def cause_remove_celebrity_association(cause,id_celebrity):
    try:    
        top = len(cause.celebrities)
        for i in range(0,top):
            if(str(cause.celebrities[i].id)==id_celebrity):
                del cause.celebrities[i]
                cause.save()
                break
        return True    
    except Exception as e:
        return e

'''
@summary: Method that create a new association between celebrity and cause
@param cause: Object(Cause)
@param celebrity: Object(Celebrity)
'''
def cause_create_celebrity_association(cause,celebrity):
    cause.celebrities.append(celebrity)
    cause.save()