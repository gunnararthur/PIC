# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-24 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skraning', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='groups',
            field=models.ManyToManyField(db_table='m2m_contact_group', to='skraning.Group'),
        ),
    ]