from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import User

def index(request):
#    return HttpResponse("Uper is Awesome!")
    return render(request, 'uper/index.html')

def register(request):
    return HttpResponse("Register Page");

def login(request):
    if request.method == 'POST':
        username_ = request.POST.get('username_')
        password_ = request.POST.get('password_')
        exist = User.objects.filter(username = username_, password = password_)
        if exist:
            return HttpResponse('login successfully!')           
        else:
            return HttpResponse('Wrong username or password!')
        
