from django.db import models
from django.db.models import Count
from django import forms

class ToDoList(models.Model):
    """ToDoリスト"""
    todolist_name = models.CharField('ToDoリスト名', max_length=60)

    def __str__(self):
        return self.todolist_name


class ToDo(models.Model):
    """ToDo"""
    todolist = models.ForeignKey(ToDoList, related_name='todos')
    todo_name = models.CharField('ToDo名', max_length=100)
    deadline = models.DateField('期限', auto_now_add = False)
    created_time = models.DateField('作成日', auto_now_add = True) #, verbose_name='作成日'
    comp = models.BooleanField('完了/末完了')

    def __str__(self):
        return self.todo_name, self.deadline, self.created_time, self.comp
