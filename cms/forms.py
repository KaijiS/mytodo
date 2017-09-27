from django.forms import ModelForm
from cms.models import ToDoList, ToDo
from django import forms


class ToDoListForm(ModelForm):
    """ToDoリストのフォーム"""
    class Meta:
        model = ToDoList
        fields = ('todolist_name',)
        widgets = {
            'todolist_name': forms.TextInput(attrs={'placeholder':'リスト名を入力してください'})
        }


class ToDoForm(ModelForm):
    """ToDoのフォーム"""
    class Meta:
        model = ToDo
        fields = ('todo_name', 'deadline', 'comp')
        widgets = {
            'todo_name': forms.TextInput(attrs={'placeholder':'ToDo名を入力してください'}),
            'deadline': forms.TextInput(attrs={'placeholder':'(例) 2017-09-21'}),
            'comp': forms.HiddenInput(),
        }


class SerachForm(forms.Form):
    word = forms.CharField(max_length = 100,widget=forms.TextInput(attrs={'size':'60'}))
