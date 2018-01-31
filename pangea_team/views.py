# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.db import connection
import os, re

from skraning.models import Group, Student, Contact, Round


# Create your views here.
@login_required(login_url='/pangea_team/login')
def home(request):
    return render(request, 'pangea_team/home.html')

@login_required(login_url='/pangea_team/login')
def email_UI(request):
    try:
        email_group = request.POST['email_group'].split('-')
        round_nr = email_group[0]
        grade = email_group[1]
        email_list = generate_mail_list(round_nr, grade)
    except:
        email_list = generate_mail_list('','')
    return render(request, 'pangea_team/email_UI.html', {'email_list': email_list})


@login_required(login_url='/pangea_team/login')
def send_email(request):

    subject = request.POST['recipients']
    body = request.POST['body']
    try:
        email_group = request.POST['recipients'].split('-')
        round_nr = email_group[0]
        grade = email_group[1]
        recipients_list = generate_mail_list(round_nr, grade).split(',')
    except:
        return HttpResponse('Passa að velja einhver hóp.')

    group_list = Group.objects.filter(contact__email__in=recipients_list).distinct()
    for group in group_list:
        subject = eval_placeholder(request.POST['subject'],group,round_nr)
        body = eval_placeholder(request.POST['body'],group,round_nr)
        recipients = list(Contact.objects.filter(groups=group).values_list('email',flat=True))
        email = EmailMessage(
            subject,
            body,
            'nemendasvor.pangea@gmail.com',
            recipients
        )
        email.send()

    # if 'email_attachment' in request.FILES:
    #     attachment_name = request.FILES['email_attachment'].name
    #     attachment = request.FILES['email_attachment'].read()
    # else:
    #     return HttpResponse('Virkar ekki kallinn.')
    #
    # email.attach(attachment_name, attachment,'application/pdf')
    # email.send()

    return HttpResponseRedirect(reverse('pangea_team:email_finish'))

@login_required(login_url='/pangea_team/login')
def send_test_email(request):
    group = Group(school= 'Testskóli', grade='8', name='Testskoli8', index='hex_code_hash')
    subject = eval_placeholder(request.POST['subject'],group,'1')
    body = eval_placeholder(request.POST['body'],group,'1')
    recipients = ['nemendasvor.pangea@gmail.com']

    email = EmailMessage(
        subject,
        body,
        'nemendasvor.pangea@gmail.com',
        recipients
    )
    email.send()
    return HttpResponseRedirect(reverse('pangea_team:email_UI'))


def eval_placeholder(s,group,round_nr):
    # Takes in excactly three arguments: a string s, a Group group and an integer
    # round_nr. The string can
    # include three different placeholder tags #group.school#, #group.grade# or
    # #group.index#. The output is a string where the placeholders have been
    # replaced with appropriate values in respect to the group.
    var_names = re.findall(r"#([A-Z,a-z,0-9,\.]+)#", s)
    vals=[]
    for name in var_names:
        if 'school'==name:
            vals.append(group.school)
        if 'grade'==name:
            vals.append(group.grade + '. bekkur')
        if 'link'==name:
            vals.append('http://138.197.177.72/svor/' + group.index + '/' + round_nr)
    return re.sub(r"#([A-Z,a-z,0-9,\.]+)#","%s",s) % tuple(vals)


def generate_mail_list(round_nr, grade):
    if round_nr == '':
        return ''
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
            return 'ERROR'
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
            return 'ERROR'

    email_list = ','.join([email_list[i][0] for i in range(len(email_list))])
    return email_list


@login_required(login_url='/pangea_team/login')
def email_finish(request):

    return render(request, 'pangea_team/email_finish.html')

@login_required(login_url='/pangea_team/login')
def results(request):
    groups = Group.objects.all()
    nr_groups = len(groups)
    groups_not_returned = []
    nr_groups_returned=0
    for g in groups:
        students_ans=Student.objects.filter(group=g).values_list('ans1')
        if ('',) not in students_ans:
            nr_groups_returned += 1
        else:
            groups_not_returned.append(g)
    contacts_to_send=list(Contact.objects.filter(groups__in=groups_not_returned).values_list('email').distinct())
    email_list = ','.join([contacts_to_send[i][0] for i in range(len(contacts_to_send))])
    #return HttpResponse(str(nr_groups_returned) + ' hópar af ' + str(nr_groups) + ' búnir að skila niðurstöðum. Netföng tengiliða sem eiga eftir að skrá niðurstöður sinna hópa eru: ' + email_list)

    return render(request, 'pangea_team/results.html', {'nr_groups_returned': nr_groups_returned, 'nr_groups': nr_groups, 'email_list': email_list, 'nr_groups_returned_mod10': (nr_groups_returned % 10)})
