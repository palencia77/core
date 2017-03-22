'''
Created on 19/06/2014

@author: palencia77
'''
import re
from datetime import timedelta
from com.data.models import *
from com.tools.tools_general import *
from flask import render_template
from bson.objectid import ObjectId
from com.tools.email_subjects import *
from com.tools.token_types import *
from com.tools.project_paths import *
from com.tools.app_types import *
from com.tools.objects_status import *
from com.services.services_resource import *
from com.services.services_bee import bee_update_status, get_bee_by_owner

'''
@summary: Method that return token by access_token
@param access_token:
'''
def get_token_by_access_token(access_token):
    token = Token.objects.get(access_token=access_token)
    return token

'''
@summary: Method that get a user by they token access
@param access_token:
@return: Object user
'''
def get_user_by_token(access_token):
    token = Token.objects.get(access_token=access_token)
    return token.owner

'''
@summary: Method that validates a user's credentials
@param login:
@param password: 
@param app: ("MOBILE", "BACKEND", "LANDINGPAGE")
@return: String access_token
'''   
def validate_credentials(login, password, app):
    status = [STATUS_OBJECT_ACTIVE, STATUS_OBJECT_PENDING, STATUS_OBJECT_SUSPENDED]
    user_result = User.objects.filter(login=login, status__in=status)
    if user_result.count() <= 0:
        raise Exception('Username or password incorrect')
    user = user_result[0]
    if user.password != encrypt_password(password):
        raise Exception('Username or password incorrect')
    if user.status == STATUS_OBJECT_SUSPENDED:
        # Send the email with a link to activate the bee account:
        activate_token = generate_token(user, ACCESS_TOKEN_ACTIVATE_ACCOUNT)
        url_email = SOCIAL_PATH + "/user/activate/account?access_token=" + str(activate_token.access_token)
        #short_url=  goo_shorten_url_bitly(url)
        data = {'url': url_email, 'user': user}
        subject_html = SUBJECT_BEE_ACTIVATE_ACCOUNT
        text_html = render_template('email/bee_activate_account.html', data=data)
        send_email(user.email, subject_html, text_html)
        raise Exception('You can not access until you activate your account, please check your email tray')
    if app == APP_MOBILE and user.type == USER_FRONTEND:
        token = generate_token(user, ACCESS_TOKEN_MOBILE)  
    elif app == APP_BACKEND and user.type == USER_BACKEND:
        token = generate_token(user, ACCESS_TOKEN_OPERATION)        
    elif (app == APP_LANDING or app == APP_SOCIAL) and user.type == USER_FRONTEND:
        token = generate_token(user, ACCESS_TOKEN_OPERATION)        
    else:
        raise Exception('Incorrect user credentials')
    return {'access_token': token.access_token}

'''
@summary: Method that validates a user from social networks
@param login:
@param app: ("MOBILE", "BACKEND", "LANDINGPAGE")
@param id_social_network:
@param image_social_network:
@return: String access_token
'''   
def validate_user_from_social_network(login, app, network_name, id_social_network,image_social_network):
    user = User.objects.filter(login=login, type=USER_FRONTEND)
    data ={}
    if user.count() > 0:
        user_object = user[0]
        if user_object.status == STATUS_OBJECT_INACTIVE:
            user_update_status(user_object, STATUS_OBJECT_ACTIVE)
            bee = get_bee_by_owner(user_object)
            bee_update_status(bee, STATUS_OBJECT_ACTIVE)
        if str(network_name) not in user_object.id_social_network:
            user_object.id_social_network[str(network_name)] = str(id_social_network)
            user_object.save()       
        if app == APP_MOBILE:
            token = generate_token(user_object, ACCESS_TOKEN_MOBILE)
        else:
            token = generate_token(user_object, ACCESS_TOKEN_OPERATION)    
        data["access_token"] = token.access_token
        return data
    else:
        return None

