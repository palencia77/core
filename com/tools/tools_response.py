'''
Created on 19/06/2014

@author: palencia77
'''
from flask.helpers import make_response
from flask import render_template

def make_template_response(response_data, template_name):
    response = make_response()
    response.content_type = 'application/json'
    response.data = render_template(template_name, data=response_data, mimetype='application/json') 
    return response

def make_ok_response(response_data):
    response = make_response()
    response.content_type = 'application/json'
    response.data = render_template('general/ok.json', data=response_data, mimetype='application/json') 
    return response

def make_error_response(response_data):
    response = make_response()
    response.content_type = 'application/json'
    response.data = render_template('general/error.json', data=response_data, mimetype='application/json') 
    return response
