'''
Created on 30/06/2014

@author: palencia77
'''
from com.data.models import *
import base64
from bson.objectid import ObjectId

'''
@summary: Method that generate a new scope
@param with_resource: Bool true or false
@param name, description, activation_date, closing_date, resource(optional)
@return: id_scope: The scope created
@status: Tested
'''
def register_scope(name, description, activation_date, closing_date, resource, with_resource,color):
    scope = Scope(name=name, description=description, activation_date=activation_date, closing_date=closing_date, color=color)
    scope.save()
    if (with_resource=='True'):
        logo = Resource(name=resource['name'],text=resource['text'],
                        binary_content=base64.b64decode(resource['binary_content']),
                        content_type=resource['content_type'])
        logo.save()
        scope.logo = logo
        scope.save()

    return scope.id

'''
@summary: Method that generate a new SubScope
@param with_resource: Bool true or false
@param name, description, activation_date, closing_date, scope_parent, resource(optional)
@return: id_SubScope: The SubScope created
@status: Tested
'''
def register_subscope(name, description, activation_date, closing_date, resource, scope_parent, with_resource):
    subscope = SubScope(name=name, description=description, activation_date=activation_date,
                        closing_date=closing_date, parent=scope_parent)
    subscope.save()
    if (with_resource== True):
        logo = Resource(name=resource['name'],text=resource['text'],
                            binary_content=base64.b64decode(resource['binary_content']),
                            content_type=resource['content_type'])
        logo.save()
        subscope.logo = logo
        subscope.save()
    return subscope.id

'''
@summary: Get a scope object by id
@param id_scope:
@return: Object Scope
'''
def get_scope_by_id(id_scope):
    scope = Scope.objects.get(id = ObjectId(id_scope))
    return scope


'''
@summary: Get a scope object by id
@param id_scope:
@return: Object Scope
'''
def get_subscope_by_id(id_subscope):
    subscope = SubScope.objects.get(id=ObjectId(id_subscope))
    return subscope


'''
@summary: Get scopes objects
@param page_number:
@param page_size
@return: result
'''
def get_scopes(name_filter, status,page_number = 1, page_size = 3):
    result = {}
    paginate_result = Pagination(Scope.objects(_cls='Scope',name__icontains=name_filter,status=status).order_by('-creation_date'),int(page_number),int(page_size))
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
@summary: Get sub-scopes objects by id_scope
@param scope: Object(scope)
@return: sub_scopes: Objects (Sub_Scope)
'''
def get_sub_scopes_by_scope(scope,name_filter,status, page_number = 1, page_size = 3):
    result = {}
    paginate_result = Pagination(SubScope.objects(parent = scope,name__icontains=name_filter,status=status),int(page_number),int(page_size))
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
@summary: Method that remove a subscope
@param id_subscope:
@return: True or Exception
'''
def remove_subscope_by_id(id_subscope):
    try:
        subscope = SubScope.objects.get(id = ObjectId(id_subscope))
        subscope.delete()
        return True
    except Exception as e:
        return e

'''
@summary: Method that remove a scope
@param id_scope:
@return: True or Exception
'''
def remove_scope_by_id(id_scope):
    try:
        scope = get_scope_by_id(id_scope)
        sub_scopes = get_sub_scopes_by_scope(scope)
        for sub_scope in sub_scopes:
            sub_scope.delete()
        scope.delete()
        return True
    except Exception as e:
        return e

'''
@summary: Method that update a scope
@param with_resource: Bool true or false
@param scope, name, description, activation_date, closing_date, resource(optional)
@return: True or exception
@status: Tested 27/07/2014
'''
def update_scope(scope, name, description, activation_date, closing_date, resource, with_resource, color):
    try:
        scope.name = name
        scope.description = description
        scope.activation_date = activation_date
        scope.closing_date = closing_date
        scope.color = color
        scope.save()
        if (with_resource=='True'):
            logo = Resource(name=resource['name'],text=resource['text'],
                            binary_content=base64.b64decode(resource['binary_content']),
                            content_type=resource['content_type'])
            logo.save()
            scope.logo = logo
            scope.save()
        return True
    except Exception as e:
        return e

'''
@summary: Method that update a scope
@param with_resource: Bool true or false
@param scope, name, description, activation_date, closing_date, resource(optional)
@return: True or exception
@status: Tested 27/07/2014
'''
def update_subscope(subscope, scope, name, description, activation_date, closing_date, resource, with_resource):
    try:
        subscope.name = name
        subscope.parent = scope
        subscope.description = description
        subscope.activation_date = activation_date
        subscope.closing_date = closing_date
        subscope.save()
        if (with_resource== True):
            logo = Resource(name=resource['name'],text=resource['text'],
                            binary_content=base64.b64decode(resource['binary_content']),
                            content_type=resource['content_type'])
            logo.save()
            subscope.logo = logo
            subscope.save()
        return True
    except Exception as e:
        return e

'''
@summary: Method that update status of a scope
@param scope: object
@return: True or Exception
@status:
'''
def scope_update_status(scope,status):
    scope.status = status
    scope.save()
    return True


'''
@summary: Method that update status of a scope
@param scope: object
@return: True or Exception
@status:
'''
def subscope_update_status(subscope, status):
    subscope.status = status
    subscope.save()
    return True