# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Group, Student, Contact, Round
import os, pandas

# Create your views here.

def enrollment_info(request, message):
    return render(request, 'skraning/enrollment_info.html', {'message': message})


def download_excel(request):
    file_path = 'pangea_excel_test.xlsx'
    #if os.path.exists(file_path):
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
    #raise Http404

def upload_enrollment_info(request):
    contact = Contact(name=request.POST['name'], email=request.POST['email'])
    contact.save()
    group = Group(school=request.POST['school'], grade=request.POST['grade'])
    group.save()
    contact.groups.add(group)

    if 'skradir_nemendur' in request.FILES:
        file_name = request.FILES['skradir_nemendur'].name
    else:
        message = 2
        return HttpResponseRedirect(reverse('skraning:enrollment_info', args=[message]))


    if file_name[-4:] == 'xlsx' or file_name[-3:] == 'xls':
        skradir_nemendur = pandas.read_excel(request.FILES['skradir_nemendur'])
        # group_of_student = get_object_or_404(Group, pk=group.id)
        for i in skradir_nemendur.index:
            student_name = skradir_nemendur.iloc[i,0]
            student_kt = skradir_nemendur.iloc[i,1]
            student = Student(name=student_name, kt=student_kt, group=group)
            student.save()
        return HttpResponseRedirect(reverse('skraning:finish_enrollment', args=[contact.id, group.id]))
    else:
        message = 1
        print message
        return HttpResponseRedirect(reverse('skraning:enrollment_info', args=[message]))
    return HttpResponse(' c",')

def finish_enrollment(request, contact_id, group_id):
    group = get_object_or_404(Group, pk=group_id)
    student_list = group.student_set.all()
    student_list = student_list.order_by('name')
    return render(request, 'skraning/student_table.html', {'student_list': student_list})
