__author__ = 'palencia77'
# Created: 11/11/2014 By dev@domain-dev04
# Thread handler with APScheduler:
# Doc at: https://apscheduler.readthedocs.org/en/latest/userguide.html
# Example background process: https://bitbucket.org/agronholm/apscheduler/src/master/examples/schedulers/background.py
# Example blocking process: https://bitbucket.org/agronholm/apscheduler/src/master/examples/schedulers/blocking.py
from apscheduler.schedulers.background import BackgroundScheduler
from com.services.services_security import *
from com.services.services_bee import *
from com.tools.objects_status import *

'''
@summary: Thread that find users with PENDING status expired
          to change their status to SUSPENDED.
'''
def thread_check_users_with_PENDING_status():
    print "Threads executed"
    users = get_user_by_status_and_status_date_interval(STATUS_OBJECT_PENDING, 1)
    if users is not None:
        for user in users:
            if 'id_bee' in user.parameters:
                if user.parameters['id_bee'] is not None:
                    bee = get_bee_by_id(str(user.parameters['id_bee']))
                    bee_update_status(bee, STATUS_OBJECT_SUSPENDED)
            user_update_status(user, STATUS_OBJECT_SUSPENDED)

'''
@summary: Thread that find users with SUSPENDED status expired
          to change their status to ROBOT.
'''
def thread_check_users_with_SUSPENDED_status():
    users = get_user_by_status_and_status_date_interval(STATUS_OBJECT_SUSPENDED, 1)
    if users is not None:
        for user in users:
            if 'id_bee' in user.parameters:
                if user.parameters['id_bee'] is not None:
                    bee = get_bee_by_id(str(user.parameters['id_bee']))
                    bee_update_status(bee, STATUS_OBJECT_ROBOT)
            user_update_status(user, STATUS_OBJECT_ROBOT)

def tick():
    print('Tick! Executing threads: %s' % datetime.now())

#####################################################################################
####################### THREADS CONTROL #############################################
#####################################################################################
# -- THREADS DECLARATION:
scheduler_01 = BackgroundScheduler()
# -- THREADS CONFIGURATION:
scheduler_01.add_job(thread_check_users_with_PENDING_status, 'interval', minutes=30)
scheduler_01.add_job(thread_check_users_with_SUSPENDED_status, 'interval', minutes=30)
##scheduler_01.add_job(tick, 'interval', seconds=5)
# -- THREADS EXECUTION:
scheduler_01.start()
# -- #################################################################################

'''
@summary: Service to stop all the threads execution
'''
def thread_stop_all():
    scheduler_01.shutdown()

'''
@summary: Service to restart all the threads execution
'''
def thread_restart_all():
    scheduler_01.shutdown()
    scheduler_01.start()