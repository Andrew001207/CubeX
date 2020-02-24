import datetime
from typing import List, Any

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from .models import Task
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def home(request, *args, **kwargs):
    today = datetime.datetime.now().date()
    return render(request, "home.html", {"today": today})


def task_view(request, *args, **kwargs):
    allTasks = Task.objects.all()
    allEvents = Event.objects.all()
    dict = {'allTasks': allTasks, 'allEvents': allEvents}
    return render(request, 'task.html', dict)


def get_data(request, *args, **kwargs):
    data = {'a': 'ab', 'b': 'ba'}
    return JsonResponse(data)


class Pie_View (View):
    def get(self, request, *args, **kwargs):
        allTasks = Task.objects.all()
        allEvents = Event.objects.all()
        task_list = []
        time_list = []
        taskid_map = {}
        i = 0
        for task in allTasks:
            task_list.append(task.task_name)
            taskid_map[task.task_id] = i
            i = i + 1
        for i in task_list:
            time_list.append(datetime.timedelta())
        for event in allEvents:
            index = taskid_map[event.task_id]
            if event.end_time is not None:
                time_list[index] += event.end_time - event.start_time
        i = 0
        for time in time_list:
            time_list[i] = time.seconds
            i = i + 1

        dict = {'task_list': task_list, 'time_list': time_list}
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
        allEvents = Event.objects.all()
        allTasks = Task.objects.all()
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

