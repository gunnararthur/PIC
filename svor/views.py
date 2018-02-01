# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from skraning.models import Group, Student, Contact, Round

# Create your views here.
def answers(request, group_index, round_nr):
    group = get_object_or_404(Group, index=group_index)
    student_list = group.student_set.all()
    student_list = student_list.order_by('name')
    rnd = get_object_or_404(Round, id=str(round_nr)+str(group.grade))
    nr_of_questions = rnd.nr_of_questions
    q_list = range(1,nr_of_questions+1) # Teljum spurningar frá 1

    return render(request, 'svor/answers.html', {'student_list': student_list,
    'q_list': q_list, 'nr_of_questions': nr_of_questions, 'group': group, 'round_nr': round_nr })

def save_answers(request, group_index, round_nr):
    group = get_object_or_404(Group, index=group_index)
    student_list = group.student_set.all()
    rnd = get_object_or_404(Round, id=str(round_nr)+str(group.grade))
    nr_of_questions = rnd.nr_of_questions
    q_list = range(1,nr_of_questions+1) # Teljum spurningar frá 1

    ans = ''
    # mafs = request.POST['Sp_GunnarArthurHelgason']
    # print mafs
    for student in student_list:
        for question in q_list:
            data = request.POST['Sp_' + str(question) + '_' + student.name]
            #print student.name, data
            if data in 'abcdeABCDE' and data is not '':
                ans = ans + data
                #print 'if já'
            else:
                ans = ans + 'x'
                #print 'if nei'

        if int(round_nr) is 1:
            student.ans1 = ans.lower()
        elif int(round_nr) is 2:
            student.ans2 = ans.lower()
        elif int(round_nr) is 3:
            student.ans3 = ans.lower()
        # ELSE SKILA ERROR
        student.save()
        ans = ''

    return HttpResponseRedirect(reverse('svor:answers', args=[group_index, round_nr]))
