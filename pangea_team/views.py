# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
import os

from skraning.models import Group, Student, Contact, Round


# Create your views here.
@login_required(login_url='/pangea_team/login')
def home(request):
    return render(request, 'pangea_team/home.html')

@login_required(login_url='/pangea_team/login')
def new_round(request):
    return render(request, 'pangea_team/new_round.html')

@login_required(login_url='/pangea_team/login')
def to_answer_key(request): # From new_round
    umf = Round(grade=request.POST['grade'], round_nr=request.POST['round_nr'],
    nr_of_questions=request.POST['nr_of_questions'])
    umf.save()

    return HttpResponseRedirect(reverse('pangea_team:answer_key', args=[umf.id]))

@login_required(login_url='/pangea_team/login')
def answer_key(request, round_id):
    umf = get_object_or_404(Round, pk=round_id)
    q_list = range(1,umf.nr_of_questions+1)
    return render(request, 'pangea_team/answer_key.html', {'round': umf, 'q_list': q_list})

@login_required(login_url='/pangea_team/login')
def save_answer_key(request, round_id):
    umf = get_object_or_404(Round, pk=round_id)
    svor = ''
    stig = ''

    for question in range(1,umf.nr_of_questions+1):
        svor += request.POST['svar_' + str(question)]
        stig += request.POST['stig_' + str(question)]

    umf.answer_key = svor
    umf.weights = stig
    umf.save()

    return HttpResponseRedirect(reverse('pangea_team:finish_new_round'))

@login_required(login_url='/pangea_team/login')
def finish_new_round(request):
    return HttpResponse('TAKK MAÐUR')


@login_required(login_url='/pangea_team/login')
def email_UI(request):
    return render(request, 'pangea_team/email_UI.html')

@login_required(login_url='/pangea_team/login')
def send_email(request):

    subject = request.POST['subject']
    body = request.POST['body']
    recipients = request.POST['recipients'].split('-')
    #her tharf ad vera fall sem kallar a retta vidtakendur
    email = EmailMessage(
        subject,
        body,
        'nemendasvor@gmail.com',
        ['gunnararthur@gmail.com']
    )

    if 'email_attachment' in request.FILES:
        attachment_name = request.FILES['email_attachment'].name
        attachment = request.FILES['email_attachment'].read()
    else:
        return HttpResponse('Virkar ekki kallinn.')

    email.attach(attachment_name, attachment,'application/pdf')
    email.send()

    return HttpResponseRedirect(reverse('pangea_team:email_finish'))

@login_required(login_url='/pangea_team/login')
def email_finish(request):
    return HttpResponse('Póstur hefur verið sendur')

@login_required(login_url='/pangea_team/login')
def results(request):
    return HttpResponse('Hér eru niðurstöður')
