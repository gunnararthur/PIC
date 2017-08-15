# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from skraning.models import Round

# Create your views here.
def grin(request, contact_id, round_nr):
    umferd = Round(grade='8', answer_key='abcdabcdabcde', weights='1111222233334', round_nr=round_nr)
    strengur = 'Hæ ég er notandi ' + contact_id + ' í umferð ' + round_nr
    strengur = strengur + ' Bekkur: ' + umferd.grade + ' Svör: ' + umferd.answer_key
    return HttpResponse(strengur)
