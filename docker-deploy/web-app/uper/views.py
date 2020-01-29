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
        
        if exist: # on successful login
            # set session cookie
            user_id = User.objects.get(username = username_).id
            request.session["user_id"] = user_id 
            # redirect to Uper main page
            return HttpResponseRedirect(reverse('uper:main_page'))            

        else: # fail to login
            return HttpResponse('Wrong username or password!')

def main_page(request):
    # get current user id from session
    user_id = request.session["user_id"]
    username = User.objects.get(pk = user_id).username
    # build context dictionary to inject into html page
    context = {'username':username,}
    return render(request, 'uper/main_page.html', context)
    

