# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.db import connection
from django.contrib import messages
import os, re, pandas as pd, numpy as np, math as m, time


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
        rnd = get_object_or_404(Round,id=round_nr+grade)
        if round_nr=='1':
            with connection.cursor() as cursor:
                cursor.execute('SELECT distinct(c.email) FROM skraning_group g,m2m_contact_group cg,skraning_contact c WHERE g.name=cg.group_id and cg.contact_id=c.email and g.grade=%s',[grade])
                email_list=cursor.fetchall()
        elif round_nr=='2':
            with connection.cursor() as cursor:
                cursor.execute('SELECT distinct(c.email) FROM skraning_student s,skraning_group g,m2m_contact_group cg,skraning_contact c WHERE s.group_id=g.name and g.name=cg.group_id and cg.contact_id=c.email and s.points1>= %s and g.grade = %s',(rnd.cutoff,grade))
                email_list=cursor.fetchall()
        elif round_nr=='3':
            with connection.cursor() as cursor:
                cursor.execute('SELECT distinct(c.email) FROM skraning_student s,skraning_group g,m2m_contact_group cg,skraning_contact c WHERE s.group_id=g.name and g.name=cg.group_id and cg.contact_id=c.email and s.points2>= %s and g.grade = %s',(rnd.cutoff,grade))
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

    if round_nr=='1':
        rnd8 = get_object_or_404(Round, id='28')
        rnd9 = get_object_or_404(Round, id='29')
        results_data_8 = get_result_table(rnd8)
        results_data_9 = get_result_table(rnd9)
        results_data_8['points'] = [ student.points1 for student in results_data_8['student_object'] ]
        results_data_9['points'] = [ student.points1 for student in results_data_9['student_object'] ]

    elif round_nr=='2' or round_nr=='3':
        rnd8 = get_object_or_404(Round, id='38')
        rnd9 = get_object_or_404(Round, id='39')
        results_data_8 = get_result_table(rnd8)
        results_data_9 = get_result_table(rnd9)
        results_data_8['points'] = [ student.points2 for student in results_data_8['student_object'] ]
        results_data_9['points'] = [ student.points2 for student in results_data_9['student_object'] ]

    results_data_8 = results_data_8.sort_values(by='points',ascending=False).reset_index(drop=True)
    results_data_9 = results_data_9.sort_values(by='points',ascending=False).reset_index(drop=True)
    student_list8 = results_data_8['student_object']
    student_list9 = results_data_9['student_object']
    points8 = list(results_data_8['points'])
    points9 = list(results_data_9['points'])

    return render(request, 'pangea_team/results.html', {'nr_groups_returned': nr_groups_returned, 'nr_groups': nr_groups,
     'email_list': email_list, 'nr_groups_returned_mod10': (nr_groups_returned % 10),
     'student_list8': student_list8, 'points8': points8, 'points9': points9,
     'student_list9': student_list9, 'round_nr': round_nr})

@login_required(login_url='/pangea_team/login')
def calculate_score_view(request, round_nr):
    criteria = float(request.POST['criteria'])
    results_data_8=calculate_results(get_object_or_404(Round,id=round_nr+'8'),criteria)
    results_data_9=calculate_results(get_object_or_404(Round,id=round_nr+'9'),criteria)
    return HttpResponseRedirect(reverse('pangea_team:results', args=[round_nr]))


def calculate_score(ans_str,rnd):
    #function which returns the total points and a binary array containing
    #which questions were correctly answered
    points=0
    points_array=np.zeros((rnd.nr_of_questions,), dtype=np.int)
    if ans_str=='' or rnd.answer_key=='':
        return points,points_array
    if len(ans_str) is not len(rnd.answer_key) or rnd.nr_of_questions is not len(rnd.answer_key):
        #Here it would be better to throw an error
        return points,points_array
    for i in range(rnd.nr_of_questions):
        #Note: Terrible hardcode-ing
        points_array[i] = ans_str[i]==rnd.answer_key[i] or (i==10 and  ans_str[i]=='a' and rnd.round_nr==1)
        points+= int(rnd.weights[i])*points_array[i]
    return points,points_array

