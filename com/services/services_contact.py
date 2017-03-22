'''
Created on 08/07/2014

@author: palencia77
'''
from flask import request
from com.restful.__init__ import services_app
from com.data.models import *
from bson.objectid import ObjectId
from com.services.services_resource import *

'''
@summary: Method that save a new contact
@param name, email, mobile_phone, telephone, address, organization
@return: id_contact: The contact created
@status: Tested
'''
def register_contact(name, email,mobile_phone, telephone, address, organization):
    contact= Contact(name=name, email=email, mobile_phone=mobile_phone, telephone=telephone,address=address,organization=organization)
    contact.save()
    return contact.id

'''
@summary: Method update a contact
@param contact, name, email,mobile_phone, telephone, address, organization
@status: Tested
'''
def update_contact(contact, name, email,mobile_phone, telephone, address, organization):
    contact.name = name
    contact.email = email
    contact.mobile_phone = mobile_phone
    contact.telephone = telephone
    contact.address = address
    contact.organization = organization    
    contact.save()

'''
@summary: Method that get a contact by id
@param id_contact
@return: contact object
@status: Tested
'''  
def get_contact_by_id(id_contact):
    contact = Contact.objects.get(id = ObjectId(id_contact))
    return contact