'''
@summary: Method that creates a token and associates it with an user
@param user:
@return: Object token
'''    
def generate_token(user, type):
    token = Token(owner=user)
    token.access_token = create_access_token()
    start_date = token.start_date
    if type == ACCESS_TOKEN_OPERATION:
        delta = timedelta(days=1)
        token.type = ACCESS_TOKEN_OPERATION        
    elif type == ACCESS_TOKEN_RECOVER_PASSWORD:
        delta = timedelta(days=1)
        token.type = ACCESS_TOKEN_RECOVER_PASSWORD        
    elif type == ACCESS_TOKEN_MOBILE:
        delta = timedelta(days=365)
        token.type = ACCESS_TOKEN_MOBILE
    elif type == ACCESS_TOKEN_ACTIVATE_ACCOUNT:
        delta = timedelta(days=2)
        token.type = ACCESS_TOKEN_ACTIVATE_ACCOUNT
    elif type == ACCESS_TOKEN_INACTIVATE_ACCOUNT:
        delta = timedelta(days=1)
        token.type = ACCESS_TOKEN_INACTIVATE_ACCOUNT
    token.finish_date = token.start_date + delta
    token.save()
    return token

'''
@summary: service that receives the data to register a new user
@param: login
@param password:
@param email: 
@param full_name
@param gender: 
@param type_user
@param app:
@image_social_network_url:
@return 
'''
def register_user(login, password, email, full_name, gender, birthday, type_user, app,
                  phone, avatar, from_social_network=False, id_social_network=None,
                  network_name=None, image_social_network_url=None):
    if from_social_network is True:
        user = User(login=login, email=email, full_name=full_name, type=type_user, gender=gender)
        user.id_social_network[network_name] = id_social_network
        user_status = STATUS_OBJECT_ACTIVE
        user.save()
    else:  # The new user did not make a social login:
        # Validate the birthday:
        if birthday is not None:
            user_birthday = datetime(*map(int, re.split('[^\d]', str(birthday))[:-1]))
        else:
            user_birthday = None
        # Creating the user object:
        user = User(login=login, password=encrypt_password(password), email=email, full_name=full_name,
                    gender=gender, type=type_user, birthday=user_birthday, phone=phone)
        # Determinate the status of the user:
        if user.type == USER_BACKEND:
            user_status = STATUS_OBJECT_ACTIVE
        else:
            user_status = STATUS_OBJECT_PENDING
    # Save the user status:
    user.status = user_status
    user.save()
    # Validating the avatar:
    if avatar is not None:
        create_resource_user(user, avatar, "avatar")

    # Validating the app type:
    if app == APP_MOBILE:
        token = generate_token(user, ACCESS_TOKEN_MOBILE)
    else:
        token = generate_token(user, ACCESS_TOKEN_OPERATION)

    # Validating the user type to generate a bee person object:
    bee = None
    if user.type == USER_FRONTEND:
        bee = Person(name=user.full_name, owner=user)
        bee.save()
        #Saving the short ulr of the bee
        short_url = goo_shorten_url_bitly(PERSON_URL_BASE+str(bee.id))
        bee.short_url = short_url
        bee.save()
        user.parameters['id_bee'] = bee.id
        user.save()

    # Validating if its necessary send the mechanism to activate the account:
    if from_social_network is True:
        # Send the email without a link to activate the bee account:
        data = {'user': user}
        subject_html = SUBJECT_BEE_SOCIAL_REGISTER
        text_html = render_template('email/bee_social_register.html', data=data)
        send_email(user.email, subject_html, text_html)
        data_image = convert_image_from_url(image_social_network_url, 200, 200)
        create_resource_bee(bee, data_image, "avatar")
    elif user.type == USER_FRONTEND:
        # Send the email with a link to activate the bee account:
        activate_token = generate_token(user, ACCESS_TOKEN_ACTIVATE_ACCOUNT)
        url = SOCIAL_PATH + "/user/activate/account?access_token=" + str(activate_token.access_token)
        #short_url=  goo_shorten_url_bitly(url)
        data = {'url': url, 'user': user}
        subject_html = SUBJECT_BEE_REGISTER
        text_html = render_template('email/bee_register.html', data=data)
        send_email(user.email, subject_html, text_html)

    # Return the data:
    data = {}
    data["access_token"] = token.access_token
    data["login"] = login
    data["full_name"] = user.full_name
    data["email"] = user.email
    data["id_user"] = user.id
    if bee is not None:
        data["id_bee"] = bee.id
    return data

'''
@summary: Method that created resources in user
@param user:
@param resource: 
@status: in process
'''
def create_resource_user(user, resource, *key):
    resource = Resource(name=resource['name'], text=resource['text'],
                        binary_content=base64.b64decode(resource['binary_content']),
                        content_type=resource['content_type'])
    resource.save()
    user.parameters[str(key[0])]=resource.id
    user.save()       
    return resource

