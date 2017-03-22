'''
Created on 22/10/2014

@author: palencia77
'''
from flask import request
from flask import json
from com.restful.__init__ import services_app
from com.services.services_security import *
from com.tools.tools_response import *
from com.tools.tools_general import send_email

    
'''
@summary: Service to send a email from com
@param access_token:
@param address:
@param subject:
@param text:
@return: json ok or error
@status: tested 22/10/2014
'''
@services_app.route('/tools/send_mail', methods=['POST'])
def restful_tools_send_mail():
    data = {}
    try:
        data = json.loads(request.data)
        access_token = data['access_token']
        validate_token(access_token)
        #Validating the params:
        if data['address'] is not None and data['subject'] is not None and data['text'] is not None:
            result = send_email(data['address'], data['subject'], data['text'])
            if result is True:
                data = {}
                data['message'] = 'ok'
                return make_template_response(data, 'ok.json')
            else:
                raise Exception(result)
        else:
            raise Exception('You must provide all data of of the email')
    except Exception as e:
        data = {}
        data['error'] = e
        return make_template_response(data, 'error.json')