# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/pangea_team/login')
def home(request):
    return render(request, 'pangea_team/home.html')

def new_round(request):
    return HttpResponse('Búa til nýja umferð')

def send_email(request):
    return HttpResponse('Svo þú vilt skrifa póst?')

def results(request):
    return HttpResponse('Hér eru niðurstöður')