def get_result_table(rnd):
    #function which generates a data frame including results for a particular
    #rnd object.
    if rnd.round_nr==1:
        with connection.cursor() as cursor:
            cursor.execute('SELECT s.name,s.kt,g.name as group_name,g.grade,s.ans1 FROM skraning_student s,skraning_group g WHERE s.group_id=g.name and g.grade=%s ORDER BY s.kt',(rnd.grade,))
            result_table=cursor.fetchall()
    elif rnd.round_nr==2:
        with connection.cursor() as cursor:
            cursor.execute('SELECT s.name,s.kt,g.name as group_name,g.grade,ans2 FROM skraning_student s,skraning_group g WHERE s.group_id=g.name and g.grade=%s and s.points1>=%s ORDER BY s.kt',(rnd.grade,rnd.cutoff,))
            result_table=cursor.fetchall()
    elif rnd.round_nr==3:
        with connection.cursor() as cursor:
            cursor.execute('SELECT s.name,s.kt,g.name as group_name,g.grade,ans3 FROM skraning_student s,skraning_group g WHERE s.group_id=g.name and g.grade=%s and s.points1>=%s ORDER BY s.kt',(rnd.grade,rnd.cutoff,))
            result_table=cursor.fetchall()
    #else: ERROR
    #convert tuples to dataframe with column name ans instead of ansx where x in {1,2,3}
    result_table=pd.DataFrame(result_table,columns=['Nemandi','Kt','group_name','grade','ans'])
    students=Student.objects.filter(kt__in=result_table.Kt.values).order_by('kt')
    #Add a column containing the relevant students, note both the df and students
    #are ordered by kt, so the merging is correct
    result_table['student_object']=students
    return result_table

def calculate_results(rnd,criteria):
    result_table=get_result_table(rnd)
    result_table['points']=0
    binary_answers=pd.DataFrame(0,index=np.arange(len(result_table)), columns=range(1,rnd.nr_of_questions+1))
    for i in range(0,len(result_table)):
        score_of_student = calculate_score(result_table['ans'][i],rnd)
        result_table.points.iloc[i] = score_of_student[0]
        binary_answers.loc[i,:] = score_of_student[1]
        student = result_table['student_object'][i]
        if rnd.round_nr==1:
            student.points1=result_table['points'][i]
        elif rnd.round_nr==2:
            student.points2=result_table['points'][i]
        elif rnd.round_nr==3:
            student.points3=result_table['points'][i]
        #else:
            #return ERROR
        student.save()
    binary_answers['group_name']=result_table['group_name']
    grouped_results=binary_answers.groupby('group_name')
    group_names=grouped_results.groups.keys()
    grouped_results=grouped_results.mean()
    for i in range(0,len(grouped_results)):
        questions_results=list(grouped_results.iloc[i,])
        results_string="-".join(str(questions_results[i]) for i in range(len(questions_results)))
        try:
            result_object=get_object_or_404(Results,index=group_names[i]+str(rnd.round_nr))
        except:
            grp=get_object_or_404(Group,name=group_names[i])
            result_object=Results(group=grp,round=rnd,index=group_names[i]+str(rnd.round_nr))
        result_object.results=results_string
        result_object.save()
    #now extract data of students that go to the next round
    result_table=result_table.sort_values(by='points',ascending=False).reset_index(drop=True)
    if criteria > 1:
        remaining_students=result_table[result_table['points']>=result_table['points'].iloc[criteria-1]]
    elif criteria > 0 and criteria <=1:
        remaining_students=result_table[result_table['points']>=result_table['points'].iloc[int(m.ceil(criteria*len(result_table))-1)]]
    else: return ERROR
    if rnd.round_nr<3:
        next_rnd = get_object_or_404(Round, id=str(rnd.round_nr+1)+rnd.grade)
        if next_rnd.cutoff==0:
            next_rnd.cutoff = remaining_students['points'].iloc[len(remaining_students)-1]
            next_rnd.save()
    return remaining_students

def total_avg_questions(rnd):
  results_objects=Results.objects.filter(round=rnd)
  count_list =[0]*rnd.nr_of_questions
  sum_of_active=0
  for results in results_objects:
    avg_of_group=results.results.split('-')
    active_students = results.active
    sum_of_active+=active_students
    count_list=[ y+active_students*float(x) for x,y in zip(avg_of_group,count_list) ]
    return [x/sum_of_active for x in count_list]

@login_required(login_url='/pangea_team/login')
def stat(request, grade):
    return HttpResponse('Hér væri hægt að birta tölfræði.')

@login_required(login_url='/pangea_team/login')
def test(request):
    return render(request, 'pangea_team/test.html')

@login_required(login_url='/pangea_team/login')
def time_test(request):
    sec = float(request.POST['sec'])
    time.sleep(sec)
    messages.success(request, 'Biðinni er lokið!')
    return HttpResponseRedirect(reverse('pangea_team:test'))
