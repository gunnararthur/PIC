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

def new_round(request):
    return render(request, 'pangea_team/new_round.html')

def to_answer_key(request): # From new_round
    umf = Round(grade=request.POST['grade'], round_nr=request.POST['round_nr'],
    nr_of_questions=request.POST['nr_of_questions'])
    umf.save()

    return HttpResponseRedirect(reverse('pangea_team:answer_key', args=[umf.id]))

def answer_key(request, round_id):
    umf = get_object_or_404(Round, pk=round_id)
    q_list = range(1,umf.nr_of_questions+1)
    return render(request, 'pangea_team/answer_key.html', {'round': umf, 'q_list': q_list})

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

def finish_new_round(request):
    return HttpResponse('TAKK MAÐUR')



def email_UI(request):
    return render(request, 'pangea_team/email_UI.html')

def send_email(request):

    subject = request.POST['subject']
    body = request.POST['body']
    password = request.POST['password']
    settings.EMAIL_HOST_PASSWORD = password
    #os.environ['EMAIL_HOST_PASSWORD']=password
    #print os.environ.get("EMAIL_HOST_PASSWORD", "Hallo")
    recipients = request.POST['recipients'].split('-')
    #her tharf ad vera fall sem kallar a retta vidtakendur
    email = EmailMessage(
        subject,
        body,
        'nemendasvor@gmail.com',
        ['gunnararthur@gmail.com', 'solviro@gmail.com']
    )
    email.send()
    """ send_mail(
    subject,
    body,
    'nemendasvor@gmail.com',
    ['gunnararthur@gmail.com', 'solviro@gmail.com'],
    fail_silently=False,
    auth_password=password,
    )"""

    return HttpResponseRedirect(reverse('pangea_team:email_finish'))

def email_finish(request):
    return HttpResponse('Póstur hefur verið sendur')

def results(request):
    return HttpResponse('Hér eru niðurstöður')
