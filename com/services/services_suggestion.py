'''
Created on 01/07/2014

@author: palencia77
'''
from datetime import timedelta,datetime
from com.data.models import *
from bson.objectid import ObjectId

'''
@summary: Method that returns paginated causes suggested of a bee
@param bee:
@param page_number:
@param page_size:  
@return: Suggested causes
@status: Tested
'''
def get_suggested_causes(bee,page_number=1,page_size=10):
    result = {}
    paginate_result = []
    paginate_result = Pagination(Cause.objects.filter(id__nin = bee.bee_refs), int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items #List of causes
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method that returns paginated bee's person suggested of a bee
@param bee:
@param page_number:
@param page_size:  
@return: Suggested bee's person
@status: Tested
'''
def get_suggested_persons(bee,page_number=1,page_size=10):
    result = {}
    paginate_result = []
    paginate_result = Pagination(Person.objects.filter(id__nin = bee.bee_refs), int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items #List of causes
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method that returns paginated celebrities suggested of a bee
@param bee:
@param page_number:
@param page_size:  
@return: Suggested celebrities
@status: Tested
'''
def get_suggested_celebrities(bee,page_number=1,page_size=10):
    result = {}
    paginate_result = []
    paginate_result = Pagination(Celebrity.objects.filter(id__nin = bee.bee_refs), int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items #List of causes
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method that returns paginated partners suggested of a bee
@param bee:
@param page_number:
@param page_size:  
@return: Suggested celebrities
@status: Tested
'''
def get_suggested_partner(bee,page_number=1,page_size=10):
    result = {}
    paginate_result = []
    paginate_result = Pagination(Partner.objects.filter(id__nin = bee.bee_refs), int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items #List of causes
    result['number_elements'] = len(paginate_result.items)
    return result