'''
Created on 19/06/2014

@author: palencia77
'''
from datetime import datetime
from mongoengine import *
from com.__init__ import *
from mongoengine import queryset_manager
from com.tools.objects_status import *


class User(db.Document):
    login = db.StringField()
    facebook_id = db.StringField()
    id_social_network = db.DictField()
    image_social_network = db.DictField()
    password = db.StringField()
    email = db.EmailField(required=True)
    full_name = db.StringField(max_length=50)
    gender = db.StringField(max_length=50)
    status = db.StringField(default=STATUS_OBJECT_PENDING)
    status_date = db.DateTimeField(default=datetime.now)
    parameters = db.DictField()  # id_bee, avatar
    birthday = db.DateTimeField()
    phone = db.StringField(max_length=50, default='00000000')
    created_date = db.DateTimeField(default=datetime.now)
    type = db.StringField()


class Token(db.Document):
    owner = db.ReferenceField(User)
    access_token = db.StringField(max_length=500, required=True)
    start_date = db.DateTimeField(default=datetime.now)
    finish_date = db.DateTimeField()
    type = db.StringField(required=True)
    status = db.StringField(default=STATUS_TOKEN_VALID)


class Bee(db.Document):
    name = db.StringField(required=True)
    owner = db.ReferenceField(User)
    post_counter = db.IntField(default=0)  # Count Post
    love_counter = db.IntField(default=0)  # Count Love Action 
    love_refs = db.ListField()  # Referencias a los bee que hicieron acton love
    resource_refs = db.ListField()  # Referencias a los Id de Recursos
    created_date = db.DateTimeField(default=datetime.now)
    status = db.StringField(default=STATUS_OBJECT_PENDING)
    status_date = db.DateTimeField(default=datetime.now)
    bee_blocked_refs = db.ListField()  # blacklist
    administrators_refs = db.ListField()  # Referencias a los administradores del bee
    parameters = db.DictField()  # avatar,cover,promotional_photo,promotional_video,document
    short_url = db.StringField()
    current_status = db.StringField(default='Mi estado actual')  # Referente al estado actual en la red social
    meta = {'allow_inheritance': True}


class Award(db.Document):
    title = db.StringField()
    text = db.StringField()
    owner = db.ReferenceField(Bee)
    resource_refs = db.ListField()  # Referencias a los Id de Recursos
    quantity = db.IntField(default=0)  # Cantidad de premio
    created_date = db.DateTimeField(default=datetime.now)
    amount_love = db.IntField(default=0)
    fly_refs = db.ListField()
    fly_counter = db.IntField(default=0)  # Contador de Fly recibidos
    status = db.StringField(default=STATUS_OBJECT_ACTIVE)


class Person(Bee):
    love_score = db.IntField(default=0)  # Love Organico para donar en la Red
    love_coin = db.IntField(default=0)
    bee_refs = db.ListField()  # Referencias a Bee que sigue
    sub_scope_refs = db.ListField()  # Referencias a id de los SubAmbitos que sigue el bee
    awards_refs = db.ListField(db.ReferenceField(Award))  # Id de los premios obtenidos (por canje).


class Celebrity(Bee):
    email = db.EmailField()
    description = db.StringField()
    telephone = db.StringField(max_length=50, default='00000000')
    web_site = db.StringField()
    facebook = db.StringField()
    twitter = db.StringField()
    google_plus = db.StringField()
    address = db.StringField()


class Partner(Bee):
    email = db.EmailField()
    description = db.StringField()
    telephone = db.StringField(max_length=50, default='00000000')
    web_site = db.StringField()
    address = db.StringField()
    facebook = db.StringField()
    twitter = db.StringField()
    google_plus = db.StringField()


class Post(db.Document):
    title = db.StringField()
    text = db.StringField(required=True)
    owner = db.ReferenceField(Bee)
    love_counter = db.IntField(default=0)  # Contador de Love Recibidos
    love_refs = db.ListField()
    fly_refs = db.ListField()
    postcomment_refs = db.ListField()  # Referencias a los Id de PostComments
    resource_refs = db.ListField()  # Referencias a los Id de Recursos
    fly_counter = db.IntField(default=0)  # Contador de Fly recibidos
    created_date = db.DateTimeField(default=datetime.now)
    status = db.StringField(default=STATUS_OBJECT_ACTIVE)


class PostComment(db.Document):
    text = db.StringField(required=True)
    owner = db.ReferenceField(Bee)
    parent = db.ReferenceField(Post)
    love_counter = db.IntField(default=0)  # Es necesario para un comentario?
    love_refs = db.ListField()
    created_date = db.DateTimeField(default=datetime.now)
    status = db.StringField(default=STATUS_OBJECT_ACTIVE)


class Resource(db.Document):
    name = db.StringField(required=True)
    image = db.ImageField()
    text = db.StringField(required=True)
    binary_content = db.BinaryField()
    content_type = db.StringField()
    owner = db.ReferenceField(Bee)
    post = db.ReferenceField(Post)
    award = db.ReferenceField(Award)
    love_counter = db.IntField(default=0)  # Contador de Love Recibidos
    love_refs = db.ListField()
    created_date = db.DateTimeField(default=datetime.now)
    status = db.StringField(default=STATUS_OBJECT_ACTIVE)


class ResourceComment(db.Document):
    text = db.StringField(required=True)
    owner = db.ReferenceField(Bee)
    resource = db.ReferenceField(Resource)
    love_counter = db.IntField(default=0)  # Contador de Love Recibidos
    love_refs = db.ListField()
    created_date = db.DateTimeField(default=datetime.now)
    status = db.StringField(default=STATUS_OBJECT_ACTIVE)


