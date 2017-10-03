from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse

from cms.models import ToDoList, ToDo
from cms.forms import ToDoListForm, ToDoForm, SerachForm

from django.db.models import Max,Min,Count

import datetime

def ToDoList_list(request):
    """ToDoリストの一覧"""
    form = ToDoListForm(request.POST or None)
    messages_error = None
    messages_success = None
    if request.method == 'POST':
        if form.is_valid():    # フォームのバリデーション
            flag = 0
            if len(request.POST["todolist_name"]) == 0:
                flag = 1
                messages_error = "ToDoリストの名称は1文字以上にしてください"
            elif len(request.POST["todolist_name"]) > 30:
                flag = 1
                messages_error = "ToDoリストの名称は30文字以内にしてください"
            else:
                for i in ToDoList.objects.all():
                    if str(request.POST["todolist_name"]) == str(i):
                        flag = 1
                        messages_error = "そのToDoリスト名は既に存在します"
            if flag == 0:
                todolist = form.save()
                todolist.save()
                messages_success = "新しいToDoリストが作成されました"
                # return redirect('cms:todolist_list')

    todolists = ToDoList.objects.annotate(latest_day=Max('todos__created_time')).order_by('-latest_day') # ToDoリストに登録されているToDoの作成日が新しい順にソート
    todo_count = []
    check_count = []
    near_dead = []
    now = datetime.datetime.now()
    now_date = datetime.date(now.year, now.month, now.day)
    time_between = []
    # ソートされたToDoリストに関して、順に処理を行う
    for i in todolists:
        tmp = ToDoList.objects.filter(todolist_name=i.todolist_name).annotate(c_todo=Count('todos__todo_name'))# そのToDoリストが親となるToDoの個数をカウント
        todo_count += [tmp[0].c_todo]

        tmp = ToDoList.objects.filter(todolist_name=i.todolist_name,todos__comp=True).annotate(c_check=Count('todos__todo_name'))# そのToDoリストが親となるToDoの内,完了した個数をカウント
        if tmp:
            check_count += [tmp[0].c_check]
        else:
            check_count += [0]

        tmp = ToDoList.objects.filter(todolist_name=i.todolist_name,todos__comp=False).annotate(near_day=Min('todos__deadline'))# そのToDoリストが親となるToDoの内,最も締め切りが近い日(完了したものは含まない)
        if tmp:
            near_dead += [tmp[0].near_day]
            time_between += [int((tmp[0].near_day - now_date).days)]
        else:
            near_dead += ['全て完了'] # 締め切りが近い日が1つも格納されていなければ「全て完了」、ToDoが0個でも同様に処理しtemplateのhtmlで再処理を行う
            time_between += [None]


    contexts = {
        'form':form,
        'todolists':todolists,
        'todo_count':todo_count,
        'check_count':check_count,
        'near_dead':near_dead,
        'time_between':time_between,
        'messages_error':messages_error,
        'messages_success':messages_success,
    }
    return render(request,'cms/ToDoList_list.html',contexts)


def ToDoList_edit(request, todolist_id):
    """ToDoリストの編集"""
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    messages = None
    if request.method == 'POST':
        form = ToDoListForm(request.POST, instance=todolist)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            flag = 0
            if len(request.POST["todolist_name"]) == 0:
                flag = 1
                messages = "ToDoリストの名称は1文字以上にしてください"
            elif len(request.POST["todolist_name"]) > 30:
                flag = 1
                messages = "ToDoリストの名称は30文字以内にしてください"
            else:
                for i in ToDoList.objects.all():
                    if int(i.id) == int(todolist_id):
                        pass
                    else:
                         if str(request.POST["todolist_name"]) == str(i):
                            flag = 1
                            messages = "そのToDoリスト名は既に存在します"
            if flag == 0:
                todolist = form.save(commit=False)
                todolist.save()
                return redirect('cms:todolist_list')

    else:    # GET の時
        form = ToDoListForm(instance=todolist)  # todolist インスタンスからフォームを作成

    return render(request, 'cms/ToDoList_edit.html', dict(form=form, todolist_id=todolist_id,messages=messages))


def ToDoList_del(request, todolist_id):
    """ToDoリストの削除"""
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    todolist.delete()
    return redirect('cms:todolist_list')



def ToDo_list(request, todolist_id,):
    """ToDoの一覧"""
    todolist = get_object_or_404(ToDoList, pk=todolist_id)  # 親のToDoリストを読む
    form = ToDoForm(request.POST or None)
    messages_error = None
    messages_success = None
    if request.method == 'POST':
        if form.is_valid():    # フォームのバリデーション
            flag = 0
            if len(request.POST["todo_name"]) == 0:
                flag = 1
                messages_error = "ToDoリの名称は1文字以上にしてください"
            elif len(request.POST["todo_name"]) > 30:
                flag = 1
                messages_error = "ToDoの名称は30文字以内にしてください"
            else:
                for i in todolist.todos.all():
                    if str(request.POST["todo_name"]) == str(i.todo_name):
                        flag = 1
                        messages_error = "そのToDo名は既に存在します"

            if flag == 0:
                todo= form.save(commit=False)
                todo.todolist = todolist  # このToDoの、親のToDoリストをセット
                todo.save()
                messages_success = "新しいToDoが作成されました"
                # return redirect('cms:todo_list', todolist_id=todolist_id)

    todos = todolist.todos.all().order_by('-created_time')   # ToDoリストの子供の、ToDoを読む
    check_todo = ToDoList.objects.filter(todolist_name=todolist).annotate(todo_count=Count('todos__todo_name')) #ToDoの数をカウント

    now = datetime.datetime.now()
    now_date = datetime.date(now.year, now.month, now.day)
    time_between = []
    for i in todos:
        time_between += [int((i.deadline - now_date).days)]

    contexts = {
        'form':form,
        'todolists_id':todolist_id,
        'todos':todos,
        'todolist':todolist,
        'c_count':check_todo[0].todo_count,
        'time_between':time_between,
        'messages_error':messages_error,
        'messages_success':messages_success,
    }
    return render(request,'cms/ToDo_list.html',contexts)


