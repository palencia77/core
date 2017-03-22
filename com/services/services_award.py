'''
Created on 10/11/2014

@author: palencia77
'''
from com.data.models import *
from com.services.services_resource import *
from com.tools.objects_status import *
from bson.objectid import ObjectId
from com.tools.email_subjects import *
from com.tools.tools_general import *
from flask import render_template

"""
@summary: Method to save a new Award
@param bee: 
@param tilte: 
@param text: 
@param with_resource:
@param amount_love: 
@param resources: 
@return id_award
@status: 
"""
def register_award(bee,title,text,quantity,amount_love,with_resource,resources):
    award=Award(title=title,text=text,owner=bee,quantity=quantity,amount_love=amount_love)
    award.save()
    #Saving the resources if exists:
    if (with_resource =="True"):
        for resource in resources:
            create_resource_in_award(award,bee,resource)
    return award.id


'''
@summary: Method that remove of a award
@param award: 
@status: validating 
'''
def award_update_status(award, status):
    try:
        award.status = status
        award.save()
    except Exception as e:
        return e     
        
'''
@summary: Method that get a award by id
@param id_award:
@return: Object Award
'''     
def get_award_by_id(id_award):
    award = Award.objects.get(id = ObjectId(id_award))
    return award 
   
'''
@summary: This method get paged awards
@param id_bee:
@param page_number: Number of the page to return
@param page_size: Number of publications per page
@return: json data
'''      
def get_awards_by_bee(id_bee,status,page_number=1,page_size=10):
    result = {}
    paginate_result = Pagination(Award.objects.filter(owner = id_bee, status=status).order_by('-created_date'), int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: This method get paged timeline publications of bee
@param id_bee:
@param page_number: Number of the page to return
@param page_size: Number of publications per page
@return: json data
'''      
def get_awards(id_bee,page_number=1,page_size=10):
    result = {}
    paginate_result = Pagination(Award.objects.order_by('-created_date'), int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

"""
@summary: Method to update a Award
@param award:
@param tilte: 
@param text: 
@param quantity:  
@param amount_love: 
@status: 
"""
def update_award(award,title,text,quantity,amount_love):
    award.title = title
    award.text = text
    award.quantity = quantity
    award.amount_love = amount_love
    award.save()
    return award.id

'''
@summary: Method seeking awards associated to one cause (optional: by name)
@param bee:
@param name_filter: Empty or String
@param page_number:
@param page_size:      
@status: Tested (27/08/2014)
''' 
def get_awards_associated_to_cause(bee, name_filter, page_number=1, page_size=7):
    result = {}  
    awards = []
    for award in bee.awards:
        if award.status == STATUS_OBJECT_ACTIVE and name_filter.lower() in award.title.lower():
            awards.append(award)
    paginate_result = Pagination(awards, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method seeking awards not associated to one cause (optional: by name)
@param cause:
@param name_filter: Empty or String  
@param page_number:
@param page_size:  
@status: Tested (27/08/2014)
''' 
def get_awards_not_associated_to_cause(cause, name_filter, page_number=1, page_size=7):
    result = {}
    id_awards = []
    for award in cause.awards:
        if award.status == STATUS_OBJECT_ACTIVE:
            id_awards.append(award.id)
    awards = Award.objects.filter(title__icontains=name_filter, quantity__gt = 0, id__nin=id_awards, status=STATUS_OBJECT_ACTIVE)
    paginate_result = Pagination(awards, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result 

'''
@summary: Method that remove the association between award and cause
@param cause: Object(Cause)
@param id_award:
'''
def cause_remove_award_association(cause,id_award):
    try:
        award = get_award_by_id(id_award)
        award.quantity = award.quantity + 1;
        award.save()
        top = len(cause.awards)
        for i in range(0,top):
            if(str(cause.awards[i].id)==id_award):
                del cause.awards[i]
                cause.save()
                break
        return True    
    except Exception as e:
        return e

'''
@summary: Method that create a new association between award and cause
@param cause: Object(Cause)
@param award: Object(Celebrity)
'''
def cause_create_award_association(cause,award):
    if award.quantity > 0:
        award.quantity = award.quantity - 1;
        award.save()
        cause.awards.append(award)
        cause.save()
    else:
        return False

'''
@summary: Method seeking paginated awards belonging to status
@param status:
@param name_filter
@param page_number
@param page_size
@status: Building
'''
def get_paginated_awards_by_status(status, name_filter, page_number, page_size):
    result = {}
    if status is None:
        awards = Award.objects
    else:
        awards = Award.objects(title__icontains=name_filter, status=status)
    paginate_result = Pagination(awards, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size
    result['total_elements'] = paginate_result.total
    result['total_pages'] = paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: This method allows bee redeem a lot of love for a awards
@param bee: Object bee
@param award: Object Award
@status: Tested 02/12/2014
'''
def award_purchase(bee, award):
    award.quantity = award.quantity - 1;
    award.save()
    bee.love_coin = bee.love_coin - award.amount_love
    bee.awards_refs.append(award)
    bee.save()   
  
    if(len(award.resource_refs) > 0):
        resource = get_resource_by_id(award.resource_refs[0])
        id_resource = resource.id
    else: id_resource = None        
    # Send the email with the information of award won:    
    data = {'user': bee.owner, 'award':award, 'id_resource':id_resource}
    subject_html = SUBJECT_BEE_PURCHASE_AWARD
    text_html = render_template('email/bee_purchase_award.html', data=data)
    send_email(bee.owner.email, subject_html, text_html)

'''
@summary: Method increase fly_counter in  award
@param Object award:
'''
def award_fly_counter_increase(award):
    award.fly_counter += 1
    award.save()

'''
@summary: Method that allows adding a bee to a list of those who Fly action performed
@param Bee: Object Type
@param id_bee_executor: type ObjectId
'''
def award_save_executor_fly_action(award, id_bee_executor):
    award.fly_refs.append(id_bee_executor)
    award.save()
    
    