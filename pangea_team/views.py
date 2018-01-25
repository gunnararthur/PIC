# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.db import connection
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
    round_nr = email_group[0]
    grade = email_group[1]
    print grade
    if grade == '':
        round_8=get_object_or_404(Round,id=round_nr+'8')
        round_9=get_object_or_404(Round,id=round_nr+'9')
        if round_nr=='1':
            with connection.cursor() as cursor:
                cursor.execute('SELECT distinct(c.email) FROM skraning_contact c')
                email_list=cursor.fetchall()
        elif round_nr=='2':
            with connection.cursor() as cursor:
                cursor.execute('SELECT distinct(c.email) FROM skraning_student s,skraning_group g,m2m_contact_group cg,skraning_contact c WHERE s.group_id=g.name and g.name=cg.group_id and cg.contact_id=c.email and (s.points1>= %s and g.grade = %s or s.points1>= %s and g.grade = %s)',(round_8.cutoff,'8',round_9.cutoff,'9'))
                email_list=cursor.fetchall()
        elif round_nr=='3':
            with connection.cursor() as cursor:
                cursor.execute('SELECT distinct(c.email) FROM skraning_student s,skraning_group g,m2m_contact_group cg,skraning_contact c WHERE s.group_id=g.name and g.name=cg.group_id and cg.contact_id=c.email and (s.points2>= %s and g.grade = %s or s.points2>= %s and g.grade = %s)',(round_8.cutoff,'8',round_9.cutoff,'9'))
                email_list=cursor.fetchall()
        else:
            return HttpResponse('<h1>Page not found</h1>')
    else:
        round = get_object_or_404(Round,id=round_nr+grade)
        print round.cutoff
        if round_nr=='1':
            with connection.cursor() as cursor:
                cursor.execute('SELECT distinct(c.email) FROM skraning_group g,m2m_contact_group cg,skraning_contact c WHERE g.name=cg.group_id and cg.contact_id=c.email and g.grade=%s',[grade])
                email_list=cursor.fetchall()
        elif round_nr=='2':
            with connection.cursor() as cursor:
                cursor.execute('SELECT distinct(c.email) FROM skraning_student s,skraning_group g,m2m_contact_group cg,skraning_contact c WHERE s.group_id=g.name and g.name=cg.group_id and cg.contact_id=c.email and s.points1>= %s and g.grade = %s',(round.cutoff,grade))
                email_list=cursor.fetchall()
        elif round_nr=='3':
            with connection.cursor() as cursor:
                cursor.execute('SELECT distinct(c.email) FROM skraning_student s,skraning_group g,m2m_contact_group cg,skraning_contact c WHERE s.group_id=g.name and g.name=cg.group_id and cg.contact_id=c.email and s.points2>= %s and g.grade = %s',(round.cutoff,grade))
                email_list=cursor.fetchall()
        else:
            return HttpResponse('<h1>Page not found</h1>')

    email_list = ','.join([email_list[i][0] for i in range(len(email_list))])
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
