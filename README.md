# Amnesia_Application

Problem Statement

John has a certain kind of amnesia. Every hour, he forgets his name. He’s tired of setting an alarm on his very old phone which doesn’t allow setting cron alarm jobs.

He wants to hire you to create an application which will send him an SMS every hour to remind him of his name. He also wants you to make sure that he doesn’t get alarms during the night when he is asleep.

Since you don’t know which part of the world John lives in, you have to use an SMS provider which can send an SMS to nearly every country. Twilio is a nice service for sending out SMSes. However, sometimes Twilio’s SMS fails, in which case you have to send it again.

Please do the following:

1. Create a (basic) web based application where John can set his phone number
2. Send an SMS every one hour except at night
3. Try resending an SMS if it fails, but retry no more than 5 times. (There is only so much you can do!)
4. The web application should also log all the failed messages and tell John for how many hours the application has been running.

# Instructions for starting the application

It's an amnesia application built in Django framework which is used to send SMS of name on the verified phone number hourly depending on the availability of the User
<br>
The Web Application Amnesia requires Redis to function, and operates on PORT 6379
Redis 2.10.5 is used for this application.
Once redis-server is called and is active. We can run the Django server using `python3 manage.py runserver 8000` and go to `http://127.0.0.1:8000/amnesia_ap/home` from the web browser.
<br>Open 2 other terminals also in the folder where manage.py exists and run :<br>
1. celery -A amnesia worker -l info<br>
2. celery -A amnesia beat -l info<br>

Please swap in your Twilio- TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in settings.py file to avoid authentication error. 
<br>
It is important to note that one must register their phone number on their free Twilio account and verify it via SMS. Non registered numbers cannot have SMS's sent from a free account.
