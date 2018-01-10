from django.conf.urls import url

from . import views


app_name = 'skraning'
urlpatterns = [
    # ex: /skraning/
    url(r'^(?P<message>[0-3]?)$', views.enrollment_info, name='enrollment_info'),

    url(r'^[0-3]?download_excel/$', views.download_excel, name='download_excel'),

    url(r'^upload_enrollment_info/', views.upload_enrollment_info, name='upload_enrollment_info'),

    url(r'^(?P<info_temp_index>[0-9a-f]+)/$', views.confirm_enrollment, name='confirm_enrollment'),

    url(r'^(?P<info_temp_index>[0-9a-f]+)/stadfest$', views.send_confirmation, name='send_confirmation'),


]
