# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# from django.contrib.postgres.fields import ArrayField

# Create your models here.

@python_2_unicode_compatible
class Group(models.Model):
    name = models.CharField(primary_key=True,max_length=200)
    school = models.CharField(max_length=200)
    grade = models.CharField(max_length=1)
    index = models.IntegerField(default=0)

    def __str__(self):
        return self.school + self.grade

@python_2_unicode_compatible
class Student(models.Model):
    name = models.CharField(max_length=200)
    ans1 = models.CharField(max_length=100, default='')
    ans2 = models.CharField(max_length=100, default='')
    ans3 = models.CharField(max_length=100, default='')
    kt = models.CharField(primary_key=True,max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    points1 = models.IntegerField(default=0)
    points2 = models.IntegerField(default=0)
    points3 = models.IntegerField(default=0)
    index = models.IntegerField(default=0)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(primary_key=True,max_length=200)
    groups = models.ManyToManyField(Group)
    index = models.IntegerField(default=0)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Round(models.Model):
    grade = models.CharField(primary_key=True,max_length=1)
    round_nr = models.IntegerField(primary_key=True,default=0)
    nr_of_questions = models.IntegerField(default=0)
    answer_key = models.CharField(max_length=100, default='')
    weights = models.CharField(max_length=100, default='')
    cutoff = models.IntegerField(default=0)

    def __str__(self):
        return self.round_nr + '. umferð - ' + self.grade + '. bekkur'

    def is_legal(self):
        return len(self.weights) is len(self.answer_key)

    def get_nr_of_questions(self):
        return len(self.answer_key)