class Scope(db.Document):
    name = db.StringField(required=True)
    description = db.StringField()
    _cls = db.StringField()
    logo = db.ReferenceField(Resource)
    creation_date = db.DateTimeField(default=datetime.now)
    activation_date = db.DateTimeField(default=datetime.now)
    closing_date = db.DateTimeField(default=datetime.now)
    color = db.StringField()
    status = db.StringField(default=STATUS_OBJECT_ACTIVE)
    published = BooleanField()
    meta = {'allow_inheritance': True}

    @queryset_manager
    def objects(self, queryset):
        return queryset.filter(_cls='Scope')


class SubScope(db.Document):
    name = db.StringField(required=True)
    description = db.StringField()
    _cls = db.StringField()
    logo = db.ReferenceField(Resource)
    creation_date = db.DateTimeField(default=datetime.now)
    activation_date = db.DateTimeField(default=datetime.now)
    closing_date = db.DateTimeField(default=datetime.now)
    color = db.StringField()
    status = db.StringField(default=STATUS_OBJECT_ACTIVE)
    published = BooleanField()
    meta = {'allow_inheritance': True}
    parent = db.ReferenceField(Scope)


class Hero(db.Document):
    bee = db.ReferenceField(Person)
    cause = db.ObjectIdField()  # id_cause
    date = db.DateTimeField(default=datetime.now)


class Contact(db.Document):
    name = db.StringField()
    email = db.StringField()
    mobile_phone = db.StringField(max_length=50, default='00000000')
    telephone = db.StringField(max_length=50, default='00000000')
    organization = db.StringField()
    address = db.StringField()


class Cause(Bee):
    description = db.StringField()
    goal = db.StringField()
    sub_scope = db.ReferenceField(SubScope)
    start_date = db.DateTimeField()
    finish_date = db.DateTimeField()
    geographic_location = db.GeoPointField()
    closing_date = db.DateTimeField()
    fly_counter = db.IntField(default=0)  # Contador de fly recibidas
    fly_refs = db.ListField()
    love_meter = db.IntField(default=0)  # Love money given to the cause
    love_goal = db.IntField(default=0)
    ambassadors = db.ListField()  # BORRAR
    hero = db.ReferenceField(Hero)
    beneficiary = db.StringField()  # ACLARAR
    risk_classification = db.StringField()  # ACLARAR
    responsible = db.ReferenceField(Person)  # Responsable que se muestra en la red social
    contacts = db.ListField(
        db.ReferenceField(Contact))  # Id de los responsables legales de la causa (No se muestran en la red)
    partners = db.ListField(db.ReferenceField(Partner))  # Id de los aliados de la causa
    celebrities = db.ListField(db.ReferenceField(Celebrity))  # Id de los embajadores de la causa
    awards = db.ListField(db.ReferenceField(Award))  # Id de los premios de la causa
    url_promotional_video = db.StringField()


class OperationType(db.Document):
    codename = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    created_date = db.DateTimeField(default=datetime.now)


class OperationLog(db.Document):
    owner = db.ReferenceField(Bee)
    operation_type = db.ReferenceField(OperationType)
    created_date = db.DateTimeField(default=datetime.now)
    status = db.StringField(default=STATUS_OBJECT_ACTIVE)
    meta = {'allow_inheritance': True}


class OperationBee(OperationLog):
    bee_destination = db.ReferenceField(Bee)


class OperationPost(OperationLog):
    post_destination = db.ReferenceField(Post)


class OperationComment(OperationLog):
    comment_destination = db.ReferenceField(PostComment)


class OperationAward(OperationLog):
    award_destination = db.ReferenceField(Award)


class RequestFriendship(db.Document):
    owner = db.ReferenceField(Bee)
    destination = db.ReferenceField(Bee)
    status = db.StringField(default=STATUS_FRIENDSHIP_PENDING)
    created_date = db.DateTimeField(default=datetime.now)


class NotificationType(db.Document):
    codename = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    created_date = db.DateTimeField(default=datetime.now)


class Notification(db.Document):
    owner = db.ReferenceField(Bee)
    target = db.ReferenceField(Bee)
    description = db.StringField()
    notification_type = db.ReferenceField(NotificationType)
    status = db.StringField(default=STATUS_NOTIFICATION_UNREAD)
    created_date = db.DateTimeField(default=datetime.now)
    meta = {'allow_inheritance': True}


class NotificationPost(Notification):
    post_destination = db.ReferenceField(Post)


class NotificationComment(Notification):
    comment_destination = db.ReferenceField(PostComment)


class InteractionType(db.Document):
    codename = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    status = db.StringField(default=STATUS_OBJECT_ACTIVE)


class Interaction(db.Document):
    name = db.StringField(required=True)
    value = db.IntField(default=0)
    time_interval = db.IntField(default=0)  # in minutes
    status = db.StringField(default=STATUS_OBJECT_ACTIVE)
    interaction_type = db.ReferenceField(InteractionType)


class InteractionLog(db.Document):
    owner = db.ReferenceField(Bee)
    created_date = db.DateTimeField(default=datetime.now)
    value = db.IntField(default=0)
    interaction_year_week = db.StringField()  # compose year and week
    interaction_name = db.StringField()
    interaction_type = db.StringField()
    status = db.StringField(default=STATUS_OBJECT_ACTIVE)
    meta = {'allow_inheritance': True}


class InteractionBee(InteractionLog):
    bee_destination = db.ReferenceField(Bee)


class InteractionPost(InteractionLog):
    post_destination = db.ReferenceField(Post)


class InteractionComment(InteractionLog):
    comment_destination = db.ReferenceField(PostComment)


class InteractionAward(InteractionLog):
    award_destination = db.ReferenceField(Award)
