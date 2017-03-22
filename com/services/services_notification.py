'''
Created on 26/06/2014

@author: palencia77
'''
from com.data.models import *
from bson.objectid import ObjectId

'''
@summary: Method that creates a notification
@param destination_bee: type object (Bee)
@param description: string
@param notification_type: type object (NotificationType)
'''
def create_notification_destination_bee(owner, bee_destination, description, notification_type):   
    notification = Notification(owner=owner, target=bee_destination, description=description, notification_type=notification_type)
    notification.save()
    
'''
@summary: Method that creates a notification
@param destination_bee: type object (Post)
@param description: string
@param notification_type: type object (NotificationType)
'''
def create_notification_destination_post(owner, target, post_destination, description, notification_type):   
    notification = NotificationPost(owner=owner, target=target, post_destination=post_destination, description=description, notification_type=notification_type)
    notification.save()
    
'''
@summary: Method that creates a notification
@param destination_post: type object (Comment)
@param description: string
@param notification_type: type object (NotificationType)
'''
def create_notification_destination_comment(owner, target, comment_destination, description, notification_type):   
    notification = NotificationComment(owner=owner, target=target, comment_destination=comment_destination, description=description, notification_type=notification_type)
    notification.save()
    
'''
@summary: Method that allows you to find the type of notification for codename
@param codename: attribute that enables a nickname for the type of notification
@return: Object object NotificationType 
'''
def get_notification_type(codename):
    notification_type = NotificationType.objects.get(codename=codename)
    return notification_type

'''
@summary: Method that allows you to find the type of notification for id
@param id_notification: 
@return: Object Notification
'''
def get_notification_by_id(id_notification):
    notification = Notification.objects.get(id=ObjectId(id_notification))
    return notification

'''
@summary: Method for querying a bee notifications
@param bee: type object (Bee)
@param notification_status: string
@param page_number: integer
@param page_size: integer
'''
def get_notifications_by_bee(bee, notification_status=None,  page_number=0, page_size=3):
        result = {}
        if notification_status is not None and notification_status != '':
            paginate_result = Pagination(Notification.objects.filter(target=bee, status=notification_status).order_by('-created_date'), int(page_number), int(page_size))
        else: 
            paginate_result = Pagination(Notification.objects.filter(target=bee).order_by('-created_date'), int(page_number), int(page_size))    
        
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
@summary: Method that allows to update the status of a notification
@param notification: type object (Notification)
@param status: string
'''    
def update_status_notification(notification, status):
    notification.status = status
    notification.save()

'''
@summary: Method to count notifications by status. If there is not status, then count all
@param bee_reader: type object (Bee)
@param notification_status: string
'''
def count_notifications_by_status(bee_reader, notification_status=None):
    if notification_status is not None and notification_status != '':
        notification_counter = len(Notification.objects.filter(target=bee_reader, status=notification_status).order_by('-created_date'))
    else:
        notification_counter = len(Notification.objects.filter(target=bee_reader).order_by('-created_date'))
    return notification_counter