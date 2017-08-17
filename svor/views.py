# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from skraning.models import Group, Student, Contact, Round

# Create your views here.
def answers(request, group_id, round_nr):
    return render(request, 'svor/answers.html')

def save_answers(request):
    return HttpResponseRedirect(reverse('svor:answers', args=[70, 1]))
