from django.conf.urls import url

from . import views


app_name = 'svor'
urlpatterns = [
    url(r'^(?P<contact_id>[0-9]+)/(?P<round_nr>[1-2])$', views.grin, name='grin'),
]
