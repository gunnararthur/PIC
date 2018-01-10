#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Group, Student, Contact, Round,Info_temp,Student_temp
import os, pandas, re, StringIO, csv, xlsxwriter as xl, hashlib
from django.core.mail import EmailMessage
from django.utils.encoding import smart_str



def enrollment_info(request, message):
    excel_path=request.build_absolute_uri() + "download_excel"
    return render(request, 'skraning/enrollment_info.html', {'message': message,'excel_path': excel_path})

def download_excel(request):
    file_path = 'pangea2018_skraning.xlsx'
    #if os.path.exists(file_path):
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
    #raise Http404

def upload_enrollment_info(request):
    group_name = convert_to_ice(request.POST['school'].replace(' ',''))+request.POST['grade']
    info_temp = Info_temp(contact_name=request.POST['name'], contact_email=request.POST['email'],school=request.POST['school'].replace(' ',''),grade=request.POST['grade'],group_name=group_name,index=hashlib.sha224(str(Info_temp.objects.all().count())).hexdigest())
    info_temp.save()

    if 'skradir_nemendur' in request.FILES:
        file_name = request.FILES['skradir_nemendur'].name
    else:
        message = 2
        return HttpResponseRedirect(reverse('skraning:enrollment_info', args=[message]))
    #check whether the input file is of type xlsx or xls
    if file_name[-4:] == 'xlsx' or file_name[-3:] == 'xls':
        skradir_nemendur = pandas.read_excel(request.FILES['skradir_nemendur'],dtype={'Nafn':str,'Kennitala':str},na_values='')
        skradir_nemendur = skradir_nemendur.replace('nan','')
        if skradir_nemendur.shape[1] == 2 and skradir_nemendur.columns[0] == 'Nemandi' and skradir_nemendur.columns[1] =='Kennitala':
            for i in skradir_nemendur.index:
                student_name = skradir_nemendur.iloc[i,0]
                student_kt = str(skradir_nemendur.iloc[i,1])
                student_kt = student_kt.replace('\s+ | -', '')
                if student_kt is not '':
                    student_temp = Student_temp(name=student_name, kt=student_kt, info=info_temp)
                    student_temp.save()
                # Hvað ef það vantar óvart kennitölu?
            return HttpResponseRedirect(reverse('skraning:confirm_enrollment', args=[info_temp.index]))
        else:
            message = 3
            return HttpResponseRedirect(reverse('skraning:enrollment_info', args=[message]))
    else:
        message = 1
        return HttpResponseRedirect(reverse('skraning:enrollment_info', args=[message]))
    return HttpResponse('Óþekkt villa. Reynið aftur eða hafið samband.')

def convert_to_ice(str):
    out_str=''
    ice_letters = {'á':'a','ð': 'd','é':'e','í':'i','ó':'o','ú':'u','ý':'y','þ':'th','æ':'ae','ö':'o'}
    out_str = str.lower()
    for i in range(0,len(ice_letters)):
        out_str = re.sub(ice_letters.keys()[i], ice_letters[ice_letters.keys()[i]], out_str)
    return out_str

def confirm_enrollment(request, info_temp_index):
    info_temp = get_object_or_404(Info_temp, index=info_temp_index)
    student_list = info_temp.student_temp_set.all()
    student_list = student_list.order_by('name')
    return render(request, 'skraning/student_table.html', {'student_list': student_list,'info_temp':info_temp})

def send_confirmation(request, info_temp_index):
    info_temp = get_object_or_404(Info_temp, index=info_temp_index)
    #store contact and group in actual database
    contact = Contact(name=info_temp.contact_name, email=info_temp.contact_email, index=hashlib.sha224(info_temp.contact_email).hexdigest())
    contact.save()
    group = Group(school=info_temp.school, grade=info_temp.grade, name=info_temp.group_name, index=hashlib.sha224(info_temp.group_name).hexdigest())
    group.save()
    contact.groups.add(group)
    student_list = info_temp.student_temp_set.all()
    student_list = student_list.order_by('name')
    #store students in actual database
    for i in student_list:
        student_name = i.name
        student_kt = i.kt
        if i.kt is not '':
            student = Student(name=i.name, kt=i.kt, group=group, index=hashlib.sha224(i.kt).hexdigest())
            student.save()

    f = StringIO.StringIO() # create a file-like object
    workbook = xl.Workbook(f)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, smart_str(u"Nafn"))
    worksheet.write(0, 1, smart_str(u"Kennitala"))

    row = 1
    col = 0
    student_list_all = group.student_set.all()
    student_list_all = student_list.order_by('name')
    for student in student_list_all:
        worksheet.write(row, col, student.name)
        worksheet.write(row, col+1, student.kt)
        row += 1

    workbook.close()

    subject = 'Pangea 2018 - Staðfesting'
    body = 'Góðan dag %s,\n\nþetta er sjálfvirkur póstur sendur til staðfestingar á skráningu í Stærðfræðikeppnina Pangeu 2018. Í viðhengi má nálgast töflu með öllum nemendum úr hópnum %s sem nú hafa verið skráðir. Takk fyrir þátttökuna.\nNánari upplýsingar berast þegar líður að keppninni.\n\nMeð góðri kveðju,\nPangeateymið'% (contact.name, group.name)

    email = EmailMessage(
        subject,
        body,
        'nemendasvor.pangea@gmail.com',
        [contact.email],
        bcc=['nemendasvor.pangea@gmail.com']
    )

    email.attach(group.name+'_nemendur.xlsx', f.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()

    return render(request, 'skraning/confirm_complete.html')
