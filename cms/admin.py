from django.contrib import admin
from cms.models import ToDoList, ToDo

# admin.site.register(ToDoList)
# admin.site.register(ToDo)


class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('id', 'todolist_name',)  # 一覧に出したい項目
    list_display_links = ('id', 'todolist_name',)  # 修正リンクでクリックできる項目
admin.site.register(ToDoList, ToDoListAdmin)


class ToDoAdmin(admin.ModelAdmin):
    list_display = ('id', 'todo_name', 'deadline', 'created_time', 'comp',)
    list_display_links = ('id', 'todo_name' ,)
admin.site.register(ToDo, ToDoAdmin)