def ToDo_edit(request, todolist_id, todo_id):
    """ToDoの編集"""
    todolist = get_object_or_404(ToDoList, pk=todolist_id)  # 親のToDoリストを読む
    todo = get_object_or_404(ToDo, pk=todo_id)
    messages = None
    if request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            flag = 0
            if len(request.POST["todo_name"]) == 0:
                flag = 1
                messages = "ToDoの名称は1文字以上にしてください"
            elif len(request.POST["todo_name"]) > 30:
                flag = 1
                messages = "ToDoの名称は30文字以内にしてください"
            else:
                for i in todolist.todos.all():
                    if int(i.id) == int(todo_id):
                        pass
                    else:
                        if str(i.todo_name) == str(request.POST["todo_name"]):
                            flag = 1
                            messages = "そのToDo名は既に存在します"

            if flag == 0:
                todo= form.save(commit=False)
                todo.todolist = todolist  # このToDoの、親のToDoリストをセット
                todo.save()
                return redirect('cms:todo_list', todolist_id=todolist_id)

    else:    # GET の時
        form = ToDoForm(instance=todo)  # todo インスタンスからフォームを作成

    return render(request,'cms/ToDo_edit.html',dict(form=form, todolist_id=todolist_id, todo_id=todo_id, messages=messages))


def ToDo_del(request, todolist_id, todo_id):
    """感想の削除"""
    todo = get_object_or_404(ToDo, pk=todo_id)
    todo.delete()
    return redirect('cms:todo_list', todolist_id=todolist_id)


def Comp_change(request, todolist_id, todo_id):
    """ToDoの完了/未完了の切り替え"""
    todolist = get_object_or_404(ToDoList, pk=todolist_id)  # 親のToDoリストを読む
    todo = get_object_or_404(ToDo, pk=todo_id)
    if todo.comp:
        todo.comp = False
    else:
        todo.comp = True
    todo.save()
    return redirect('cms:todo_list', todolist_id=todolist_id)


def Search(request):
    """検索"""
    if request.is_ajax():
        print("sss")
    else:
        print("nnn")
    if request.method == 'GET':
        query = request.GET.get('query') #検索ワード：query
        if query:
            word_todo = [i.todo_name for i in ToDo.objects.filter(todo_name__icontains=query).order_by('-created_time')] #クエリを含むToDo名をそれに対応するToDoの作成日順にソート
            word_todo_id = [i.id for i in ToDo.objects.filter(todo_name__icontains=query).order_by('-created_time')] #クエリを含むToDoのIDをそれに対応するToDoの作成日順にソート
            word_todo_todolist = [j.todolist_name for j in (i.todolist for i in ToDo.objects.filter(todo_name__icontains=query).order_by('-created_time'))] #クエリを含むToDoの親ToDoリストをそれに対応するToDoの作成日順にソート
            word_todo_todolist_id = [j.id for j in (i.todolist for i in ToDo.objects.filter(todo_name__icontains=query).order_by('-created_time'))] #クエリを含むToDoの親ToDoリストIDをそれに対応するToDoの作成日順にソート
            word_deadline = [i.deadline for i in ToDo.objects.filter(todo_name__icontains=query).order_by('-created_time')] #クエリを含むToDoの締切日をそれに対応するToDoの作成日順にソート
            word_created_time = [i.created_time for i in ToDo.objects.filter(todo_name__icontains=query).order_by('-created_time')] #クエリを含むToDoの作成日に関して、作成日順にソート
            word_todolist = [i.todolist_name for i in ToDoList.objects.filter(todolist_name__icontains=query).annotate(latest_day=Max('todos__created_time')).order_by('-latest_day')] #クエリを含むToDoリスト名をそれに対応するToDoリストの作成日(ToDoリスト内の最も新しい作成日)順にソート
            word_todolist_id = [i.id for i in ToDoList.objects.filter(todolist_name__icontains=query).annotate(latest_day=Max('todos__created_time')).order_by('-latest_day')] #クエリを含むToDoリストのIDをそれに対応するToDoリストの作成日(ToDoリスト内の最も新しい作成日)順にソート
            word_todolist_created = [i.latest_day for i in ToDoList.objects.filter(todolist_name__icontains=query).annotate(latest_day=Max('todos__created_time')).order_by('-latest_day')] #クエリを含むToDoリストの作成日(ToDoリスト内の最も新しい作成日)に関して、作成日順にソート
            for i in range(len(word_todolist_created)):
                if word_todolist_created[i] == None:
                    word_todolist_created[i] = "ToDoがありません"
            word_todolist_id = [ str(x) for x in word_todolist_id]
            d = {
                'word_todo':word_todo,
                'word_todo_id':word_todo_id,
                'word_todo_todolist':word_todo_todolist,
                'word_todo_todolist_id':word_todo_todolist_id,
                'num_word_todolist':str(len(word_todolist)),
                'num_word_todo':str(len(word_todo)),
                'word_deadline':word_deadline,
                'word_created_time':word_created_time,
                'word_todolist':word_todolist,
                'word_todolist_id':word_todolist_id,
                'word_todolist_created':word_todolist_created,
            }
            return JsonResponse(d)

    return render(request, 'cms/Search.html')