'''
@summary: Method that validates the token expiration
@param access_token:
'''
def validate_token(access_token):
    token = Token.objects.get(access_token=access_token)
    if datetime.now() > token.finish_date or token.type != ACCESS_TOKEN_OPERATION or token.status == "INVALID":
        raise Exception('SESSIONEXPIRED')

'''
@summary: Method that validates the token expiration for mobile
@param access_token:
'''
def validate_token_mobile(access_token):
    token = Token.objects.get(access_token=access_token)
    if datetime.now() > token.finish_date or token.type != ACCESS_TOKEN_MOBILE or token.status == "INVALID":
        raise Exception('Invalid Token')
    
'''
@summary: Method that validates the token expiration for recover password
@param access_token:
'''
def validate_token_recover_password(access_token):
    token = Token.objects.get(access_token=access_token)
    if datetime.now() > token.finish_date or token.type != ACCESS_TOKEN_RECOVER_PASSWORD or token.status == "USED":
        raise Exception('Invalid Token')

'''
@summary: Method that validates the token expiration for activate a bee account
@param access_token:
'''
def validate_token_activate_account(access_token):
    token = Token.objects.get(access_token=access_token)
    if datetime.now() > token.finish_date or token.type != ACCESS_TOKEN_ACTIVATE_ACCOUNT or token.status == "USED":
        raise Exception('The token has expired')

'''
@summary: Method that validates the token expiration for inactivate a bee account
@param access_token:
'''
def validate_token_inactivate_account(access_token):
    token = Token.objects.get(access_token=access_token)
    if datetime.now() > token.finish_date or token.type != ACCESS_TOKEN_INACTIVATE_ACCOUNT or token.status == "USED":
        raise Exception('The token has expired')

'''
@summary: Method that allows change the password of an user
@param user:
@param old_password: 
@param new_password: 
'''
def user_update_password(user, old_password, new_password):
    old_encrypted_password = encrypt_password(old_password) 
    password = user.password
    if password != old_encrypted_password:
        raise Exception('Passwords do not match')
    else:
        user.password = encrypt_password(new_password)
        user.save()
        
'''       
@summary: Method that allows update user
@param user
@param gender
@param full_name
@param birthday
@return: user    
'''
def user_update(user, gender, full_name, birthday):
    user.gender = gender
    user.full_name = full_name
    user.birthday = birthday
    user.save()
'''       
@summary: Method that allows update user
@param user
@param resource Object
@return: user Object   
'''
def user_avatar_update(user,resource):
    user.parameters['id_avatar']=resource.id
    user.save()
    return user

'''       
@summary: Method that allows update cover of user
@param user
@param resource Object
@return: user Object   
'''
def user_cover_update(user,resource):
    user.parameters['id_cover'] = resource.id
    user.save()
    return user             

'''       
@summary: Method that get an user by id
@param id_user: login
@return: user Object 
'''
def get_user_by_id(id_user):
    user = User.objects.get(id=ObjectId(id_user))
    return user

'''       
@summary: Method that get an user by login
@param login: 
@return: user Object 
'''
def get_user_by_login(login):
    user = User.objects.get(login=login)
    return user

'''       
@summary: Validates that the login is not registered
@param login:
@return: An exception if the login exists
'''
def validate_uniqueness_login(login, app):
    user = User.objects.filter(login=login)
    if user.count() > 0:
        if app == APP_SOCIAL:
            recover_password(user[0], APP_SOCIAL)
            raise Exception('Tu cuenta ya existe, te hemos enviado un correo para recuperar tu clave')
        else:
            raise Exception('El login ya existe')
            
    
'''
@summary: Method seeking paginated users belonging to status and name_filter
@param status: 
@param name_filter:    
@status: Tested 02/09/2014
''' 
def get_all_user_paginated(status, name_filter, type_user, page_number, page_size):
    result = {}
    if status is None:
        user = User.objects
    else:        
        user = User.objects(full_name__icontains=name_filter, status = status, type=type_user)
    paginate_result = Pagination(user, int(page_number), int(page_size))
    result['page_number'] = page_number
    result['page_size'] = page_size 
    result['total_elements'] = paginate_result.total
    result['total_pages'] = paginate_result.pages
    result['content'] = paginate_result.items
    result['number_elements'] = len(paginate_result.items)
    return result

