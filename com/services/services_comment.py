'''
Created on 20/06/2014

@author: palencia77
'''
from com.data.models import *
from bson.objectid import ObjectId
from com.tools.objects_status import *

"""
@summary: Method to save a new Comment
@param text:
@param comment_owner:  
@param comment_parent: 
"""
def create_postcomment(text,comment_owner,comment_parent):
    comment = PostComment(text,owner=comment_owner, parent=comment_parent)
    comment.save()
    comment_parent.postcomment_refs.append(comment.id)
    comment_parent.save()
    return comment

'''
@summary: Method that remove of a comment
@param comment:
@return: True or Exception
'''
def remove_postcomment(comment):
    comment.status = STATUS_OBJECT_INACTIVE
    comment.save()
    
'''
@summary: Method that edit of a comment
@param comment:
@param text:
@return: True or Exception
'''
def edit_postcomment(comment,text):
    comment.text = text
    comment.save()

'''
@summary: Method seeking comments having a particular post
@param post:
@param with_resources:
@param page_number:
@param page_size: 
@status: result 
'''
def get_postcomments(post, page_number = 1, page_size = 3):
        result = {}
        paginate_result = Pagination(PostComment.objects.filter(parent=post, status=STATUS_OBJECT_ACTIVE).order_by('-created_date'),
                                     int(page_number), int(page_size))
        result['page_number'] = page_number
        result['page_size'] = page_size
        result['total_pages'] = paginate_result.pages
        result['total_elements'] = paginate_result.total
        result['content'] = paginate_result.items
        result['number_elements'] = len(paginate_result.items)
        result['first_page'] = not paginate_result.has_prev
        result['last_page'] = not paginate_result.has_next
        return result
    
'''
@summary: Method that get a comment by id
@param id_comment:
@return: Object Comment
'''     
def get_postcomment_by_id(id_comment):
    comment = PostComment.objects.get(id = ObjectId(id_comment))
    return comment


'''
@summary: Method increase love_counter in Comment
@param Object Comment
'''
def comment_love_counter_increase(Comment):
    Comment.love_counter = Comment.love_counter + 1
    Comment.save()
    
'''
@summary: Method that allows adding a bee to a list of those who love action performed 
@param comment: Object Type
@param id_bee_executor: type string
'''
def comment_save_executor_love_action(comment, id_bee_executor):
    comment.love_refs.append(id_bee_executor)
    comment.save()