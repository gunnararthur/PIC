# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Group, Student, Contact, Round

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

    return HttpResponseRedirect(reverse('skraning:student_info', args=[contact.id, group.id]))



def student_info(request, contact_id, group_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    group = get_object_or_404(Group, pk=group_id)
    return render(request, 'skraning/student_info.html', {'contact': contact, 'group': group})



def next_student_info(request, contact_id, group_id):
    # Bý til nema

    if request.POST.get('next', False):
        group_of_student = get_object_or_404(Group, pk=group_id)
        contact_of_student = get_object_or_404(Contact, pk=contact_id)
        student = Student(name=request.POST['name'], kt=request.POST['kt'], group=group_of_student)
        student.save()

        return HttpResponseRedirect(reverse('skraning:student_info', args=[contact_of_student.id, group_of_student.id]))

    elif request.POST.get('finish', False):
        # Athuga hvort nemandi sé skráður
        return HttpResponse('Takk fyrir að taka þátt')

    else:
        return HttpResponse('KLÚÐUR c",')



def finish_enrollment(request):
    return HttpResponse('Takk fyrir að taka þátt')
