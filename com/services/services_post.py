'''
Created on 20/06/2014

@author: palencia77
'''
from com.data.models import *
from com.services.services_resource import *
from com.services.services_comment import *
from bson.objectid import ObjectId
from com.tools.objects_status import *

"""
@summary: Method to save a new Post
@param bee: 
@param tilte: 
@param text: 
@param with_resource:
@param resources: 
@return id_post
@status: update 06/08/2014
"""
def create_post(bee,title,text,with_resource,resources):
    post=Post(title=title,text=text,owner=bee)
    post.save()
    #Saving the resources if exists:
    if (with_resource =="True"):
        for resource in resources:
            create_resource_in_post(post,bee,resource)
    return post

'''
@summary: Method that remove of a post
@param post: 
@status: validating 
'''
def remove_post (post):
    try:
        post.status= STATUS_OBJECT_INACTIVE
        post.save()
    except Exception as e:
        return e     

'''
@summary: Method that update text of a post
@param post: 
@status: validating 
'''
def update_text_post (post,text):
    try:
        post.text= text
        post.save()
    except Exception as e:
        return e  
    
'''
@summary: Method that get a post by id
@param id_post:
@return: Object Post
'''     
def get_post_by_id(id_post):
    post = Post.objects.get(id = ObjectId(id_post), status=STATUS_OBJECT_ACTIVE)
    return post 

'''
@summary: Method to get the existence of a post
@param id_post:
@return: True or False
'''     
def there_is_post(id_post):
    post = Post.objects.get(id = ObjectId(id_post))
    if post is not None:
        return True
    else: return False
    
'''
@summary: Method increase love_counter in  post
@param Object Post:
'''       
def post_love_counter_increase(post):
    post.love_counter = post.love_counter + 1
    post.save()      
    
'''
@summary: This method get paged publications
@param id_bee:
@param page_number: Number of the page to return
@param page_size: Number of publications per page
@return: json data
'''      
def get_posts(id_bee,page_number=1,page_size=10):
    result = {}
    paginate_result = Pagination(Post.objects.filter(owner = id_bee, status=STATUS_OBJECT_ACTIVE).order_by('-created_date'), int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] =  paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    result['last_page'] = not paginate_result.has_next
    return result

'''
@summary: This method get paged timeline publications of bee
@param id_bee:
@param page_number: Number of the page to return
@param page_size: Number of publications per page
@return: json data
'''
def get_timeline(bee, page_number=1, page_size=10):
    result = {}
    paginate_result = Pagination(Post.objects(status=STATUS_OBJECT_ACTIVE).order_by('-created_date'), int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] = paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    result['last_page'] = not paginate_result.has_next
    return result
    
'''     
@summary: this method that allows to adding a bee to a list of those who FLY action performed 
@param post:
@param id_be_executor:      
'''   
def post_save_executor_love_action(post, id_bee_executor):   
    post.love_refs.append(id_bee_executor)
    post.save()
    
'''
@summary: this method that allows to adding a bee to a list of those who FLY action performed 
@param post:
@param id_be_executor:      
'''
def post_add_fly_refs(post,id_bee_executor):
    post.fly_refs.append(id_bee_executor)
    post.save()
    
'''
@summary: Method increase fly_counter in  post
@param Object Post:
'''       
def post_fly_counter_increase(post):
    post.fly_counter += 1
    post.save()   

"""
@summary: Method to update a Post
@param post:
@param tilte: 
@param text: 
@param resources_to_remove:
@param resources_to_add: 
@status: tested 14/08/2014
"""
def update_post(post, title, text):
    post.title = title
    post.text = text
    post.save()
    return post.id
  