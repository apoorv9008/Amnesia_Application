from twilio.rest.lookups import TwilioLookupsClient
from twilio.rest.exceptions import TwilioRestException
from twilio.rest import TwilioRestClient
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from .models import User
from datetime import datetime
from pytz import timezone
from phonenumbers import timezone as ptz
import phonenumbers as ph

ALERT_START_TIME = 7
ALERT_STOP_TIME = 23


def is_valid_number(number):
    client = TwilioLookupsClient()
    try:
        response = client.phone_numbers.get(number)
        response.phone_number               # If invalid, throws an exception.
        return True
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e

@task(name="send_sms_task")
def send_sms_task(number, message):         #https://www.twilio.com/docs/api/rest/sending-messages
    log_file = open("log.txt", "a+")
    client = TwilioRestClient()
    attempts = 0
    while attempts < 5:
        try:
            client.messages.create(
                to      = number,
                from_   = "+12015915580",
                body    = message,
                )
            log_file.write("%s UTC - Message sent to %s\n"%(datetime.now(timezone('UTC')), number))
            log_file.close()
            break
        except TwilioRestException as e:
            log_file.write("%s UTC - %s"(datetime.now(timezone('UTC')), e))
            attempts = attempts + 1
    log_file.close()


#crontab(minute=0, hour='%s-%s'%(ALERT_START_TIME, ALERT_STOP_TIME))
@periodic_task(run_every=(crontab(minute=0)), name="main_task", ignore_result=True)
def main_task():
    users = User.objects.all()
    for user in users:
        if valid_hours(user.phone_number):
            send_sms_task(user.phone_number, user.name)
        else:
            continue


def valid_hours(number):
    phone_number = ph.parse(number, None)
    country_timezone = ptz.time_zones_for_number(phone_number)[0]
    country_time = datetime.now(timezone(country_timezone))
    if country_time.hour <= ALERT_STOP_TIME or country_time.hour >= ALERT_START_TIME:
        return True
    else:
        return False