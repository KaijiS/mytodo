# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 13:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('todo_name', models.CharField(max_length=30, verbose_name='ToDo')),
                ('deadline', models.DateTimeField(verbose_name='Deadline')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Create_time')),
                ('comp', models.BooleanField(verbose_name='完了/末完了')),
            ],
        ),
        migrations.CreateModel(
            name='ToDoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('todolist_name', models.CharField(max_length=30, verbose_name='ToDoList')),
            ],
        ),
        migrations.AddField(
            model_name='todo',
            name='todolist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo', to='cms.ToDoList', verbose_name='todo名'),
        ),
    ]
