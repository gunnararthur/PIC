from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from . import views


app_name = 'pangea_team'
urlpatterns = [
    url(r'^$', views.home),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, name='logout'),
    url(r'^home/$', views.home, name='home'),

    url(r'^home/email/$', views.email_UI, name='email_UI'),
    url(r'^home/send_email/$', views.send_email, name='send_email'),
    url(r'^home/send_test_email/$', views.send_test_email, name='send_test_email'),
    #url(r'^home/email/generate_mail_list$', views.generate_mail_list, name='generate_mail_list'),
    url(r'^home/email/finish/$', views.email_finish, name='email_finish'),

    url(r'^home/results/$', views.results, name='results'),

]
