from django.shortcuts import render
from .models import User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

def register_process(request):
    user = User(username=request.POST['username'], password=request.POST['password'])
    user.save()
    return HttpResponseRedirect(reverse('uper:index')) # use reverse() to avoid hard-code url

def login(request):
    if request.method == 'POST':
        username_ = request.POST['username']
        password_ = request.POST['password']
        exist = User.objects.filter(username = username_, password = password_)
        if exist:
            return HttpResponse('login successfully!')           
        else:
            return HttpResponse('Wrong username or password!')
        

