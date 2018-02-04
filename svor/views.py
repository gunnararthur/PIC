# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages

from skraning.models import Group, Student, Contact, Round, Results

# Create your views here.
def answers(request, group_index, round_nr):
    group = get_object_or_404(Group, index=group_index)
    student_list = list(group.student_set.all())
    student_list.sort(cmp=cmp2)
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
    active = 0
    # mafs = request.POST['Sp_GunnarArthurHelgason']
    # print mafs
    for student in student_list:
        for question in q_list:
            data = request.POST['Sp_' + str(question) + '_' + student.name]
            if data in 'abcdeABCDE' and data is not '':
                ans = ans + data
            else:
                ans = ans + 'x'

        if int(round_nr) is 1:
            student.ans1 = ans.lower()
        elif int(round_nr) is 2:
            student.ans2 = ans.lower()
        elif int(round_nr) is 3:
            student.ans3 = ans.lower()
        # ELSE SKILA ERROR
        student.save()
        active += (set('abcdeABCDE') & set(ans) != set())
        ans = ''

    try:
        results = get_object_or_404(Results, index=group.name+str(round_nr))
    except:
        results = Results(group=group, round=rnd, index=group.name+str(round_nr))
    results.returned = True
    results.active = active
    results.save()

    messages.success(request, 'Skráð svör hafa verið vistuð!')
    return HttpResponseRedirect(reverse('svor:answers', args=[group_index, round_nr]))


def cmp2(student1,student2):
    s1 = student1.name
    s2 = student2.name
    i = 0
    ice_alphabet={'A':1,'Á':2,'B':3,'C':4,'D':5,'Ð':6,'E':7,'É':8,'F':9,'G':10,'H':11,'I':12,'Í':13,'J':14,'K':15,'L':16,'M':17,'N':18,'O':19,'Ó':20,'P':21,'R':22,'S':23,'T':24,'U':25,'Ú':26,'V':27,'W':28,'X':29,'Y':30,'Z':31,'Þ':32,'Æ':33,'Ö':34,'a':1,'á':2,'b':3,'c':4,'d':5,'ð':6,'e':7,'é':8,'f':9,'g':10,'h':11,'i':12,'í':13,'j':14,'k':15,'l':16,'m':17,'n':18,'o':19,'ó':20,'p':21,'r':22,'s':23,'t':24,'u':25,'ú':26,'v':27,'w':28,'x':29,'y':30,'z':31,'þ':32,'æ':33,'ö':34}
    while(len(s1) > i and len(s2) > i):
        #if char not found in dicitonary, assign it to a large enough value
        try:
            val_s1=ice_alphabet[s1[i]]
        except:
            val_s1=max(ice_alphabet.values())+1

        try:
            val_s2=ice_alphabet[s2[i]]
        except:
            val_s2=max(ice_alphabet.values())+1
        if val_s1 < val_s2:
            return -1
        elif val_s1 > val_s2:
            return 1
        i=i+1
    #at this point, if they are of same length, they must be equal
    #if s1 is shorter than s2 return -1 else 1
    if len(s1) ==i and len(s2)==i:
        return 0
    elif len(s1)==i:
        return -1
    else:
        return 1
