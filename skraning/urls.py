from django.conf.urls import url

from . import views


app_name = 'skraning'
urlpatterns = [
    # ex: /skraning/
    url(r'^$', views.contact_info, name='contact_info'),

    url(r'^to_student_info/', views.to_student_info, name='to_student_info'),
    # ex: /skraning/45/53
    url(r'^(?P<contact_id>[0-9]+)/(?P<group_id>[0-9]+)/(?P<message>[0-9]+)$', views.student_info, name='student_info'),

    url(r'^download_excel/$', views.download_excel, name='download_excel'),

    url(r'^read_excel/(?P<contact_id>[0-9]+)/(?P<group_id>[0-9]+)$', views.read_excel_upload, name='read_excel_upload'),

    url(r'^next_student_info/(?P<contact_id>[0-9]+)/(?P<group_id>[0-9]+)$', views.next_student_info, name='next_student_info'),

    url(r'^(?P<contact_id>[0-9]+)/(?P<group_id>[0-9]+)/tafla$', views.student_table, name='student_table'),

    url(r'finish', views.finish_enrollment, name='finish_enrollment'),

]
