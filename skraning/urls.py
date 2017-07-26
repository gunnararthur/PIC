from django.conf.urls import url

from . import views


app_name = 'skraning'
urlpatterns = [
    # ex: /skraning/
    url(r'^$', views.contact_info, name='contact_info'),

    url(r'^to_student_info/', views.to_student_info, name='to_student_info'),
    # ex: /skraning/45/53
    url(r'^(?P<contact_id>[0-9]+)/(?P<group_id>[0-9]+)$', views.student_info, name='student_info'),

    url(r'^next_student_info/(?P<contact_id>[0-9]+)/(?P<group_id>[0-9]+)$', views.next_student_info, name='next_student_info'),

]