'''
@summary: Method that update a user
@param user:
@param email:
@param full_name:
@param gender:
@param birthday:
@param phone:
@param avatar:
@status: tested 04/09/2014
'''
def update_user(user, email, full_name, gender, birthday, phone, avatar):
    try:
        user_birthday = datetime(*map(int, re.split('[^\d]', str(birthday))[:-1]))
        user.email = email
        user.full_name = full_name
        user.gender = gender
        user.phone = phone
        user.birthday = user_birthday
        user.save()
        if avatar is not None:
            create_resource_user(user,avatar,"avatar")
        return True
    except Exception as e:
        return e

'''
@summary: Method that update status of a user
@param user: object
@param status:
@return: True or Exception
@status: Tested 08/08/2014
'''  
def user_update_status(user, status):
    user.status = status
    user.status_date = datetime.now
    user.save()
    return True

'''
@summary: Method that find users by their status
@param status:
@return: user list or Exception
@status: Tested 11/11/2014
'''
def get_user_by_status(status):
    users = User.objects.filter(status=status)
    if users.count() > 0:
        return users
    else:
        return None

'''
@summary: Method that find users by status on a time interval
@param status:
@param hours_time: Time in hours
@return: user list or Exception
@status: Tested 11/11/2014
'''
def get_user_by_status_and_status_date_interval(status, hours_time):
    delta = timedelta(hours=hours_time)
    users = User.objects.filter(status=status, status_date__lt=datetime.now()-delta)
    if users.count() > 0:
        return users
    else:
        return None

'''
@summary: Method which lets you get the user to send mail to retrieve your password
@param user:
@param app:
'''
def recover_password(user, app):
    token = generate_token(user, ACCESS_TOKEN_RECOVER_PASSWORD)
    if app == APP_SOCIAL:
        url = SOCIAL_PATH + "/user/recover/update/password?access_token=" + str(token.access_token)
    elif app == APP_BACKEND:
        url = BACKEND_PATH + "/user/recover/update/password?access_token=" + str(token.access_token)
    #short_url=  goo_shorten_url_bitly(url)
    data = {'url': url, 'user': user}
    text_html = render_template('email/user_recover_password.html', data=data)
    subject_html = SUBJECT_RECOVER_PASSWORD
    send_email(user.email, subject_html, text_html)
    
'''
@summary: Method which lets you get the user to send mail to retrieve your password
@param user:
@param app:
'''
def send_confirmation_to_inactivate_account(user):
    inactivate_token = generate_token(user, ACCESS_TOKEN_INACTIVATE_ACCOUNT)
    url = SOCIAL_PATH + "/user/inactivate/account?access_token=" + str(inactivate_token.access_token)
    #short_url=  goo_shorten_url_bitly(url)
    data = {'url': url, 'user': user}
    subject_html = SUBJECT_BEE_INACTIVATE_ACCOUNT
    text_html = render_template('email/bee_inactivate_account.html', data=data)
    send_email(user.email, subject_html, text_html)
    raise Exception('We have sent an email with a link that lets you deactivate your account')
    
    
    
'''
@summary: Method that allows update the password of an user
and used to update the state of the token
@param user:
'''
def recover_password_update_data(user, password, access_token):
    new_password = encrypt_password(password)
    user.password = new_password
    user.save()
    token_update_status(access_token, "USED")
 
'''
@summary: Method that update the state of the token
@param access_token:
@param status:
'''   
def token_update_status(access_token, status):
    token = get_token_by_access_token(access_token)
    token.status = status
    token.save()
    
'''
@summary: Method that update the specific field on a user
@param id_user: field
@param value:
@return: True or Exception
@status: Tested 24/11/2014
'''
def user_update_attribute(id_user, field, value):
    User._get_collection().update({"_id": ObjectId(id_user), "status": "ACTIVE"},{"$set": { field: value }})

'''
@summary: Method to validate that a bee is the owner of the token
@param access_token: String
@param id_bee:
@return: True or Exception
@status: Tested 27/11/2014
'''
def validate_token_owner(access_token, id_bee):
    user = get_user_by_token(access_token)
    if str(user.parameters['id_bee']) != str(id_bee):
        raise Exception('You do not have permission to perform this operation')
    return True