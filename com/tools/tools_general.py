'''
Created on 19/06/2014

@author: palencia77
'''
import md5
import base64
import time
import datetime
import random
import smtplib
from com.__init__ import app_path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from wand.image import Image
import urllib2

def encrypt_password(password):
    m = md5.new()
    m.update(password)
    encrypt_password = m.digest()
    base64_password = base64.b64encode(encrypt_password)
    return base64_password

'''
@summary: Generator of string token
@return: token
@status: Validating
'''
def create_access_token():
    token= ""
    millis= int(round(time.time() * 1000)) #Time in milliseconds
    #print millis
    #Para que se usa un: Random r = new Random(millis); en java?
    longitud = random.randint(150, 500) #Integer beetween 150 and 500
    i= 0
    while (i < longitud):
        char = random.randint(0,255)
        if ((char >= 48 and char <= 57) or (char >= 65 and char <= 90) or (char >= 97 and char <= 122)):
            token += str(chr(char))
            i += 1
    return str(token)

'''
 @summary: method that allows you to send an email
 @param addresse: 
 @param issue:
 @param message:  
 '''
def send_email(address, subject, text_html):
    try:
        email_config = {}
        execfile(app_path + "/conf/properties/email.cfg", email_config)
        smtpserver = smtplib.SMTP(email_config["smtp_server"],email_config["smtp_port"])
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        message = MIMEMultipart()
        message['From'] = email_config["sender"]
        message['To'] = address
        message['Subject']= subject
        text = MIMEText(text_html, 'html')
        message.attach(text)
        smtpserver.login(email_config["sender"], email_config["password"])
        smtpserver.sendmail(email_config["sender"], address, message.as_string())
        smtpserver.close()
        return True
    except Exception as e:
        return e
'''
@summary: method that creates a short url given a long url
@param url (long): 
@return: short_url
'''    
def goo_shorten_url_bitly(url):
    get_url = 'https://api-ssl.bitly.com/v3/user/link_save'
    params = {'longUrl': url,'access_token' : '75a17462b6dfc1726fcaa03cabb6ff6f7d042cc1' }
    headers = {'content-type': 'application/json'}
    r = requests.get(get_url, headers=headers, params = params)
    rjson = r.json()
    return rjson['data']['link_save']['link']

'''
@summary: method that allows to remove spaces to a string
@param string: 
@return: string with spaces replaced by dashes
'''
def remove_spaces_string(string):
    string_replace = string.replace(" ", "-")
    return string_replace.lower()

'''
@summary: resize method to the size of an image and returns its new binary content
@param binary_content: String
@param width: Integer
@param height: Integer
@return: new_binary_content
@status: Tested (08/09/2014)
'''
def resize_image(binary_content, width, height):
    with Image(blob=binary_content) as image:
        image.resize(width,height)
        new_binary_content = base64.b64encode(image.make_blob())
        return new_binary_content
    
'''
@summary: resize method to the size of an image and returns its new binary content
@param binary_content: String
@param width: Integer
@param height: Integer
@return: new_binary_content
@status: Tested (18/09/2014)
'''
def resize_image_mobile(binary_content, width, height):
    with Image(blob=binary_content) as image:
        image.resize(width,height)
        new_binary_content = image.make_blob()
        return new_binary_content

'''
@summary: convert_image_from_url This method converts an image coming from a url in binary content
@param url: String
@param width: Integer
@param height: Integer
@return: data
@status: Tested (20/11/2014)
'''
def convert_image_from_url(url, width, height):
    data = {}
    with Image(file=urllib2.urlopen(url)) as image:
        image.resize(width,height)
        new_binary_content = base64.b64encode(image.make_blob())
        data['binary_content'] = new_binary_content
        data['name'] = "photo.jpg"
        data['text'] = "Upload From Social Network"
        data['content_type'] = "image/jpg"
        return data


'''
@summary: Generator of string password
@return: token
@status: Validating
'''
def generate_password():
    password= ""
    millis= int(round(time.time() * 1000)) #Time in milliseconds
    i= 0
    while (i < 10):
        char = random.randint(0,255)
        if ((char >= 48 and char <= 57) or (char >= 65 and char <= 90) or (char >= 97 and char <= 122)):
            password += str(chr(char))
            i += 1
    return str(password)

'''
@summary: crop method to the size of an image and returns its new binary content
@param binary_content: String
@param x: Integer
@param y: Integer
@param right: Integer
@param bottom: Integer
@return: new_binary_content
@status: Tested (02/12/2014)
'''
def crop_image(binary_content, x, y, right, bottom):
    with Image(blob=binary_content) as image:
        image.crop(x, y, width=right, height=bottom)
        new_binary_content = base64.b64encode(image.make_blob())
        return new_binary_content


'''
@summary: This method calculates a week this year required for ranking week
@param : None
@return: week
@status: Tested (11/12/2014)
'''
def week_number():
    week = 0
    week = datetime.datetime.now().isocalendar()[1]
    week_result = 0
    year = datetime.datetime.today().year
    if year % 4 == 0:
        if year % 100 == 0 and year % 400 != 0:
            if week == 1:
                week_result = datetime.datetime.now().isocalendar()[0]
            else:
                week_result = datetime.datetime.now().isocalendar()[0]-1
        else:
            if week == 1:
                week_result = datetime.datetime.now().isocalendar()[0]
            else:
                week_result = datetime.datetime.now().isocalendar()[0]-1
    else:
            if week == 1:
                week_result = datetime.datetime.now().isocalendar()[0]
            else:
                week_result = datetime.datetime.now().isocalendar()[1]-1

    return week_result

def get_year():
    year =datetime.datetime.now().year
    return year

def composing_date():
    compose_date= ("W")+str(week_number())+("-")+("Y")+str(get_year())
    return  compose_date
