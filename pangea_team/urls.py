from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


app_name = 'pangea_team'
urlpatterns = [
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, name='logout'),
    url(r'^home/$', views.home),

    url(r'^home/new_round$', views.new_round, name='new_round'),
    url(r'^home/to_answer_key$', views.to_answer_key, name='to_answer_key'),
    url(r'^home/new_round/answer_key/(?P<round_id>[0-9]+)$', views.answer_key, name='answer_key'),
    url(r'^home/save_answer_key/(?P<round_id>[0-9]+)$', views.save_answer_key, name='save_answer_key'),
    url(r'^home/new_round/finish$', views.finish_new_round, name='finish_new_round'),



    url(r'^home/email$', views.email_UI, name='email_UI'),
    url(r'^home/send_email$', views.send_email, name='send_email'),
    url(r'^home/email/finish$', views.email_finish, name='email_finish'),





    url(r'^home/results$', views.results, name='results'),

]
