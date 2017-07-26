# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Group, Student, Contact

admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Contact)
