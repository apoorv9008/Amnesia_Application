from django.shortcuts import get_object_or_404, render
from .models import User
from twilio.rest.lookups import TwilioLookupsClient
from twilio.rest.exceptions import TwilioRestException
import datetime
from django.template import RequestContext
from django.shortcuts import render_to_response
from .tasks import *
from django.utils.timezone import utc
from django.template import loader

# Create your views here.

def home(request):
    if request.method == 'GET':
        return render_to_response('home.html', RequestContext(request, {}))

    name = request.POST['name']
    number = request.POST['number']

    if not name:
        return render(request, 'home.html', context={'error_message': 'Please enter a name'})
    if not number:
        return render(request, 'home.html', context={'error_message': 'Please enter a number'})

    try:
        if not is_valid_number( number ):
            return render(request, 'home.html', context={'error_message': 'This number is not a valid number'})
        obj, created = User.objects.get_or_create( name=name, phone_number = number )
        if created:
            return render(request, 'success.html')
        else:
            time = datetime.utcnow().replace(tzinfo=utc) - obj.created
            return render(request, 'home.html', {'error_message': 'This number already exists and has been running for %s'%time})
    except:
        return render(request, 'home.html', {'error_message': 'Error, please try again'})