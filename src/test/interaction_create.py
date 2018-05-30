'''
Created on 04/07/2014

@author: palencia77
'''
import json
import requests
from com.data.models import *

#Test configuration------------------------------------------------------------
global_login = 'admin' #Required
global_password = '19104894' #Required
global_app = "BACKEND"
#------------------------------------------------------------------------------

#===============================================================================
InteractionType(codename='ITCA', name='Interaction on Cause').save()
InteractionType(codename='ITAW', name='Interaction on Award').save()
InteractionType(codename='ITPOCA', name='Interaction on Cause Post').save()
InteractionType(codename='ITCOCA', name='Interaction on Cause Comment').save()
InteractionType(codename='ITPOCE', name='Interaction on Celebrity Post').save()
InteractionType(codename='ITCOCE', name='Interaction on Celebrity Comment').save()
InteractionType(codename='ITPOPA', name='Interaction on Partner Post').save()
InteractionType(codename='ITCOPA', name='Interaction on Partner Comment').save()
InteractionType(codename='ITPOBEE', name='Interaction on Bee Post').save()
InteractionType(codename='ITCOBEE', name='Interaction on Bee Comment').save()
#===============================================================================

#We get a new access token
data = {}
data['login'] = global_login
data['password'] = global_password
data['app'] = global_app

result = requests.post("http://localhost:5000/user/validate", data=json.dumps(data))
validate_result = result.json()
if 'access_token' in validate_result:
    print "access_token: " + validate_result['access_token']

    ##################################################################
    #LOVE OPERATIONS
    ##################################################################

    #We get a new access token
    data = {}
    data['codename'] = "ITCA"
    data['name'] = "LOVE"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITPOCA"
    data['name'] = "LOVE"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITCOCA"
    data['name'] = "LOVE"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITPOCE"
    data['name'] = "LOVE"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITCOCE"
    data['name'] = "LOVE"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITPOPA"
    data['name'] = "LOVE"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITCOPA"
    data['name'] = "LOVE"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITPOBEE"
    data['name'] = "LOVE"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITCOBEE"
    data['name'] = "LOVE"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    ##################################################################
    #FLY OPERATIONS
    ##################################################################

    #We get a new access token
    data = {}
    data['codename'] = "ITCA"
    data['name'] = "FLY"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITPOCA"
    data['name'] = "FLY"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITCOCA"
    data['name'] = "FLY"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITPOCE"
    data['name'] = "FLY"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITCOCE"
    data['name'] = "FLY"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITPOPA"
    data['name'] = "FLY"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITCOPA"
    data['name'] = "FLY"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITPOBEE"
    data['name'] = "FLY"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITCOBEE"
    data['name'] = "FLY"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()

    #We get a new access token
    data = {}
    data['codename'] = "ITAW"
    data['name'] = "FLY"
    data['access_token'] = validate_result['access_token']

    result = requests.post("http://localhost:5000/interaction/create", data=json.dumps(data))
    print ""
    print "==TEST RESULT FOR CREATE INTERACTION=="
    print "=============================="
    print result.json()
