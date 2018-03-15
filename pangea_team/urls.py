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

    url(r'^home/results/(?P<round_nr>[1-3])$', views.results, name='results'),
    url(r'^home/results/(?P<round_nr>[1-3])/calc$', views.calculate_score_view, name='calculate_score_view'),
    url(r'^home/results/(?P<round_nr>[1-3])/(?P<grade>[89])/excel$', views.get_excel_results, name='get_excel_results'),

    url(r'^home/stat/(?P<grade>[89])$', views.stat, name='stat'),
    url(r'^home/finals/(?P<grade>[89])/(?P<action_type>[sc])$', views.finals, name='finals'),
    url(r'^home/finals/(?P<grade>[89])/action_view$', views.finals_action_view, name='finals_action_view'),

    url(r'^home/test/$', views.test, name='test'),
    url(r'^home/test/wait$', views.time_test, name='time_test'),

]
