from django.conf.urls import url
from cms import views

urlpatterns = [
    # ToDoリスト
    url(r'^ToDoList/$', views.ToDoList_list, name='todolist_list'),   # 一覧
    url(r'^ToDoList/mod/(?P<todolist_id>\d+)/$', views.ToDoList_edit, name='todolist_mod'),  # 修正
    url(r'^ToDoList/del/(?P<todolist_id>\d+)/$', views.ToDoList_del, name='todolist_del'),   # 削除

    # ToDo
    url(r'^ToDo/(?P<todolist_id>\d+)/$', views.ToDo_list, name='todo_list'),  # 一覧
    url(r'^ToDo/mod/(?P<todolist_id>\d+)/(?P<todo_id>\d+)/$', views.ToDo_edit, name='todo_mod'),  # 修正
    url(r'^ToDo/del/(?P<todolist_id>\d+)/(?P<todo_id>\d+)/$', views.ToDo_del, name='todo_del'),   # 削除
    url(r'^ToDo/change/(?P<todolist_id>\d+)/(?P<todo_id>\d+)/$', views.Comp_change, name='comp_change'),   #完了/未完了反転

    # 検索
    url(r'^Search/$', views.Search, name='search'),

    # 検索
    url(r'^Sort/$', views.Sort, name='sort'),
]
