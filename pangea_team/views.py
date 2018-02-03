# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.db import connection
import os, re, pandas as pd, numpy as np, math as m

from skraning.models import Group, Student, Contact, Round, Results


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
def results(request, round_nr):
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
    results_data_8=calculate_results(get_object_or_404(Round,id=round_nr+'8'),0.5)
    results_data_9=calculate_results(get_object_or_404(Round,id=round_nr+'9'),0.5)

    student_list8 = results_data_8['student_object']
    points8 = list(results_data_8['points'])
    student_list9 = results_data_9['student_object']
    points9 = list(results_data_9['points'])
    return render(request, 'pangea_team/results.html', {'nr_groups_returned': nr_groups_returned, 'nr_groups': nr_groups,
     'email_list': email_list, 'nr_groups_returned_mod10': (nr_groups_returned % 10),
     'student_list8': student_list8, 'points8': points8, 'points9': points9,
     'student_list9': student_list9})

def calculate_score(ans_str,round):
    #function which returns the total points and a binary array containing
    #which questions were correctly answered
    points=0
    points_array=np.zeros((round.nr_of_questions,), dtype=np.int)
    for i in range(round.nr_of_questions):
        points_array[i]=ans_str[i]==round.answer_key[i]
        points+= int(round.weights[i])*points_array[i]
    return points,points_array

def get_result_table(round):
    #function which generates a data frame including results for a particular
    #round object.
    if round.round_nr==1:
        with connection.cursor() as cursor:
            cursor.execute('SELECT s.name,s.kt,g.name as group_name,g.grade,s.ans1 FROM skraning_student s,skraning_group g WHERE s.group_id=g.name and g.grade=%s ORDER BY s.kt',(round.grade,))
            result_table=cursor.fetchall()
    elif round.round_nr==2:
        prev_round=get_object_or_404(Round,round_nr=1,grade=round.grade)
        with connection.cursor() as cursor:
            cursor.execute('SELECT s.name,s.kt,g.name as group_name,g.grade,ans2 FROM skraning_student s,skraning_group g WHERE s.group_id=g.name and g.grade=%s and s.points1>=%s ORDER BY s.kt',(round.grade,prev_round.cutoff,))
            result_table=cursor.fetchall()
    elif round.round_nr==3:
        prev_round=get_object_or_404(Round,round_nr=2,grade=round.grade)
        with connection.cursor() as cursor:
            cursor.execute('SELECT s.name,s.kt,g.name as group_name,g.grade,ans3 FROM skraning_student s,skraning_group g WHERE s.group_id=g.name and g.grade=%s and s.points1>=%s ORDER BY s.kt',(round.grade,prev_round.cutoff,))
            result_table=cursor.fetchall()
    #else: ERROR
    #convert tuples to dataframe with column name ans instead of ansx where x in {1,2,3}
    result_table=pd.DataFrame(result_table,columns=['Nemandi','Kt','group_name','grade','ans'])
    students=Student.objects.filter(kt__in=result_table.Kt.values).order_by('kt')
    #Add a column containing the relevant students, note both the df and students
    #are ordered by kt, so the merging is correct
    result_table['student_object']=students
    return result_table

def calculate_results(round,criteria):
    import pandas as pd
    import numpy as np

    result_table=get_result_table(round)
    result_table['points']=0
    binary_answers=pd.DataFrame(0,index=np.arange(len(result_table)), columns=range(1,round.nr_of_questions+1))
    for i in range(0,len(result_table)):
        score_of_student=calculate_score(result_table['ans'][i],round)
        result_table['points'][i]=score_of_student[0]
        binary_answers.loc[i]=score_of_student[1]
        student= result_table['student_object'][i]
        if round.round_nr==1:
            student.points1=result_table['points'][i]
        elif round.round_nr==2:
            student.points2=result_table['points'][i]
        elif round.round_nr==3:
            student.points3=result_table['points'][i]
        #else:
            #return ERROR
        student.save()
    binary_answers['group_name']=result_table['group_name']
    grouped_results=binary_answers.groupby('group_name')
    group_names=grouped_results.groups.keys()
    grouped_results=grouped_results.mean()
    for i in range(0,len(grouped_results)):
        questions_results=list(binary_answers.loc[i,binary_answers.columns!="group_name"])
        results_string="-".join(str(questions_results[i]) for i in range(len(questions_results)))
        try:
            result_object=get_object_or_404(Results,index=group_names[i]+round.round_nr)

        except:
            result_object=Results(group=get_object_or_404(Group,name=group_names[i]),round=round,index=group_names[i]+str(round.round_nr))

    result_object.results=results_string
    result_object.save()
    #now extract data of students that go to the next round
    result_table=result_table.sort_values(by='points',ascending=False).reset_index(drop=True)
    if criteria > 1:
        remaining_students=result_table[result_table['points']>=result_table['points'].iloc[criteria-1]]
    elif criteria > 0 and criteria <=1:
        remaining_students=result_table[result_table['points']>=result_table['points'].iloc[int(m.ceil(criteria*len(result_table))-1)]]
    else: return ERROR
    round.cutoff = remaining_students['points'].iloc[len(remaining_students)-1]
    round.save()
    return remaining_students

@login_required(login_url='/pangea_team/login')
def stat(request, grade):
    return HttpResponse('Hér væri hægt að birta tölfræði.')
