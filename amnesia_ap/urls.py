from django.conf.urls import url
from . import views

app_name = 'amnesia_ap'

urlpatterns = [
    url(r'^home$', views.home, name="home"),

]