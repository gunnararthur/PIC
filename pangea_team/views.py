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
def email_UI(request):
    email_list = ''
    return render(request, 'pangea_team/email_UI.html', {'email_list': email_list})

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
def generate_mail_list(request):
    email_group = request.POST['email_group'].split('-')
    #email_list =
    return render(request, 'pangea_team/email_UI.html', {'email_list': email_list})



# def body_input(s):
#     # Byrjun á útfærslu á custom pósti (svipað mailmerge frá því 2017)
#     var_names = re.findall(r"#([A-Z,a-z,0-9,\.]+)#", s)
#     for name in var_names:
#         if

@login_required(login_url='/pangea_team/login')
def email_finish(request):
    return HttpResponse('Póstur hefur verið sendur')

@login_required(login_url='/pangea_team/login')
def results(request):
    return HttpResponse('Hér eru niðurstöður')
