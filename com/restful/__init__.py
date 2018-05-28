#-- FLASK APP:
from flask import Flask, redirect, url_for

services_app = Flask(__name__)

'''
Root core services url
@redirect to /ping
'''
@services_app.route('/')
def root():
    return redirect(url_for('ping'))


'''
Ping service for checking core service status
'''
@services_app.route('/ping', methods=['GET'])
def ping():
    data = {'message': 'pong'}
    return make_ok_response(data)


#-- RESTful SERVICES:
from com.restful.restful_security import *
from com.restful.restful_bee import *
from com.restful.restful_post import *
from com.restful.restful_comment import *
from com.restful.restful_operation import *
from com.restful.restful_scope import *
from com.restful.restful_notification import *
from com.restful.restful_suggestion import *
from com.restful.restful_cause import *
from com.restful.restful_partner import *
from com.restful.restful_celebrity import *
from com.restful.restful_resource import *
from com.restful.restful_tools import *
from com.restful.restful_award import *
from com.restful.restful_interaction import *

#-- THREADS:
#from com.services.threads.thread_security import *