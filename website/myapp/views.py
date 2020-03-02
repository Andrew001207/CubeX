import datetime
from django.http import JsonResponse
from django.views.generic import View
from .models import Event, Task, Cube
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CubeIdForm, TaskForm

def home(request, *args, **kwargs):
    today = datetime.datetime.now().date()
    return render(request, "home.html", {"today": today})


def task_view(request, *args, **kwargs):
    username = request.user.username
    allTasks = Task.objects.filter(username=username).order_by('cube_id')
    dict = {'allTasks': allTasks}
    return render(request, 'task.html', dict)


def get_data(request, *args, **kwargs):
    data = {'a': 'ab', 'b': 'ba'}
    return JsonResponse(data)


class Pie_View (View):
    def get(self, request, cube_id = 1):
        dict = self.create_dict(cube_id, request)
        return render(request, 'piechart.html', dict)

    def create_dict(self, cube_id, request):
        if request.user.is_authenticated == True:
            username = request.user.username
        allTasks = Task.objects.filter(cube_id=cube_id)

        task_list = []
        time_list = []
        taskid_map = {}
        i = 0
        taskidlist = []
        for task in allTasks:
            task_list.append(task.task_name)
            taskid_map[task.task_id] = i
            taskidlist.append(task.task_id)
            i = i + 1

        allEvents = Event.objects.filter(task_id__in = taskidlist)
        for i in task_list:
            time_list.append(datetime.timedelta())
        for event in allEvents:
            if event.end_time is not None:
                index = taskid_map[event.task_id]
                time_list[index] += event.end_time - event.start_time

        i = 0
        for time in time_list:
            time_list[i] = time.seconds
            i = i + 1
        user_cubes = Cube.objects.filter(username=username)
        cubes = []
        for cube in user_cubes:
             cubes.append(cube.cube_id)
        dict = {'task_list': task_list, 'time_list': time_list, 'user_cubes': cubes}
        return dict

    def post(self, request):
        form = CubeIdForm(request.POST)
        if form.is_valid():
            cube_id = form.cleaned_data['cube_id']
            dict = self.create_dict(cube_id,request)
            return render(request, 'piechart.html', dict)


def login_view(request, *args, **kwargs):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        msg = "user sucessfully logged in"
    else:
        msg ="no such user or passiert"
    return render(request, "registration/login.html", {'msg' : msg})

def nav_bar(request):
    dict = {}
    return render(request, "nav.html", dict)

class BarView(View):
    def get(self, request, *args, **kwargs):
        username = request.user.username
        allEvents = Event.objects.all()
        allTasks = Task.objects.filter(username=username)
        taskid_map = {}
        group_list = []
        time_spent = []
        for task in allTasks:
            taskid_map[task.task_id] = task.group_name
            if task.group_name not in group_list:
                group_list.append(task.group_name)
                time_spent.append(0)
        for event in allEvents:
            if event.end_time is not None:
                dtime = (event.end_time - event.start_time).seconds
                time_spent[group_list.index(taskid_map[event.task_id])] += dtime
        dict = {'group_list': group_list, 'time_spent': time_spent}
        return render(request, 'barchart.html', dict)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

class CreateTask(View):
    def get(self, request):
        form = TaskForm(request.POST)
        return render(request, 'createTask.html', {'form':form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            new_Task = Task()
            new_Task.cube_id = form.cleaned_data['cube_id']
            new_Task.task_name = form.cleaned_data['task_name']
            new_Task.group_name = form.cleaned_data['task_group']
            new_Task.username = request.user.username
            new_Task.save()
            form.clean()
        return render(request, 'createTask.html', {'form': form})