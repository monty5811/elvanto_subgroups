# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElvantoGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Group Name', max_length=250)),
                ('e_id', models.CharField(verbose_name='Elvanto ID', max_length=36)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ElvantoPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('e_id', models.CharField(verbose_name='Elvanto ID', max_length=36)),
                ('first_name', models.CharField(verbose_name='First Name', max_length=250)),
                ('preferred_name', models.CharField(verbose_name='Preferred Name', max_length=250, blank=True)),
                ('last_name', models.CharField(verbose_name='Last Name', max_length=250)),
                ('elvanto_groups', models.ManyToManyField(to='elvanto_subgroups.ElvantoGroup', blank=True, related_name='group_members')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('last_sync', models.DateTimeField(null=True, blank=True)),
                ('main_group', models.OneToOneField(to='elvanto_subgroups.ElvantoGroup', related_name='main_group')),
                ('sub_groups', models.ManyToManyField(to='elvanto_subgroups.ElvantoGroup', related_name='sub_groups')),
            ],
        ),
    ]
