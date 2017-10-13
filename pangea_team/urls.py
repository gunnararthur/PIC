from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


app_name = 'pangea_team'
urlpatterns = [
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, name='logout'),
    url(r'^home/$', views.home),
    url(r'^home/new_round$', views.new_round, name='new_round'),
    url(r'^home/send_email$', views.send_email, name='send_email'),
    url(r'^home/results$', views.results, name='results'),

]
