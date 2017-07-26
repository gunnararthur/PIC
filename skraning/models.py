# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class Group(models.Model):
    school = models.CharField(max_length=200)
    grade = models.CharField(max_length=1)

    def __str__(self):
        return self.school + self.grade

@python_2_unicode_compatible
class Student(models.Model):
    name = models.CharField(max_length=200)
    kt = models.CharField(max_length=11)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    points1 = models.IntegerField(default=0)
    points2 = models.IntegerField(default=0)
    points3 = models.IntegerField(default=0)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.name
