from django.conf.urls import url

from . import views


app_name = 'svor'
urlpatterns = [
    url(r'^(?P<group_id>[0-9]+)/(?P<round_nr>[1-2])$', views.answers, name='answers'),
    url(r'^vista_svor$', views.save_answers, name='save_answers'),
]
