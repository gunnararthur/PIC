#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Group, Student, Contact, Round
import os, pandas, re, StringIO, csv, xlsxwriter as xl
from django.core.mail import EmailMessage
from django.utils.encoding import smart_str



def enrollment_info(request, message):
    excel_path=request.build_absolute_uri() + "download_excel"
    return render(request, 'skraning/enrollment_info.html', {'message': message,'excel_path': excel_path})

def download_excel(request):
    file_path = 'pangea_excel_test.xlsx'
    #if os.path.exists(file_path):
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
    #raise Http404

def upload_enrollment_info(request):
    contact = Contact(name=request.POST['name'], email=request.POST['email'], index=Contact.objects.all().count())
    contact.save()
    group = Group(school=request.POST['school'], grade=request.POST['grade'], name=request.POST['school']+request.POST['grade'], index=Group.objects.all().count())
    group.save()
    contact.groups.add(group)

    if 'skradir_nemendur' in request.FILES:
        file_name = request.FILES['skradir_nemendur'].name
    else:
        message = 2
        return HttpResponseRedirect(reverse('skraning:enrollment_info', args=[message]))


    if file_name[-4:] == 'xlsx' or file_name[-3:] == 'xls':
        skradir_nemendur = pandas.read_excel(request.FILES['skradir_nemendur'])
        for i in skradir_nemendur.index:
            student_name = skradir_nemendur.iloc[i,0]
            student_kt = str(skradir_nemendur.iloc[i,1])
            student_kt = student_kt.replace('\s+ | -', '')
            if student_kt is not '':
                student = Student(name=student_name, kt=student_kt, group=group, index=Student.objects.all().count())
                student.save()
        return HttpResponseRedirect(reverse('skraning:confirm_enrollment', args=[contact.index, group.index]))
    else:
        message = 1
        print message
        return HttpResponseRedirect(reverse('skraning:enrollment_info', args=[message]))
    return HttpResponse(' c",')



def confirm_enrollment(request, contact_index, group_index):
    group = get_object_or_404(Group, index=group_index)
    student_list = group.student_set.all()
    student_list = student_list.order_by('name')
    return render(request, 'skraning/student_table.html', {'student_list': student_list, 'contact_index': contact_index, 'group_index': group_index})

def send_confirmation(request, contact_index, group_index):
    group = get_object_or_404(Group, index=group_index)
    contact = get_object_or_404(Contact, index=contact_index)
    student_list = group.student_set.all()
    student_list = student_list.order_by('name')

    f = StringIO.StringIO() # create a file-like object
    workbook = xl.Workbook(f)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, smart_str(u"Nafn"))
    worksheet.write(0, 1, smart_str(u"Kennitala"))

    row = 1
    col = 0

    for student in student_list:
        worksheet.write(row, col, student.name)
        worksheet.write(row, col+1, student.kt)
        row += 1

    workbook.close()

    subject = 'Pangea 2018 - Staðfesting'
    body = ''' Sæl/Sæl
    '''

    email = EmailMessage(
        subject,
        body,
        'nemendasvor@gmail.com',
        contact.email
    )

    email.attach('nemendur.xlsx', f.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()

    return HttpResponse('Takk fyrir skráninguna')


# def export_group_nparray(group_id):
#     # Returns a numpy array where the names of students in a group (identified
#     # with group_id) are in the first column and their kt in the second
#     group = get_object_or_404(Group, pk=group_id)
#     student_list = group.student_set.all()
#     nofn = np.empty((len(student_list),1), dtype='S200') # Er að prófa mig áfram með dtype. Þetta
#     kts = np.empty((len(student_list),2), dtype='S11')   # þarf trúlega ekki að vera svona klunnalegt.
#     table = np.stack((nofn, kts), axis=-1)
#
#     for i in range(len(student_list)):
#         table[i,0] = student_list[i].name
#         table[i,1] = student_list[i].kt
#
#     return table

def export_group_cvs(request, queryset):
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=nemendur.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Nafn"),
        smart_str(u"Kennitala"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.name),
            smart_str(obj.kt),
        ])
    return response
