# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Group, Student, Contact, Round
import os, pandas

# Create your views here.

def contact_info(request):
    return render(request, 'skraning/contact_info.html')

def to_student_info(request):
    # Bý til contact sem á að bæta við
    # ÞARF AÐ ATHUGA MEÐ TVÍRIT
    contact = Contact(name=request.POST['name'], email=request.POST['email'])
    contact.save()

    # Bý til group sem á að bæta við og tengja við added_contact
    # ÞARF AÐ ATHUGA MEÐ TVÍRIT
    group = Group(school=request.POST['school'], grade=request.POST['grade'])
    group.save()

    contact.groups.add(group)

    return HttpResponseRedirect(reverse('skraning:student_info', args=[contact.id, group.id,'0']))

def student_info(request, contact_id, group_id, message):
    contact = get_object_or_404(Contact, pk=contact_id)
    group = get_object_or_404(Group, pk=group_id)
    return render(request, 'skraning/student_info.html', {'contact': contact, 'group': group, 'message': message})

def next_student_info(request, contact_id, group_id, message):
    # Bý til nema
    if request.POST.get('next', False):
        group_of_student = get_object_or_404(Group, pk=group_id)
        contact_of_student = get_object_or_404(Contact, pk=contact_id)
        student = Student(name=request.POST['name'], kt=request.POST['kt'], group=group_of_student)
        student.save()

        return HttpResponseRedirect(reverse('skraning:student_info', args=[contact_of_student.id, group_of_student.id,'0']))

    elif request.POST.get('finish', False):
        # Athuga hvort nemandi sé skráður
        return HttpResponse('Takk fyrir að taka þátt')

    else:
        return HttpResponse('KLÚÐUR c",')

def finish_enrollment(request):
    return HttpResponse('Takk fyrir að taka þátt')










def download_excel(request):
    file_path = 'pangea_excel_test.xlsx'
    #if os.path.exists(file_path):
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
    #raise Http404

def read_excel_upload(request, contact_id, group_id):

    if 'skradir_nemendur' in request.FILES:
        file_name = request.FILES['skradir_nemendur'].name
    else:
        message = 2
        print message
        return HttpResponseRedirect(reverse('skraning:student_info', args=[contact_id, group_id, message]))


    if file_name[-4:] == 'xlsx' or file_name[-3:] == 'xls':
        skradir_nemendur = pandas.read_excel(request.FILES['skradir_nemendur'])
        group_of_student = get_object_or_404(Group, pk=group_id)
        for i in skradir_nemendur.index:
            student_name = skradir_nemendur.iloc[i,0]
            student_kt = skradir_nemendur.iloc[i,1]
            student = Student(name=student_name, kt=student_kt, group=group_of_student)
            student.save()
        return HttpResponseRedirect(reverse('skraning:student_table', args=[contact_id, group_id]))
    else:
        message = 1
        print message
        return HttpResponseRedirect(reverse('skraning:student_info', args=[contact_id, group_id, message]))
    return HttpResponse(' c",')

def student_table(request, contact_id, group_id):
    group = get_object_or_404(Group, pk=group_id)
    student_list = group.student_set.all()
    student_list = student_list.order_by('name')
    return render(request, 'skraning/student_table.html', {'student_list': student_list})
