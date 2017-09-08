# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-24 18:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_auto_20170824_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecomment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xcourses.Course', verbose_name='评论的课程'),
        ),
        migrations.AlterField(
            model_name='coursecomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]