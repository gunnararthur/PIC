# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Group, Student, Contact


class StudentAdmin(admin.ModelAdmin):
    list_filter = ('group', )

class GroupAdmin(admin.ModelAdmin):
    def groups(self):
        return '<a href="/admin/skraning/student/?group__id__exact=%d">%s</a>' % (self.group_id, self.group)
    groups.allow_tags = True

admin.site.register(Student, StudentAdmin)
admin.site.register(Group)
admin.site.register(Contact)
