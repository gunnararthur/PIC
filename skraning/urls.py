from django.conf.urls import url

from . import views


app_name = 'skraning'
urlpatterns = [
    # ex: /skraning/
    url(r'^(?P<message>[0-9]*)$', views.enrollment_info, name='enrollment_info'),

    url(r'^download_excel/$', views.download_excel, name='download_excel'),

    url(r'^upload_enrollment_info/', views.upload_enrollment_info, name='upload_enrollment_info'),

    url(r'^(?P<contact_index>[0-9]+)/(?P<group_index>[0-9]+)/$', views.confirm_enrollment, name='confirm_enrollment'),

    url(r'^(?P<contact_index>[0-9]+)/(?P<group_index>[0-9]+)/stadfest$', views.send_confirmation, name='send_confirmation'),


]
